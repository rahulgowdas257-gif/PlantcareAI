from io import BytesIO
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import database
from components import ui
from PIL import Image


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.path_patch = patch.object(database, "DB_PATH", self.db_path)
        self.path_patch.start()
        database.initialize_database()

    def tearDown(self):
        self.path_patch.stop()
        self.temp_dir.cleanup()

    def test_passwords_are_hashed_and_authenticate(self):
        user_id = database.create_user("gardener", "correct-horse")
        self.assertGreater(user_id, 0)
        self.assertEqual(database.authenticate_user("GARDENER", "correct-horse"), user_id)
        self.assertIsNone(database.authenticate_user("gardener", "wrong-password"))
        with database.connection() as conn:
            stored = conn.execute("SELECT password_hash FROM users").fetchone()[0]
        self.assertNotEqual(stored, "correct-horse")

    def test_plant_reminder_and_growth_lifecycle(self):
        owner = "user:1"
        database.seed_sample_plants(owner)
        plants = database.list_plants(owner)
        self.assertEqual(len(plants), 3)
        plant = plants[0]
        reminders = database.list_reminders(owner)
        self.assertEqual(len(reminders), 6)

        reminder = reminders[0]
        self.assertTrue(database.complete_reminder(owner, reminder["id"]))
        updated = next(item for item in database.list_reminders(owner) if item["id"] == reminder["id"])
        self.assertEqual(updated["last_completed"], date.today().isoformat())

        record_id = database.add_growth_record(
            owner, plant["id"], date.today().isoformat(), 12.5, "New leaves"
        )
        self.assertGreater(record_id, 0)
        self.assertEqual(len(database.list_growth_records(owner, plant["id"])), 1)

        self.assertTrue(database.delete_plant(owner, plant["id"]))
        self.assertIsNone(database.get_plant(owner, plant["id"]))
        self.assertEqual(database.list_growth_records(owner, plant["id"]), [])

    def test_users_cannot_access_another_owners_records(self):
        database.seed_sample_plants("user:one")
        plant = database.list_plants("user:one")[0]
        self.assertEqual(database.list_plants("user:two"), [])
        self.assertIsNone(database.get_plant("user:two", plant["id"]))
        self.assertFalse(database.complete_reminder("user:two", 1))

    def test_sample_data_is_seeded_only_once(self):
        database.seed_sample_plants("guest:one")
        database.seed_sample_plants("guest:one")
        self.assertEqual(len(database.list_plants("guest:one")), 3)
        self.assertEqual(len(database.list_reminders("guest:one")), 6)

    def test_create_edit_and_schedule_a_plant(self):
        owner = "user:plant-lifecycle"
        data = {
            "name": "Fern",
            "scientific_name": "Nephrolepis",
            "category": "Indoor",
            "age_years": 2,
            "added_date": date.today().isoformat(),
            "growth_stage": "Growing",
            "health_status": "Healthy",
            "watering": "Keep soil lightly moist.",
            "sunlight": "Indirect light",
            "humidity": "High",
            "soil": "Well-draining",
            "fertilizer": "Monthly",
            "flowering": "",
            "fruit": "",
            "harvest": "",
            "photo_path": "",
        }
        plant_id = database.save_plant(owner, data)
        self.assertEqual(database.get_plant(owner, plant_id)["name"], "Fern")

        data["name"] = "Boston Fern"
        database.save_plant(owner, data, plant_id)
        self.assertEqual(database.get_plant(owner, plant_id)["name"], "Boston Fern")

        due_date = (date.today() + timedelta(days=4)).isoformat()
        database.update_reminder(owner, plant_id, "Watering", 4, due_date)
        reminder = next(
            item for item in database.list_reminders(owner)
            if item["plant_id"] == plant_id and item["kind"] == "Watering"
        )
        self.assertEqual(reminder["next_due"], due_date)
        self.assertEqual(reminder["interval_days"], 4)

    def test_uploaded_images_are_validated_and_stored_under_uploads(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            upload_dir = root / "uploads"
            image_data = BytesIO()
            Image.new("RGB", (24, 16), color="green").save(image_data, format="PNG")
            uploaded = SimpleNamespace(getvalue=image_data.getvalue)
            with patch.object(ui, "BASE_DIR", root), patch.object(ui, "UPLOAD_DIR", upload_dir):
                relative_path = ui.save_uploaded_image(uploaded)
                saved_path = ui.image_path(relative_path)
                self.assertIsNotNone(saved_path)
                with Image.open(saved_path) as saved_image:
                    self.assertEqual(saved_image.size, (24, 16))
                with self.assertRaises(ValueError):
                    ui.save_uploaded_image(SimpleNamespace(getvalue=lambda: b"not an image"))


if __name__ == "__main__":
    unittest.main()
