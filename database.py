"""SQLite storage and data-access helpers for PlantCare AI."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterator


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("PLANTCARE_DB_PATH", str(BASE_DIR / "plantcare.db")))
PASSWORD_ITERATIONS = 310_000


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    """Open a transaction and always close its SQLite connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database() -> None:
    """Create the local database and its tables when the app starts."""
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_key TEXT NOT NULL,
                name TEXT NOT NULL,
                scientific_name TEXT NOT NULL DEFAULT '',
                category TEXT NOT NULL DEFAULT 'Indoor',
                age_years INTEGER NOT NULL DEFAULT 0,
                added_date TEXT NOT NULL,
                growth_stage TEXT NOT NULL DEFAULT 'Seedling',
                health_status TEXT NOT NULL DEFAULT 'Healthy',
                watering TEXT NOT NULL DEFAULT '',
                sunlight TEXT NOT NULL DEFAULT '',
                humidity TEXT NOT NULL DEFAULT '',
                soil TEXT NOT NULL DEFAULT '',
                fertilizer TEXT NOT NULL DEFAULT '',
                flowering TEXT NOT NULL DEFAULT '',
                fruit TEXT NOT NULL DEFAULT '',
                harvest TEXT NOT NULL DEFAULT '',
                photo_path TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
                kind TEXT NOT NULL CHECK(kind IN ('Watering', 'Fertilizing')),
                interval_days INTEGER NOT NULL CHECK(interval_days > 0),
                next_due TEXT NOT NULL,
                last_completed TEXT NOT NULL DEFAULT '',
                UNIQUE(plant_id, kind)
            );
            CREATE TABLE IF NOT EXISTS growth_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
                observation_date TEXT NOT NULL,
                height_cm REAL,
                notes TEXT NOT NULL DEFAULT '',
                photo_path TEXT NOT NULL DEFAULT ''
            );
            CREATE INDEX IF NOT EXISTS idx_plants_owner ON plants(owner_key);
            CREATE INDEX IF NOT EXISTS idx_reminders_due ON reminders(next_due);
            CREATE INDEX IF NOT EXISTS idx_growth_plant_date
                ON growth_records(plant_id, observation_date);
            """
        )


def _password_digest(password: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return digest.hex()


def create_user(username: str, password: str) -> int:
    """Create a user with a salted PBKDF2 password hash."""
    salt = secrets.token_bytes(16)
    digest = _password_digest(password, salt)
    try:
        with connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, password_hash, password_salt) "
                "VALUES (?, ?, ?)",
                (username.strip(), digest, salt.hex()),
            )
            return int(cursor.lastrowid)
    except sqlite3.IntegrityError as exc:
        raise ValueError("That username is already in use.") from exc


def authenticate_user(username: str, password: str) -> int | None:
    """Return a user's ID when their password matches; otherwise return None."""
    with connection() as conn:
        row = conn.execute(
            "SELECT id, password_hash, password_salt FROM users "
            "WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
    if row is None:
        return None
    try:
        salt = bytes.fromhex(row["password_salt"])
    except ValueError:
        return None
    digest = _password_digest(password, salt)
    return int(row["id"]) if hmac.compare_digest(digest, row["password_hash"]) else None


def seed_sample_plants(owner_key: str) -> None:
    """Add a small starter collection only when the owner has no plants yet."""
    samples = [
        {
            "name": "Tulsi",
            "scientific_name": "Ocimum tenuiflorum",
            "category": "Herb",
            "age_years": 1,
            "growth_stage": "Mature",
            "health_status": "Healthy",
            "watering": "Water when the top 2 cm of soil feels dry.",
            "sunlight": "4–6 hours of bright sunlight",
            "humidity": "40–60%",
            "soil": "Well-draining, nutrient-rich potting mix",
            "fertilizer": "Balanced organic feed every 4 weeks in growing season.",
            "flowering": "Small flower spikes in warm weather",
            "fruit": "Not applicable",
            "harvest": "Pick leaves as needed; avoid removing more than one-third.",
        },
        {
            "name": "Money Plant",
            "scientific_name": "Epipremnum aureum",
            "category": "Indoor",
            "age_years": 2,
            "growth_stage": "Growing",
            "health_status": "Healthy",
            "watering": "Water when the top 3 cm of soil dries.",
            "sunlight": "Bright, indirect light",
            "humidity": "40–70%",
            "soil": "Loose, well-draining indoor potting mix",
            "fertilizer": "Half-strength balanced feed every 4–6 weeks in spring/summer.",
            "flowering": "Rare indoors",
            "fruit": "Not applicable",
            "harvest": "Trim vines to shape; cuttings can be propagated.",
        },
        {
            "name": "Cherry Tomato",
            "scientific_name": "Solanum lycopersicum",
            "category": "Vegetable",
            "age_years": 1,
            "growth_stage": "Fruiting",
            "health_status": "Healthy",
            "watering": "Water deeply at the base every 2 days; keep soil evenly moist.",
            "sunlight": "6–8 hours of full direct sun daily",
            "humidity": "50–65%",
            "soil": "Rich compost-amended potting soil with good drainage",
            "fertilizer": "High-potassium tomato feed every 2 weeks during fruiting.",
            "flowering": "Clusters of bright yellow star-shaped blossoms along flower trusses.",
            "fruit": "Sweet round cherry tomatoes developing from green to deep glossy red.",
            "harvest": "Harvest ripe fruits when firm and uniformly red; gently twist off vine.",
        },
    ]

    with connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM plants WHERE owner_key = ? LIMIT 1", (owner_key,)
        ).fetchone()
        if existing:
            return
        today = date.today()
        for index, plant in enumerate(samples):
            cursor = conn.execute(
                """
                INSERT INTO plants (
                    owner_key, name, scientific_name, category, age_years,
                    added_date, growth_stage, health_status, watering, sunlight,
                    humidity, soil, fertilizer, flowering, fruit, harvest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    owner_key,
                    plant["name"],
                    plant["scientific_name"],
                    plant["category"],
                    plant["age_years"],
                    (today - timedelta(days=30 * (index + 2))).isoformat(),
                    plant["growth_stage"],
                    plant["health_status"],
                    plant["watering"],
                    plant["sunlight"],
                    plant["humidity"],
                    plant["soil"],
                    plant["fertilizer"],
                    plant["flowering"],
                    plant["fruit"],
                    plant["harvest"],
                ),
            )
            plant_id = int(cursor.lastrowid)
            water_due = today + timedelta(days=(index + 1))
            feed_due = today + timedelta(days=(index + 5))
            conn.executemany(
                "INSERT INTO reminders (plant_id, kind, interval_days, next_due) "
                "VALUES (?, ?, ?, ?)",
                [
                    (plant_id, "Watering", 7, water_due.isoformat()),
                    (plant_id, "Fertilizing", 30, feed_due.isoformat()),
                ],
            )


def list_plants(owner_key: str) -> list[dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM plants WHERE owner_key = ? ORDER BY name COLLATE NOCASE",
            (owner_key,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_plant(owner_key: str, plant_id: int) -> dict[str, Any] | None:
    with connection() as conn:
        row = conn.execute(
            "SELECT * FROM plants WHERE owner_key = ? AND id = ?",
            (owner_key, plant_id),
        ).fetchone()
    return dict(row) if row else None


def save_plant(owner_key: str, data: dict[str, Any], plant_id: int | None = None) -> int:
    fields = (
        "name", "scientific_name", "category", "age_years", "added_date",
        "growth_stage", "health_status", "watering", "sunlight", "humidity",
        "soil", "fertilizer", "flowering", "fruit", "harvest", "photo_path",
    )
    values = [data.get(field, "") for field in fields]
    with connection() as conn:
        if plant_id is None:
            placeholders = ", ".join("?" for _ in range(len(fields) + 1))
            cursor = conn.execute(
                f"INSERT INTO plants (owner_key, {', '.join(fields)}) "
                f"VALUES ({placeholders})",
                [owner_key, *values],
            )
            plant_id = int(cursor.lastrowid)
            due = date.today()
            conn.executemany(
                "INSERT INTO reminders (plant_id, kind, interval_days, next_due) "
                "VALUES (?, ?, ?, ?)",
                [
                    (plant_id, "Watering", 7, (due + timedelta(days=7)).isoformat()),
                    (plant_id, "Fertilizing", 30, (due + timedelta(days=30)).isoformat()),
                ],
            )
        else:
            assignments = ", ".join(f"{field} = ?" for field in fields)
            cursor = conn.execute(
                f"UPDATE plants SET {assignments} WHERE owner_key = ? AND id = ?",
                [*values, owner_key, plant_id],
            )
            if cursor.rowcount == 0:
                raise ValueError("Plant not found in this collection.")
    return plant_id


def delete_plant(owner_key: str, plant_id: int) -> bool:
    with connection() as conn:
        cursor = conn.execute(
            "DELETE FROM plants WHERE owner_key = ? AND id = ?", (owner_key, plant_id)
        )
    return cursor.rowcount > 0


def list_reminders(owner_key: str) -> list[dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute(
            """
            SELECT r.*, p.name AS plant_name
            FROM reminders r JOIN plants p ON p.id = r.plant_id
            WHERE p.owner_key = ?
            ORDER BY r.next_due, r.kind
            """,
            (owner_key,),
        ).fetchall()
    return [dict(row) for row in rows]


def update_reminder(
    owner_key: str, plant_id: int, kind: str, interval_days: int, next_due: str
) -> None:
    if kind not in {"Watering", "Fertilizing"} or interval_days < 1:
        raise ValueError("Choose a valid reminder type and interval.")
    with connection() as conn:
        plant = conn.execute(
            "SELECT 1 FROM plants WHERE owner_key = ? AND id = ?",
            (owner_key, plant_id),
        ).fetchone()
        if plant is None:
            raise ValueError("Plant not found in this collection.")
        conn.execute(
            """
            INSERT INTO reminders (plant_id, kind, interval_days, next_due)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(plant_id, kind) DO UPDATE SET
                interval_days = excluded.interval_days, next_due = excluded.next_due
            """,
            (plant_id, kind, interval_days, next_due),
        )


def complete_reminder(owner_key: str, reminder_id: int) -> bool:
    today = date.today()
    with connection() as conn:
        row = conn.execute(
            """
            SELECT r.interval_days FROM reminders r
            JOIN plants p ON p.id = r.plant_id
            WHERE r.id = ? AND p.owner_key = ?
            """,
            (reminder_id, owner_key),
        ).fetchone()
        if row is None:
            return False
        next_due = (today + timedelta(days=int(row["interval_days"]))).isoformat()
        conn.execute(
            "UPDATE reminders SET last_completed = ?, next_due = ? WHERE id = ?",
            (today.isoformat(), next_due, reminder_id),
        )
    return True


def add_growth_record(
    owner_key: str,
    plant_id: int,
    observation_date: str,
    height_cm: float | None,
    notes: str,
    photo_path: str = "",
) -> int:
    with connection() as conn:
        plant = conn.execute(
            "SELECT 1 FROM plants WHERE owner_key = ? AND id = ?",
            (owner_key, plant_id),
        ).fetchone()
        if plant is None:
            raise ValueError("Plant not found in this collection.")
        cursor = conn.execute(
            """
            INSERT INTO growth_records
                (plant_id, observation_date, height_cm, notes, photo_path)
            VALUES (?, ?, ?, ?, ?)
            """,
            (plant_id, observation_date, height_cm, notes, photo_path),
        )
        return int(cursor.lastrowid)


def list_growth_records(
    owner_key: str, plant_id: int | None = None
) -> list[dict[str, Any]]:
    query = """
        SELECT g.*, p.name AS plant_name FROM growth_records g
        JOIN plants p ON p.id = g.plant_id
        WHERE p.owner_key = ?
    """
    params: list[Any] = [owner_key]
    if plant_id is not None:
        query += " AND g.plant_id = ?"
        params.append(plant_id)
    query += " ORDER BY g.observation_date, g.id"
    with connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]
