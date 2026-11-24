"""Unit and integration tests for app pages, database seeding, and components."""

from datetime import date, timedelta
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
import sample_data
from components import ui
import app


class AppIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_app.db"
        self.path_patch = patch.object(database, "DB_PATH", self.db_path)
        self.path_patch.start()
        database.initialize_database()

    def tearDown(self):
        self.path_patch.stop()
        self.temp_dir.cleanup()

    def test_app_constants_and_knowledge_base(self):
        self.assertGreaterEqual(len(app.LIBRARY), 10)
        self.assertGreaterEqual(len(app.PROBLEMS), 5)
        for plant in app.LIBRARY:
            self.assertIn("name", plant)
            self.assertIn("scientific", plant)
            self.assertIn("water", plant)
            self.assertIn("light", plant)
        library_names = " ".join(plant["name"].casefold() for plant in app.LIBRARY)
        for requested_name in ("tulsi", "money plant", "aloe vera", "rose", "hibiscus", "tomato", "mango", "neem", "snake plant", "peace lily"):
            self.assertIn(requested_name, library_names)
        self.assertTrue(
            all("confidence_score" not in profile for profile in sample_data.DEMO_ID_PRESETS.values())
        )

    def test_sample_plants_seed_and_reminders(self):
        owner = "guest:integration_test"
        database.seed_sample_plants(owner)
        plants = database.list_plants(owner)
        self.assertEqual(len(plants), 3)

        # Verify flower, fruit, and harvest fields exist in sample plants
        cherry_tomato = next((p for p in plants if "Tomato" in p["name"]), None)
        self.assertIsNotNone(cherry_tomato)
        self.assertIn("blossom", cherry_tomato["flowering"].lower())
        self.assertIn("tomato", cherry_tomato["fruit"].lower())
        self.assertIn("harvest", cherry_tomato["harvest"].lower())

        reminders = database.list_reminders(owner)
        self.assertEqual(len(reminders), 6)

    def test_badge_styling_helper(self):
        badge_html = ui.badge("Needs Water", "urgent")
        self.assertIn("pill pill-urgent", badge_html)
        self.assertIn("Needs Water", badge_html)

        good_badge = ui.badge("Healthy", "good")
        self.assertIn("pill pill-good", good_badge)

    def test_growth_chart_generation(self):
        records = [
            {"plant_name": "Tulsi", "observation_date": "2026-11-01", "height_cm": 15.0},
            {"plant_name": "Tulsi", "observation_date": "2026-11-20", "height_cm": 22.0},
        ]
        import streamlit as st
        with patch.object(st, "markdown") as markdown:
            ui.growth_chart(records)
        rendered = "".join(str(call.args[0]) for call in markdown.call_args_list)
        self.assertIn('<svg viewBox="0 0 760', rendered)
        self.assertIn("Tulsi", rendered)
        self.assertIn('path d="M', rendered)

    def test_guest_navigation_and_plant_create(self):
        from streamlit.testing.v1 import AppTest

        app_test = AppTest.from_file(
            str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30
        ).run()
        self.assertFalse(app_test.exception, [error.message for error in app_test.exception])
        app_test.button[0].click().run()
        self.assertFalse(app_test.exception, [error.message for error in app_test.exception])
        self.assertEqual(len(app_test.metric), 4)

        for page in (
            "My Plants", "Add Plant", "Plant Scanner", "Plant Health",
            "Care Reminders", "Growth Tracking", "Plant Library", "Settings", "Dashboard",
        ):
            app_test.sidebar.radio[0].set_value(page).run()
            self.assertFalse(app_test.exception, [error.message for error in app_test.exception])
            rendered_text = "\n".join(str(item.value) for item in app_test.markdown)
            if page == "Plant Scanner":
                self.assertIn("No identification or confidence score is generated.", rendered_text)
                self.assertNotIn("98.4%", rendered_text)
            if page == "Plant Health":
                self.assertIn("not a diagnosis", rendered_text.casefold())

        app_test.sidebar.radio[0].set_value("Add Plant").run()
        next(field for field in app_test.text_input if field.label == "Plant name *").set_value("Integration Fern")
        next(field for field in app_test.text_area if field.label == "Watering needs *").set_value(
            "Check soil moisture weekly."
        )
        app_test.form_submit_button[0].set_value(True)
        app_test.run()
        self.assertFalse(app_test.exception, [error.message for error in app_test.exception])
        self.assertTrue(
            any("Integration Fern" in item.value for item in app_test.success)
        )
        owner = app_test.session_state["guest_key"]
        self.assertTrue(any(plant["name"] == "Integration Fern" for plant in database.list_plants(owner)))


if __name__ == "__main__":
    unittest.main()
