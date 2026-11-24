"""Shared styling, image handling, and small presentation helpers."""

from __future__ import annotations

import html
import math
import uuid
from datetime import date as date_type
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"


def apply_global_styles() -> None:
    import streamlit as st

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
        :root { --forest:#143b2c; --green:#23744f; --mint:#e7f2e9; --lime:#b9dca7; --ink:#20352b; --muted:#718178; }
        html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
        .stApp { background:linear-gradient(180deg,#f6faf6 0%,#f2f7f2 100%); }
        [data-testid="stHeader"] { background:rgba(246,250,246,.88); }
        [data-testid="stSidebar"] { background:#143b2c; border-right:0; }
        [data-testid="stSidebar"] * { color:#eff7ef !important; }
        [data-testid="stSidebar"] [data-testid="stAlert"] { background:#ffffff12 !important; border:1px solid #ffffff26; color:#eff7ef !important; }
        [data-testid="stSidebar"] [data-testid="stAlert"] p { color:#eff7ef !important; }
        [data-testid="stSidebar"] .stButton > button { background:#ffffff12; color:#eff7ef !important; border-color:#ffffff35; }
        [data-testid="stSidebar"] .stButton > button:hover { background:#ffffff22; color:white !important; border-color:#b9dca7; }
        [data-testid="stSidebar"] [data-testid="stRadio"] label { padding:7px 8px; border-radius:9px; }
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:#ffffff17; }
        .block-container { max-width:1200px; padding-top:2rem; padding-bottom:3rem; }
        h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:var(--forest); letter-spacing:-.035em; }
        h1 { font-weight:800 !important; }
        h2,h3 { font-weight:700 !important; }
        p, .stMarkdown { line-height:1.55; }
        [data-testid="stMetric"] { background:white; border:1px solid #e6eee6; padding:18px 20px; border-radius:16px; box-shadow:0 6px 22px #143b2c0a; }
        [data-testid="stMetricLabel"] { color:#718178; }
        [data-testid="stMetricValue"] { color:#143b2c; font-family:'Manrope',sans-serif; font-weight:800; }
        .stButton > button, .stFormSubmitButton > button { border-radius:10px; min-height:2.65rem; font-weight:700; border:1px solid #d5e4d7; transition:all .16s ease; }
        .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:#23744f; border-color:#23744f; color:white; }
        .stButton > button:hover { transform:translateY(-1px); border-color:#23744f; color:#17603e; }
        .stButton > button[kind="primary"]:hover { color:white; background:#185d3d; }
        [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-testid="stDateInput"] input, [data-testid="stSelectbox"] [role="combobox"], [data-testid="stTextArea"] textarea { border-radius:10px; }
        [data-testid="stFileUploader"] { background:white; border:1px dashed #b6ceb9; border-radius:14px; padding:8px; }
        [data-testid="stDataFrame"] { border:1px solid #e6eee6; border-radius:12px; overflow:hidden; }
        .eyebrow { color:#39825b; text-transform:uppercase; font-weight:700; font-size:.75rem; letter-spacing:.12em; margin-bottom:.35rem; }
        .hero { background:radial-gradient(circle at 85% 20%,#b5d8a4 0,#b5d8a400 32%),linear-gradient(120deg,#143b2c,#286b48); color:white; padding:42px; border-radius:24px; box-shadow:0 16px 38px #143b2c20; }
        .hero h1,.hero p { color:white !important; }
        .hero h1 { font-size:clamp(2rem,4vw,3.35rem); line-height:1.08; margin:.4rem 0 1rem; }
        .hero p { max-width:650px; color:#e4f0e5 !important; font-size:1.08rem; }
        .hero-kicker { color:#d5edce; font-weight:700; letter-spacing:.1em; text-transform:uppercase; font-size:.75rem; }
        .soft-card { background:#fff; border:1px solid #e6eee6; border-radius:16px; padding:20px; box-shadow:0 6px 22px #143b2c08; height:100%; }
        .soft-card h3 { margin:.2rem 0 .45rem; font-size:1.05rem; }
        .soft-card p { color:#68796f; margin:0; }
        .plant-card { background:white; border:1px solid #e6eee6; border-radius:16px; padding:18px; margin-bottom:12px; }
        .plant-grid-box { background:white; border:1px solid #e1efe6; border-radius:16px; padding:1.25rem; margin-bottom:1rem; box-shadow:0 4px 14px rgba(20,59,44,0.05); transition:transform .15s ease, box-shadow .15s ease; }
        .plant-grid-box:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(20,59,44,0.1); border-color:#74c69d; }
        .pill { display:inline-block; border-radius:999px; background:#e9f4eb; color:#286b48; padding:4px 10px; font-size:.76rem; font-weight:700; }
        .pill-urgent { background:#ffe3e3; color:#c92a2a; border:1px solid #ffa8a8; }
        .pill-today { background:#fff3bf; color:#d9480f; border:1px solid #ffd43b; }
        .pill-good { background:#d8f3dc; color:#2d6a4f; border:1px solid #b7e4c7; }
        .pill-stage { background:#edf7ed; color:#1b4332; border:1px solid #c8e6c9; }
        .pill-neutral { background:#f1f3f5; color:#495057; border:1px solid #dee2e6; }
        .demo-banner { background:#fff9db; border-left:4px solid #fcc419; padding:0.85rem 1.1rem; border-radius:8px; margin:0.8rem 0 1.2rem; font-size:0.9rem; color:#664d03; }
        .muted { color:#718178; font-size:.9rem; }
        .section-note { color:#718178; margin-top:-.6rem; margin-bottom:1.3rem; }
        @media (max-width:640px) { .block-container { padding:1rem 1rem 2rem; } .hero { padding:25px 22px; border-radius:18px; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_uploaded_image(uploaded_file: Any) -> str:
    """Validate, normalize, and save an uploaded image as a local JPEG."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    try:
        source = Image.open(BytesIO(uploaded_file.getvalue()))
        if source.width > 12_000 or source.height > 12_000 or source.width * source.height > 25_000_000:
            raise ValueError("Please upload an image no larger than 25 megapixels.")
        source.load()
        image = source.convert("RGB")
    except ValueError:
        raise
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("That file could not be opened as an image.") from exc

    image.thumbnail((1600, 1600))
    path = UPLOAD_DIR / f"{uuid.uuid4().hex}.jpg"
    image.save(path, format="JPEG", quality=88, optimize=True)
    return str(path.relative_to(BASE_DIR))


def image_path(relative_path: str) -> Path | None:
    if not relative_path:
        return None
    candidate = (BASE_DIR / relative_path).resolve()
    try:
        candidate.relative_to(UPLOAD_DIR.resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def card(title: str, body: str, icon: str = "🌿") -> None:
    import streamlit as st

    safe_title = html.escape(title)
    safe_body = html.escape(body)
    st.markdown(
        f'<div class="soft-card"><div style="font-size:1.5rem">{icon}</div>'
        f"<h3>{safe_title}</h3><p>{safe_body}</p></div>",
        unsafe_allow_html=True,
    )


def badge(text: str, kind: str = "good") -> str:
    classes = {
        "good": "pill pill-good",
        "urgent": "pill pill-urgent",
        "today": "pill pill-today",
        "stage": "pill pill-stage",
        "neutral": "pill pill-neutral"
    }
    cls = classes.get(kind, "pill")
    return f'<span class="{cls}">{html.escape(text)}</span>'


def growth_chart(records: list[dict[str, Any]]) -> None:
    """Render a small responsive SVG chart without a compiled chart dependency."""
    import streamlit as st

    grouped: dict[str, list[tuple[str, float]]] = {}
    for record in records:
        if record.get("height_cm") is not None:
            grouped.setdefault(record["plant_name"], []).append(
                (record["observation_date"], float(record["height_cm"]))
            )
    if not grouped:
        st.info("Your growth chart will appear here after you record a plant observation.")
        return

    points = [point for series in grouped.values() for point in series]
    dates = [date for date, _ in points]
    values = [value for _, value in points]
    min_date, max_date = min(dates), max(dates)
    min_value, max_value = min(values), max(values)
    min_x = float(date_type.fromisoformat(min_date).toordinal())
    max_x = float(date_type.fromisoformat(max_date).toordinal())
    if math.isclose(min_value, max_value):
        padding = max(abs(min_value) * 0.1, 1.0)
        min_value -= padding
        max_value += padding

    colors = ["#23744f", "#e0a33a", "#4589b5", "#a45d92", "#729c47", "#db6f57"]
    chart_height = max(320, 295 + math.ceil(len(grouped) / 3) * 22)
    elements = [
        f'<svg viewBox="0 0 760 {chart_height}" role="img" aria-label="Plant growth height chart" '
        'style="width:100%;height:auto;background:#fff;border:1px solid #e6eee6;border-radius:14px">'
    ]
    for grid_index in range(4):
        y = 55 + grid_index * 64
        value = max_value - (max_value - min_value) * grid_index / 3
        elements.append(f'<line x1="62" y1="{y}" x2="730" y2="{y}" stroke="#eaf0ea"/>')
        elements.append(f'<text x="54" y="{y + 4}" text-anchor="end" fill="#718178" font-size="11">{value:.1f}</text>')

    for index, (plant_name, series) in enumerate(grouped.items()):
        color = colors[index % len(colors)]
        series.sort(key=lambda item: item[0])
        coordinates: list[tuple[float, float]] = []
        for observed, height in series:
            observed_x = float(date_type.fromisoformat(observed).toordinal())
            x = 396.0 if max_x == min_x else 62 + (observed_x - min_x) / (max_x - min_x) * 668
            y = 247 - (height - min_value) / (max_value - min_value) * 192
            coordinates.append((x, y))
        if len(coordinates) > 1:
            path = " ".join(
                ("M" if point_index == 0 else "L") + f" {x:.1f} {y:.1f}"
                for point_index, (x, y) in enumerate(coordinates)
            )
            elements.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round"/>')
        for (x, y), (_, height) in zip(coordinates, series):
            elements.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}">'
                f'<title>{html.escape(plant_name)}: {height:g} cm</title></circle>'
            )
        legend_x = 70 + (index % 3) * 220
        legend_y = 278 + (index // 3) * 20
        elements.append(f'<circle cx="{legend_x}" cy="{legend_y - 4}" r="4" fill="{color}"/>')
        elements.append(
            f'<text x="{legend_x + 10}" y="{legend_y}" fill="#40554a" font-size="12">'
            f'{html.escape(plant_name)}</text>'
        )
    elements.append(
        f'<text x="62" y="260" fill="#718178" font-size="11">{html.escape(min_date)}</text>'
        f'<text x="730" y="260" text-anchor="end" fill="#718178" font-size="11">{html.escape(max_date)}</text>'
        '</svg>'
    )
    st.markdown("**Recorded height (cm)**", unsafe_allow_html=True)
    st.markdown("".join(elements), unsafe_allow_html=True)
