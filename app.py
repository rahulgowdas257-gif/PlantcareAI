"""PlantCare AI — a local-first botanical plant care reminder system."""

from __future__ import annotations

from datetime import date, timedelta
import html
from typing import Any
import uuid

import streamlit as st
from PIL import UnidentifiedImageError

import database as db
from components.ui import apply_global_styles, badge, card, growth_chart, image_path, save_uploaded_image


st.set_page_config(
    page_title="PlantCare AI | Plant Care Reminder System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
db.initialize_database()
apply_global_styles()

LIBRARY: list[dict[str, str]] = [
    {
        "name": "Tulsi (Holy Basil)",
        "scientific": "Ocimum tenuiflorum",
        "category": "Herb",
        "water": "Keep lightly moist; water when the top 2 cm begins to dry.",
        "light": "4–6 hours of direct morning sun",
        "soil": "Rich, well-draining organic soil mix",
        "flowering": "Small fragrant purple-white flower spikes in warm weather",
        "fruit": "Tiny dark nutlets/seeds",
        "harvest": "Pinch top leaf clusters regularly to encourage bushy branches.",
        "tip": "Pinching flowers promotes sweeter, more aromatic leaf production.",
    },
    {
        "name": "Money Plant (Golden Pothos)",
        "scientific": "Epipremnum aureum",
        "category": "Indoor",
        "water": "Water when the top 3 cm of soil is dry.",
        "light": "Bright, indirect light (tolerates lower light)",
        "soil": "Loose indoor potting mix with perlite",
        "flowering": "Non-blooming indoor foliage",
        "fruit": "None indoors",
        "harvest": "Trim trailing vines to shape; root cuttings easily in water.",
        "tip": "Wipe leaves monthly with a damp cloth to remove dust.",
    },
    {
        "name": "Sweet Cherry Tomato",
        "scientific": "Solanum lycopersicum",
        "category": "Vegetable",
        "water": "Water deeply at base every 2 days; keep soil evenly moist.",
        "light": "6–8 hours of full direct sun daily",
        "soil": "Rich compost-amended potting soil with good drainage",
        "flowering": "Clusters of bright yellow star-shaped blossoms",
        "fruit": "Clusters of round cherry tomatoes ripening from green to red",
        "harvest": "Pick tomatoes when firm, glossy, and fully red with a gentle twist.",
        "tip": "Stake vines with a trellis and pinch suckers for larger yields.",
    },
    {
        "name": "Rose",
        "scientific": "Rosa spp.",
        "category": "Flowering",
        "water": "Water deeply at soil level when the top layer begins to dry.",
        "light": "At least 6 hours of direct sun",
        "soil": "Fertile, well-draining soil",
        "flowering": "Many varieties bloom repeatedly in warm growing seasons.",
        "fruit": "Some varieties form rose hips if blooms are left on the plant.",
        "harvest": "Cut blooms with clean tools; leave enough foliage for healthy growth.",
        "tip": "Good airflow and watering at soil level can help keep foliage dry.",
    },
    {
        "name": "Hibiscus",
        "scientific": "Hibiscus rosa-sinensis",
        "category": "Flowering",
        "water": "Keep soil evenly moist, not waterlogged; adjust for weather and pot size.",
        "light": "Bright light with several hours of sun",
        "soil": "Rich, well-draining potting mix",
        "flowering": "Large showy blooms may appear in warm conditions.",
        "fruit": "Seed capsules may develop after pollination.",
        "harvest": "Ornamental plant; only use flowers if the variety is known to be edible.",
        "tip": "Avoid abrupt changes in temperature and light.",
    },
    {
        "name": "Mango",
        "scientific": "Mangifera indica",
        "category": "Tree",
        "water": "Water young plants regularly; established trees need less frequent watering.",
        "light": "Full sun",
        "soil": "Deep, well-draining soil",
        "flowering": "Mature trees may produce seasonal flower panicles in suitable climates.",
        "fruit": "Fruit production depends on variety, maturity, climate, and pollination.",
        "harvest": "Harvest timing varies by cultivar and region; follow local growing guidance.",
        "tip": "Plan for a warm climate and ample space; container trees may not fruit.",
    },
    {
        "name": "Neem",
        "scientific": "Azadirachta indica",
        "category": "Tree",
        "water": "Water young plants while establishing; avoid persistently wet soil.",
        "light": "Full sun",
        "soil": "Well-draining soil",
        "flowering": "Mature plants may produce small fragrant flowers.",
        "fruit": "Mature trees may produce yellow drupes in suitable climates.",
        "harvest": "Harvest is not applicable to most home-grown ornamental trees.",
        "tip": "Check local climate and space requirements before planting outdoors.",
    },
    {
        "name": "Aloe Vera",
        "scientific": "Aloe barbadensis miller",
        "category": "Succulent",
        "water": "Let soil dry completely between thorough waterings.",
        "light": "Bright indirect light; acclimate gradually to direct sun",
        "soil": "Gritty, fast-draining cactus and succulent mix",
        "flowering": "Mature plants produce yellow tubular bloom spikes in spring",
        "fruit": "None indoors",
        "harvest": "Slice mature outer lower leaves for natural soothing aloe gel.",
        "tip": "Always use a pot with unobstructed drainage holes.",
    },
    {
        "name": "Monstera Deliciosa",
        "scientific": "Monstera deliciosa",
        "category": "Indoor",
        "water": "Water every 7–10 days when top 5 cm of soil dries.",
        "light": "Bright, filtered indirect sunlight",
        "soil": "Chunky aroid mix (orchid bark, perlite, peat)",
        "flowering": "Rare indoors; produces white spathes in tropical greenhouses",
        "fruit": "Non-fruiting indoors",
        "harvest": "Foliage ornamental; trim dead lower leaves at stem base.",
        "tip": "Provide a coir moss pole to support vigorous climbing roots.",
    },
    {
        "name": "Snake Plant",
        "scientific": "Sansevieria trifasciata",
        "category": "Indoor",
        "water": "Allow soil to dry fully before watering (every 2–3 weeks).",
        "light": "Tolerates low light up to bright indirect light",
        "soil": "Fast-draining gritty potting mix",
        "flowering": "Rarely blooms fragrant greenish-white flower stalks",
        "fruit": "None indoors",
        "harvest": "Air-purifying foliage; wipe dust occasionally.",
        "tip": "Overwatering is the only real danger—when in doubt, wait.",
    },
    {
        "name": "Peace Lily",
        "scientific": "Spathiphyllum wallisii",
        "category": "Indoor",
        "water": "Water when top 2 cm dries; leaves droop slightly when thirsty.",
        "light": "Medium to bright indirect light (no direct sun)",
        "soil": "Rich, moisture-retentive indoor mix with good drainage",
        "flowering": "Elegant white hooded spathes bloom in spring and summer",
        "fruit": "None indoors",
        "harvest": "Snip spent brown bloom stems at the base to encourage new flowers.",
        "tip": "Sensitive to tap water chemicals; use filtered or rested water.",
    },
    {
        "name": "Genovese Basil",
        "scientific": "Ocimum basilicum",
        "category": "Herb",
        "water": "Keep soil evenly moist; water at the base in morning.",
        "light": "Full direct sun (6+ hours daily)",
        "soil": "Fertile, moist, well-draining garden soil",
        "flowering": "Small white flower heads (pinch off to maintain leaf flavor)",
        "fruit": "None",
        "harvest": "Snip top leaves above leaf nodes weekly for fresh culinary pesto.",
        "tip": "Pinching top stems doubles the branch growth.",
    },
    {
        "name": "English Lavender",
        "scientific": "Lavandula angustifolia",
        "category": "Herb",
        "water": "Water deeply only after soil dries out completely.",
        "light": "Full direct sun (6–8 hours daily)",
        "soil": "Lean, sandy or gritty alkaline soil with sharp drainage",
        "flowering": "Fragrant purple flower spikes blooming from late spring to summer",
        "fruit": "Small aromatic seeds",
        "harvest": "Harvest flower stalks when bottom florets open; dry upside down.",
        "tip": "Dislikes high humidity and soggy roots; prune lightly in spring.",
    },
    {
        "name": "Fiddle Leaf Fig",
        "scientific": "Ficus lyrata",
        "category": "Indoor",
        "water": "Water thoroughly when top 5 cm of soil is dry.",
        "light": "Consistent bright filtered light near an east-facing window",
        "soil": "Well-aerated indoor potting mix",
        "flowering": "Does not bloom indoors",
        "fruit": "Non-fruiting indoors",
        "harvest": "Architectural statement tree; wipe broad violin leaves regularly.",
        "tip": "Dislikes drafts, sudden moves, or temperature swings.",
    },
]

PROBLEMS: dict[str, dict[str, Any]] = {
    "Yellowing leaves": {
        "title": "Yellowing leaves",
        "symptoms": "Yellowing can occur on older leaves or across new growth, with many possible causes.",
        "cause": "Watering, drainage, light, nutrient availability, seasonal aging, or other stresses can look similar.",
        "immediate_action": "Check soil moisture and pot drainage. If the soil is wet, allow it to begin drying before watering again.",
        "safe_remedy": "Remove only fully yellowed leaves with clean scissors. Avoid fertilizing while the soil is saturated.",
        "prevention": "Track care changes and observe whether new growth is affected before adjusting one factor at a time.",
    },
    "Brown or crispy edges": {
        "title": "Brown or crispy leaf edges",
        "symptoms": "Leaf tips or margins may become dry, brittle, or discolored.",
        "cause": "Low humidity, inconsistent watering, mineral buildup, strong sun, or other environmental changes may contribute.",
        "immediate_action": "Review recent changes to watering, light, and temperature; check soil moisture before watering.",
        "safe_remedy": "Trim only fully dry tissue with clean scissors if desired. Keep care conditions stable while observing new growth.",
        "prevention": "Avoid sudden changes and keep plants away from strong drafts or heating vents.",
    },
    "Drooping or wilting stems": {
        "title": "Drooping or wilting",
        "symptoms": "Leaves or stems may droop, but the appearance alone does not identify the cause.",
        "cause": "Both dry soil and waterlogged roots can contribute; heat, recent repotting, or other stress may also play a role.",
        "immediate_action": "Check the soil and drainage first. Water gradually if the root zone is dry; pause if it is already wet.",
        "safe_remedy": "Keep the plant in stable conditions and monitor it. Seek local horticultural advice if symptoms persist or worsen.",
        "prevention": "Use a schedule as a reminder to check the soil, not as a substitute for checking its moisture.",
    },
    "White powdery patches": {
        "title": "White or powdery-looking patches",
        "symptoms": "A pale coating or residue may appear on leaves or stems.",
        "cause": "Fungal growth, mineral residue, or other material can look similar; a photograph alone cannot confirm a disease.",
        "immediate_action": "If the patches appear to spread, separate the plant temporarily and inspect both sides of the leaves.",
        "safe_remedy": "Avoid homemade sprays. If the issue persists, consult a local horticultural professional before choosing a treatment.",
        "prevention": "Keep airflow around plants and follow care guidance appropriate to the plant species.",
    },
    "Fine webbing or tiny speckles": {
        "title": "Fine webbing or tiny speckles",
        "symptoms": "Small speckles or fine webbing may be visible on leaves or stems.",
        "cause": "Pests such as mites are one possibility, but dust, other insects, or unrelated leaf stress may look similar.",
        "immediate_action": "Inspect leaf undersides closely. If pests are visible, separate the plant and gently rinse a small area if the plant tolerates it.",
        "safe_remedy": "Use any plant treatment only when appropriate for the plant and strictly according to its label.",
        "prevention": "Inspect plants periodically and avoid applying multiple treatments without confirming the problem.",
    },
    "Soft mushy stem base": {
        "title": "Soft or dark stem base",
        "symptoms": "A stem base may look dark or feel soft, sometimes alongside persistently wet soil.",
        "cause": "Poor drainage and prolonged wet soil can contribute to root problems, but other causes are possible.",
        "immediate_action": "Check soil moisture and drainage. Pause watering while the soil is waterlogged; avoid disturbing roots unless needed.",
        "safe_remedy": "Remove only clearly dead material with clean tools. For a worsening plant, seek local horticultural advice.",
        "prevention": "Use a pot with drainage and check soil moisture before watering.",
    },
}


def go_to(page: str) -> None:
    st.session_state["page"] = page
    st.rerun()


def flash_success(message: str) -> None:
    st.session_state["flash_success"] = message
    st.rerun()


def owner_key() -> str:
    user_id = st.session_state.get("user_id")
    return f"user:{user_id}" if user_id is not None else st.session_state.get("guest_key", "guest:default")


def show_page_title(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="eyebrow">PLANTCARE AI · BOTANICAL SYSTEM</div><h1>{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-note">{subtitle}</p>', unsafe_allow_html=True)


def plant_options(plants: list[dict[str, Any]]) -> tuple[list[str], dict[str, int]]:
    labels = [f'{plant["name"]} · {plant["scientific_name"] or plant["category"]}' for plant in plants]
    return labels, {label: plant["id"] for label, plant in zip(labels, plants)}


def render_welcome() -> None:
    st.markdown(
        """
        <section class="hero">
          <div class="hero-kicker">Botanical Plant Care Reminder System</div>
          <h1>Grow healthy plants<br>with confidence.</h1>
          <p>A beautiful, modern companion to track your plants, remember watering and fertilization schedules, and celebrate every new leaf.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown("### Choose how to start:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="soft-card" style="text-align:center">
              <div style="font-size:2rem">🌿</div>
              <h3>Continue as Guest</h3>
              <p>Instant access with sample plants preloaded. Perfect for exploring or demonstration.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Continue as Guest →", type="primary", use_container_width=True):
            st.session_state["guest_key"] = st.session_state.get(
                "guest_key", f'guest:{st.session_state.setdefault("guest_token", uuid.uuid4().hex)}'
            )
            db.seed_sample_plants(st.session_state["guest_key"])
            st.session_state["user_id"] = None
            go_to("Dashboard")

    with c2:
        st.markdown(
            """
            <div class="soft-card" style="text-align:center">
              <div style="font-size:2rem">🔑</div>
              <h3>Sign In</h3>
              <p>Returning gardener? Access your saved collection and personalized schedules.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Log In to Account", use_container_width=True):
            st.session_state["auth_tab"] = "login"
            go_to("Login / Register")

    with c3:
        st.markdown(
            """
            <div class="soft-card" style="text-align:center">
              <div style="font-size:2rem">📝</div>
              <h3>Register</h3>
              <p>Create a local profile to start your private plant journal and care schedule.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Create Free Account", use_container_width=True):
            st.session_state["auth_tab"] = "register"
            go_to("Login / Register")

    st.write("")
    st.markdown("#### Everything you need for flourishing plants")
    cols = st.columns(3)
    with cols[0]:
        card("Profiles & Care Summaries", "Detailed requirements for watering, light, humidity, flowers, and fruits.", "🪴")
    with cols[1]:
        card("Schedules & Reminders", "Visual countdowns for overdue, due-today, and upcoming care tasks.", "🗓️")
    with cols[2]:
        card("Growth History & Library", "Track heights, milestones, and browse our botanical encyclopedia.", "📈")

    st.caption("PlantCare AI is a local-first botanical prototype. Plant scanner and health analyses are simulated demonstrations.")


def render_auth() -> None:
    show_page_title("Welcome back", "Sign in, create your garden, or explore with a guest profile.")
    show_register_tab = st.session_state.pop("auth_tab", "login") == "register"
    if show_register_tab:
        register_tab, login_tab = st.tabs(["Create account", "Log in"])
    else:
        login_tab, register_tab = st.tabs(["Log in", "Create account"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="e.g. gardener")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)
        if submitted:
            user_id = db.authenticate_user(username, password)
            if user_id is None:
                st.error("We couldn't match that username and password. Please check your credentials.")
            else:
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username.strip()
                st.session_state.pop("guest_key", None)
                db.seed_sample_plants(owner_key())
                st.session_state["flash_success"] = "Welcome back!"
                go_to("Dashboard")

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username", key="register_username", placeholder="At least 3 characters")
            new_password = st.text_input("Create a password", type="password", key="register_password", placeholder="At least 8 characters")
            confirm = st.text_input("Confirm password", type="password", placeholder="Repeat your password")
            registered = st.form_submit_button("Create my account", type="primary", use_container_width=True)
        if registered:
            if len(new_username.strip()) < 3:
                st.error("Please choose a username with at least 3 characters.")
            elif len(new_password) < 8:
                st.error("Please use a secure password with at least 8 characters.")
            elif new_password != confirm:
                st.error("The passwords you entered do not match. Please verify and try again.")
            else:
                try:
                    user_id = db.create_user(new_username, new_password)
                    st.session_state["user_id"] = user_id
                    st.session_state["username"] = new_username.strip()
                    st.session_state.pop("guest_key", None)
                    db.seed_sample_plants(owner_key())
                    st.session_state["flash_success"] = "Your account and starter collection are ready!"
                    go_to("Dashboard")
                except ValueError as exc:
                    st.error(str(exc))

    st.divider()
    st.info("💡 **Quick Guest Exploration**: You can also continue as a guest without creating an account. Sample plants and reminders will be seeded automatically.")
    if st.button("Continue as Guest", type="primary"):
        st.session_state["user_id"] = None
        st.session_state["guest_key"] = f'guest:{st.session_state.setdefault("guest_token", uuid.uuid4().hex)}'
        db.seed_sample_plants(st.session_state["guest_key"])
        go_to("Dashboard")


def render_sidebar() -> str:
    authenticated = st.session_state.get("user_id") is not None
    page_options = (
        ["Welcome", "Login / Register"]
        if not authenticated and "guest_key" not in st.session_state
        else [
            "Dashboard", "My Plants", "Add Plant", "Plant Scanner", "Plant Health",
            "Care Reminders", "Growth Tracking", "Plant Library", "Settings",
        ]
    )
    st.sidebar.markdown("## 🌿 PlantCare AI")
    st.sidebar.caption("BOTANICAL CARE SYSTEM")
    if authenticated:
        st.sidebar.success(f"🌱 Gardener: **{st.session_state.get('username', 'gardener')}**")
    elif "guest_key" in st.session_state:
        st.sidebar.info("🌿 Guest Garden (Demo)")
    st.sidebar.markdown("---")
    desired_page = st.session_state.get("page", page_options[0])
    if desired_page not in page_options:
        desired_page = page_options[0]
        st.session_state["page"] = desired_page
    if st.session_state.get("navigation") not in page_options or st.session_state.get("navigation") != desired_page:
        st.session_state["navigation"] = desired_page

    def sync_navigation() -> None:
        st.session_state["page"] = st.session_state["navigation"]

    selected = st.sidebar.radio(
        "Navigate",
        page_options,
        label_visibility="collapsed",
        key="navigation",
        on_change=sync_navigation,
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Smart Plant Care & Growth Assistant")
    if authenticated or "guest_key" in st.session_state:
        if st.sidebar.button("Log out / Switch profile", use_container_width=True):
            for key in ("user_id", "username", "guest_key", "guest_token", "navigation", "selected_plant_id"):
                st.session_state.pop(key, None)
            st.session_state["page"] = "Welcome"
            st.rerun()
    return selected


def render_dashboard() -> None:
    show_page_title("Your Garden Dashboard", "A serene botanical overview of your plant collection, care schedules, and upcoming tasks.")
    plants = db.list_plants(owner_key())
    reminders = db.list_reminders(owner_key())
    today = date.today()

    urgent = [item for item in reminders if date.fromisoformat(item["next_due"]) <= today]
    due_this_week = [item for item in reminders if date.fromisoformat(item["next_due"]) <= today + timedelta(days=7)]
    needs_attention = sum(plant["health_status"] != "Healthy" for plant in plants)

    # Top Metric Cards
    metrics = st.columns(4)
    metrics[0].metric("Plants in your care", len(plants), "Active collection")
    metrics[1].metric("Looking healthy", len(plants) - needs_attention, "Thriving")
    metrics[2].metric("Need attention", needs_attention, "Check in soon")
    metrics[3].metric("Due for care today", len(urgent), "Watering & feeding")

    st.write("")

    # Plant Cards and Care Summaries (Requirement 4)
    st.markdown("### 🌿 Plant Cards & Care Summaries")
    if not plants:
        st.info("Your garden is waiting for its first plant! Click below to add one or load the plant library.")
    else:
        # Render plant cards in responsive grid columns
        cols = st.columns(min(len(plants), 3))
        for index, plant in enumerate(plants):
            col = cols[index % len(cols)]
            with col:
                photo = image_path(plant["photo_path"])
                with st.container(border=True):
                    if photo:
                        st.image(str(photo), use_container_width=True)
                    else:
                        st.markdown(
                            f'<div style="text-align:center;padding:1.4rem;background:#f0f7f2;border-radius:12px;font-size:2.8rem;margin-bottom:0.75rem">🪴</div>',
                            unsafe_allow_html=True,
                        )

                    st.markdown(f'### {html.escape(plant["name"])}')
                    st.caption(f'*{plant["scientific_name"] or plant["category"]}* · {plant["age_years"]} yr(s)')

                    # Badges
                    health_kind = "good" if plant["health_status"] == "Healthy" else "urgent"
                    st.markdown(
                        f'{badge(plant["health_status"], health_kind)} &nbsp; {badge(plant["growth_stage"], "stage")} &nbsp; {badge(plant["category"], "neutral")}',
                        unsafe_allow_html=True,
                    )
                    st.write("")

                    # Care summaries
                    st.markdown(
                        f'<div style="font-size:0.88rem;color:#20352b;line-height:1.5">'
                        f'💧 <b>Water:</b> {html.escape(plant["watering"] or "As needed")}<br>'
                        f'☀️ <b>Light:</b> {html.escape(plant["sunlight"] or "Bright indirect")}<br>'
                        f'🧪 <b>Feed:</b> {html.escape(plant["fertilizer"] or "Monthly feed")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    # Show reproductive or harvest info if present
                    if plant.get("flowering") and plant["flowering"].lower() not in ("none", "not applicable", ""):
                        st.markdown(f'<div style="font-size:0.82rem;color:#496b56;margin-top:0.35rem">🌸 <b>Bloom:</b> {html.escape(plant["flowering"])}</div>', unsafe_allow_html=True)
                    if plant.get("fruit") and plant["fruit"].lower() not in ("none", "not applicable", ""):
                        st.markdown(f'<div style="font-size:0.82rem;color:#9b4222;margin-top:0.25rem">🍓 <b>Fruit:</b> {html.escape(plant["fruit"])}</div>', unsafe_allow_html=True)
                    if plant.get("harvest") and plant["harvest"].lower() not in ("none", "not applicable", ""):
                        st.markdown(f'<div style="font-size:0.82rem;color:#1e5128;margin-top:0.25rem">✂️ <b>Harvest:</b> {html.escape(plant["harvest"])}</div>', unsafe_allow_html=True)

                    # Next scheduled reminder for this plant
                    plant_reminders = [r for r in reminders if r["plant_id"] == plant["id"]]
                    if plant_reminders:
                        st.write("---")
                        for r in plant_reminders:
                            due = date.fromisoformat(r["next_due"])
                            if due < today:
                                status_badge = badge(f"🚨 {r['kind']} Overdue", "urgent")
                            elif due == today:
                                status_badge = badge(f"⚠️ {r['kind']} Due Today!", "today")
                            else:
                                status_badge = badge(f"🗓️ {r['kind']} in {(due - today).days}d", "good")

                            c_badge, c_btn = st.columns([1.5, 1])
                            c_badge.markdown(f"{status_badge}", unsafe_allow_html=True)
                            if c_btn.button("Done ✓", key=f"dash_complete_{r['id']}", help=f"Mark {r['kind']} done"):
                                db.complete_reminder(owner_key(), r["id"])
                                flash_success(f"{r['kind']} recorded!")

                    # Quick button to open details
                    if st.button(f"View {plant['name']} Profile →", key=f"dash_view_{plant['id']}", use_container_width=True):
                        st.session_state["selected_plant_id"] = plant["id"]
                        go_to("My Plants")

    st.write("")
    st.write("---")

    # Upcoming care and Growth overview
    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        st.subheader("Upcoming Care Schedule")
        if not due_this_week:
            st.success("All caught up! None of your plants are due for water or fertilizer this week.")
        else:
            for item in due_this_week[:6]:
                due = date.fromisoformat(item["next_due"])
                if due < today:
                    status_text = f"🚨 Overdue by {(today - due).days} day(s)"
                    status_kind = "urgent"
                elif due == today:
                    status_text = "⚠️ Due today!"
                    status_kind = "today"
                else:
                    status_text = f"🗓️ Due {due.strftime('%b %d')} (in {(due - today).days} days)"
                    status_kind = "good"

                st.markdown(
                    f'<div class="plant-card">{badge(item["kind"])} &nbsp; <b>{html.escape(item["plant_name"])}</b> &nbsp; {badge(status_text, status_kind)}'
                    f'<div class="muted" style="margin-top:0.35rem">Repeat every {item["interval_days"]} days · Last completed: {item["last_completed"] or "Not yet"}</div></div>',
                    unsafe_allow_html=True,
                )

    with right:
        st.subheader("Quick Actions")
        if st.button("＋ Add New Plant", type="primary", use_container_width=True):
            go_to("Add Plant")
        if st.button("⌕ AI Plant Scanner (Demo)", use_container_width=True):
            go_to("Plant Scanner")
        if st.button("🩺 Plant Health Doctor (Demo)", use_container_width=True):
            go_to("Plant Health")
        if st.button("📚 Browse Plant Library", use_container_width=True):
            go_to("Plant Library")

    st.write("")
    st.subheader("Growth & Height Progress")
    growth = db.list_growth_records(owner_key())
    growth_chart(growth)


def plant_form(plant: dict[str, Any] | None = None, preset: dict[str, str] | None = None) -> None:
    existing = plant or {}
    preset = preset or {}
    with st.form(f'plant_form_{existing.get("id", "new")}', clear_on_submit=False):
        st.markdown("##### 🪴 Basic Botanical Identification")
        c1, c2 = st.columns(2)
        name = c1.text_input("Plant name *", value=existing.get("name", preset.get("name", "")), placeholder="e.g. Monty")
        scientific = c2.text_input("Species / Scientific name", value=existing.get("scientific_name", preset.get("scientific", "")), placeholder="e.g. Monstera deliciosa")

        c3, c4, c5 = st.columns(3)
        category_options = ["Indoor", "Herb", "Flowering", "Vegetable", "Tree", "Succulent", "Other"]
        category_value = existing.get("category", preset.get("category", "Indoor"))
        category = c3.selectbox("Category", category_options, index=category_options.index(category_value) if category_value in category_options else 0)
        age_years = c4.number_input("Age (years)", min_value=0, max_value=200, value=int(existing.get("age_years", 0)), step=1)
        growth_options = ["Seedling", "Vegetative", "Growing", "Flowering", "Fruiting", "Mature", "Dormant"]
        growth_value = existing.get("growth_stage", "Growing")
        growth_stage = c5.selectbox("Growth stage", growth_options, index=growth_options.index(growth_value) if growth_value in growth_options else 2)

        c6, c7 = st.columns(2)
        added_date = c6.date_input(
            "Date added to collection",
            value=date.fromisoformat(existing["added_date"]) if existing.get("added_date") else date.today(),
        )
        health_options = ["Healthy", "Needs attention", "Recovering", "Unknown"]
        health_value = existing.get("health_status", "Healthy")
        health_status = c7.selectbox("Current health status", health_options, index=health_options.index(health_value) if health_value in health_options else 0)

        st.markdown("##### 💧 Environment & Care Routine")
        left, right = st.columns(2)
        watering = left.text_area("Watering needs *", value=existing.get("watering", preset.get("water", "")), placeholder="e.g. Water every 7 days when top 3 cm dry.")
        sunlight = right.text_area("Sunlight requirements", value=existing.get("sunlight", preset.get("light", "")), placeholder="e.g. Bright indirect sunlight, 4-6 hours.")
        humidity = left.text_input("Humidity requirements", value=existing.get("humidity", "Moderate (50-60%)"), placeholder="e.g. Moderate to high humidity")
        soil = right.text_input("Soil & potting mix", value=existing.get("soil", preset.get("soil", "")), placeholder="e.g. Well-draining chunky potting soil")
        fertilizer = left.text_area("Fertilization schedule", value=existing.get("fertilizer", ""), placeholder="e.g. Balanced liquid houseplant fertilizer once monthly.")

        st.markdown("##### 🌸 Flowers, Fruits & Harvest Information")
        flowering = right.text_area("Flowers / Bloom information", value=existing.get("flowering", preset.get("flowering", "")), placeholder="e.g. Produces white blooms in spring, or non-blooming indoor foliage.")
        fruit = left.text_input("Fruit information (where applicable)", value=existing.get("fruit", preset.get("fruit", "")), placeholder="e.g. Produces sweet red cherry tomatoes, or none.")
        harvest = right.text_area("Harvest information (where applicable)", value=existing.get("harvest", preset.get("harvest", "")), placeholder="e.g. Harvest leaves from top down; prune dead leaves at base.")

        st.markdown("##### 📸 Plant Photograph")
        photo = st.file_uploader("Upload a plant photograph (optional)", type=["png", "jpg", "jpeg", "webp"])

        submitted = st.form_submit_button("Save plant" if plant is None else "Save changes", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter a plant name to identify it in your garden.")
            return
        photo_path = existing.get("photo_path", "")
        if photo is not None:
            try:
                photo_path = save_uploaded_image(photo)
            except ValueError as exc:
                st.error(str(exc))
                return
        data = {
            "name": name.strip(), "scientific_name": scientific.strip(), "category": category,
            "age_years": int(age_years), "added_date": added_date.isoformat(),
            "growth_stage": growth_stage, "health_status": health_status, "watering": watering.strip(),
            "sunlight": sunlight.strip(), "humidity": humidity.strip(), "soil": soil.strip(),
            "fertilizer": fertilizer.strip(), "flowering": flowering.strip(), "fruit": fruit.strip(),
            "harvest": harvest.strip(), "photo_path": photo_path,
        }
        db.save_plant(owner_key(), data, existing.get("id"))
        flash_success(f"🌱 '{name.strip()}' has been saved successfully in your collection!")


def render_my_plants() -> None:
    show_page_title("My Plants", "Explore your personal collection, review care summaries, and view individual plant profiles.")
    plants = db.list_plants(owner_key())
    if not plants:
        st.info("Your collection is currently empty. Add a plant or explore the sample library to get started.")
        if st.button("Add my first plant", type="primary"):
            go_to("Add Plant")
        return

    search = st.text_input("🔍 Search your collection", placeholder="Filter by plant name, species, category, or care note…")
    filtered = [plant for plant in plants if search.casefold() in " ".join(str(value) for value in plant.values()).casefold()]
    st.caption(f"Showing {len(filtered)} of {len(plants)} plants")

    labels, plant_ids = plant_options(filtered)
    if not labels:
        st.info("No plants match that search term.")
        return

    # Check if a specific plant was selected from dashboard
    selected_idx = 0
    if "selected_plant_id" in st.session_state:
        target_id = st.session_state.pop("selected_plant_id")
        for idx, (lbl, pid) in enumerate(plant_ids.items()):
            if pid == target_id:
                selected_idx = idx
                break

    selected_label = st.selectbox("Select plant profile to view", labels, index=selected_idx)
    plant = db.get_plant(owner_key(), plant_ids[selected_label])
    if plant is None:
        st.error("That plant could not be found.")
        return

    st.write("")
    photo = image_path(plant["photo_path"])
    image_col, details_col = st.columns([0.75, 1.25], gap="large")

    with image_col:
        if photo:
            st.image(str(photo), use_container_width=True)
        else:
            st.markdown(
                '<div class="soft-card" style="text-align:center;padding:3.5rem 1.5rem;background:#f0f7f2;border-radius:16px"><div style="font-size:3.5rem">🪴</div><p class="muted" style="margin-top:0.5rem">Photograph not yet uploaded.<br>Edit this plant to add one.</p></div>',
                unsafe_allow_html=True,
            )

    with details_col:
        st.markdown(f'## {html.escape(plant["name"])}')
        health_kind = "good" if plant["health_status"] == "Healthy" else "urgent"
        st.markdown(
            f'{badge(plant["health_status"], health_kind)} &nbsp; {badge(plant["category"], "neutral")} &nbsp; {badge(plant["growth_stage"], "stage")}',
            unsafe_allow_html=True,
        )
        st.caption(f'**Species:** *{plant["scientific_name"] or "Not specified"}* · Added {plant["added_date"]}')
        st.markdown(f'**Age:** {plant["age_years"]} year(s)')

        st.markdown("#### 🌿 Care Profile")
        c_care1, c_care2 = st.columns(2)
        with c_care1:
            st.markdown(f'💧 **Watering:** {plant["watering"] or "Not specified"}')
            st.markdown(f'☀️ **Sunlight:** {plant["sunlight"] or "Not specified"}')
            st.markdown(f'💨 **Humidity:** {plant["humidity"] or "Not specified"}')
        with c_care2:
            st.markdown(f'🪴 **Soil:** {plant["soil"] or "Not specified"}')
            st.markdown(f'🧪 **Fertilizer:** {plant["fertilizer"] or "Not specified"}')

        st.markdown("#### 🌸 Flowers, Fruits & Harvest")
        c_rep1, c_rep2, c_rep3 = st.columns(3)
        with c_rep1:
            st.markdown(f'🌸 **Flowers:**  \n{plant["flowering"] or "None / not applicable"}')
        with c_rep2:
            st.markdown(f'🍓 **Fruits:**  \n{plant["fruit"] or "None / not applicable"}')
        with c_rep3:
            st.markdown(f'✂️ **Harvest:**  \n{plant["harvest"] or "None / ornamental"}')

    st.write("")
    edit_tab, delete_tab = st.tabs(["✏️ Edit Plant Profile", "🗑️ Remove Plant"])
    with edit_tab:
        plant_form(plant)
    with delete_tab:
        st.warning(f"⚠️ Deleting '{plant['name']}' will permanently remove it along with all its reminders and growth logs.")
        confirmed = st.checkbox(f"I understand; permanently delete '{plant['name']}.", key=f'confirm_delete_{plant["id"]}')
        if st.button("Delete this plant", disabled=not confirmed, type="primary"):
            db.delete_plant(owner_key(), plant["id"])
            flash_success("Plant removed from your garden.")


def render_add_plant(preset: dict[str, str] | None = None) -> None:
    show_page_title("Add a Plant", "Welcome a new plant into your garden and configure its personalized care routine.")
    plant_form(preset=preset)


def render_scanner() -> None:
    show_page_title("Plant Scanner", "Upload a plant photograph and explore an interactive botanical identification demonstration.")

    # Prominent demonstration notice (Requirement 7)
    st.markdown(
        """
        <div class="demo-banner">
          <b>🧪 DEMONSTRATION MODE ONLY</b> · No plant-identification model is connected.
          Uploads are shown for preview only; the sample profile is selected manually and is not inferred from the photograph.
          No identification or confidence score is generated.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_scan, right_scan = st.columns([1, 1], gap="large")

    with left_scan:
        st.markdown("#### 1. Upload Plant Photograph")
        uploaded = st.file_uploader("Upload leaf or flower image", type=["png", "jpg", "jpeg", "webp"], key="scanner_photo")

        if uploaded is not None:
            try:
                st.image(uploaded, caption="Your uploaded photograph (Demo Input)", use_container_width=True)
            except (UnidentifiedImageError, OSError, ValueError) as exc:
                st.error(f"Could not load image file: {exc}")
                return

        st.markdown("#### 2. Or Select Demonstration Preset")
        demo_names = [item["name"] for item in LIBRARY]
        selected = st.selectbox("Choose sample botanical match to inspect", demo_names)

    item = next(plant for plant in LIBRARY if plant["name"] == selected)

    with right_scan:
        st.markdown("#### 3. Sample Plant Profile")

        with st.container(border=True):
            st.markdown(
                f'<h2 style="margin:0">🌿 {html.escape(item["name"])}</h2>'
                f'{badge("Sample profile · not identified", "neutral")}',
                unsafe_allow_html=True,
            )
            st.caption(f'*{item["scientific"]}* · Category: {item["category"]}')

            st.info("This care profile comes from the sample library. The uploaded photograph has not been analyzed.")

            st.write("---")
            st.markdown("##### 💧 Care Profile")
            st.markdown(f'• **Water:** {html.escape(item["water"])}')
            st.markdown(f'• **Light:** {html.escape(item["light"])}')
            st.markdown(f'• **Soil:** {html.escape(item["soil"])}')
            if item.get("flowering"):
                st.markdown(f'• **Flowers:** {html.escape(item["flowering"])}')
            if item.get("fruit"):
                st.markdown(f'• **Fruits:** {html.escape(item["fruit"])}')
            if item.get("harvest"):
                st.markdown(f'• **Harvest Tips:** {html.escape(item["harvest"])}')

            st.markdown(f'<div class="tip-box">💡 <b>Growing Tip:</b> {html.escape(item["tip"])}</div>', unsafe_allow_html=True)

            if st.button("＋ Save Sample Plant to My Collection", type="primary", use_container_width=True):
                st.session_state["plant_preset"] = item
                go_to("Add Plant")


def render_health() -> None:
    show_page_title("Plant Health Guide", "Review common signs and cautious first steps. This page does not diagnose plant disease.")

    st.markdown(
        """
        <div class="demo-banner">
          <b>⚠️ GENERAL GUIDANCE ONLY</b> · Uploaded photographs are displayed for reference and are not analyzed.
          The possible causes below are not diagnoses; similar signs can have different explanations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_img, col_diag = st.columns([0.8, 1.2], gap="large")

    with col_img:
        st.markdown("#### Reference Photograph (Not Analyzed)")
        uploaded = st.file_uploader("Upload leaf photo for reference only", type=["png", "jpg", "jpeg", "webp"], key="health_photo")
        if uploaded:
            try:
                st.image(uploaded, caption="Reference photograph — no automated analysis", use_container_width=True)
            except (UnidentifiedImageError, OSError, ValueError) as exc:
                st.error(f"Could not load image: {exc}")
                return
        else:
            st.markdown(
                '<div class="soft-card" style="text-align:center;padding:2.5rem 1rem;background:#f8faf8;border-radius:14px"><div style="font-size:2.5rem">🩺</div><p class="muted">Upload a photo above to compare symptoms side-by-side with our botanical health guide.</p></div>',
                unsafe_allow_html=True,
            )

    with col_diag:
        st.markdown("#### Choose a sign to explore")
        concern = st.selectbox("What are you noticing?", list(PROBLEMS))
        info = PROBLEMS[concern]

        with st.container(border=True):
            st.markdown(f'### 🌿 {info["title"]}')
            st.markdown(f'**Common signs:** {info["symptoms"]}')
            st.write("---")

            st.markdown(f'🔍 **Possible contributing factors (not a diagnosis):**  \n{info["cause"]}')
            st.markdown(f'⚡ **A cautious first step:**  \n{info["immediate_action"]}')
            st.markdown(f'🌿 **General care guidance:**  \n{info["safe_remedy"]}')
            st.markdown(f'🛡️ **Monitoring:**  \n{info["prevention"]}')

    st.write("")
    st.markdown("#### 📋 General Plant-Care Checklist")
    st.markdown(
        "- Check soil moisture and pot drainage before changing watering.\n"
        "- If pests or spreading spots are visible, consider separating the plant while you seek advice.\n"
        "- Make one care change at a time and observe new growth.\n"
        "- For persistent or rapidly worsening problems, consult a local horticulture professional.\n"
        "- Follow product labels and test any treatment on a small area when appropriate."
    )
    st.caption("This reference is not an expert diagnosis. PlantCare AI does not determine diseases from uploaded images.")


def render_reminders() -> None:
    show_page_title("Care Reminders & Schedules", "Keep your garden thriving with clear watering and fertilization reminders.")
    plants = db.list_plants(owner_key())
    if not plants:
        st.info("Please add a plant before setting up care schedules.")
        return

    labels, plant_ids = plant_options(plants)
    reminders = db.list_reminders(owner_key())
    today = date.today()

    overdue_count = sum(1 for r in reminders if date.fromisoformat(r["next_due"]) < today)
    today_count = sum(1 for r in reminders if date.fromisoformat(r["next_due"]) == today)
    upcoming_count = sum(1 for r in reminders if date.fromisoformat(r["next_due"]) > today)

    # Reminders summary metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Schedules", len(reminders))
    m2.metric("Overdue Tasks", overdue_count, "Needs immediate care" if overdue_count else "None")
    m3.metric("Due Today", today_count, "Care today" if today_count else "None")
    m4.metric("Upcoming (Next 30d)", upcoming_count, "On track")

    st.write("")

    # Filter Tabs
    tab_all, tab_urgent, tab_new = st.tabs(["📋 All Scheduled Reminders", "⚠️ Overdue & Due Today", "➕ Add / Edit Schedule"])

    with tab_all:
        if not reminders:
            st.info("No care schedules set up yet. Create one below!")
        else:
            for reminder in reminders:
                due = date.fromisoformat(reminder["next_due"])
                if due < today:
                    status_text = f"🚨 Overdue by {(today - due).days} day(s)"
                    status_kind = "urgent"
                elif due == today:
                    status_text = "⚠️ Due today!"
                    status_kind = "today"
                else:
                    status_text = f"🗓️ Due {due.strftime('%b %d, %Y')} (in {(due - today).days}d)"
                    status_kind = "good"

                with st.container(border=True):
                    c_title, c_details, c_action = st.columns([1.5, 2, 1])
                    c_title.markdown(f'**{reminder["plant_name"]}**  \n{badge(reminder["kind"], "neutral")}', unsafe_allow_html=True)
                    c_details.markdown(
                        f'{badge(status_text, status_kind)} &nbsp; <span class="muted">Repeat every {reminder["interval_days"]} days</span><br>'
                        f'<span class="muted" style="font-size:0.8rem">Last completed: {reminder["last_completed"] or "Not recorded yet"}</span>',
                        unsafe_allow_html=True,
                    )
                    if c_action.button("Mark Done ✓", key=f'complete_all_{reminder["id"]}', type="primary", use_container_width=True):
                        db.complete_reminder(owner_key(), reminder["id"])
                        flash_success(f"{reminder['kind']} logged for {reminder['plant_name']}! Next due date updated.")

    with tab_urgent:
        urgent_items = [r for r in reminders if date.fromisoformat(r["next_due"]) <= today]
        if not urgent_items:
            st.success("🎉 Great job! You have zero overdue care tasks today.")
        else:
            for reminder in urgent_items:
                due = date.fromisoformat(reminder["next_due"])
                status_text = f"🚨 Overdue by {(today - due).days} day(s)" if due < today else "⚠️ Due today!"
                status_kind = "urgent" if due < today else "today"

                with st.container(border=True):
                    c_title, c_details, c_action = st.columns([1.5, 2, 1])
                    c_title.markdown(f'**{reminder["plant_name"]}**  \n{badge(reminder["kind"], "neutral")}', unsafe_allow_html=True)
                    c_details.markdown(
                        f'{badge(status_text, status_kind)} &nbsp; Every {reminder["interval_days"]} days',
                        unsafe_allow_html=True,
                    )
                    if c_action.button("Complete Now ✓", key=f'complete_urg_{reminder["id"]}', type="primary", use_container_width=True):
                        db.complete_reminder(owner_key(), reminder["id"])
                        flash_success("Care recorded!")

    with tab_new:
        st.markdown("#### Set or Adjust a Care Schedule")
        with st.form("reminder_form"):
            selected = st.selectbox("Choose Plant", labels)
            kind = st.selectbox("Care Task", ["Watering", "Fertilizing"])
            interval = st.number_input("Repeat every (days)", min_value=1, max_value=365, value=7 if kind == "Watering" else 30, step=1)
            next_due = st.date_input("Next scheduled due date", value=today)
            saved = st.form_submit_button("Save Schedule", type="primary")

        if saved:
            db.update_reminder(owner_key(), plant_ids[selected], kind, int(interval), next_due.isoformat())
            flash_success(f"Schedule saved! {selected.split(' · ')[0]} will be reminded every {int(interval)} days.")

    st.caption("Reminders appear inside the application. No external emails or push notifications are sent.")


def render_growth() -> None:
    show_page_title("Growth Tracking & Journal", "Record plant measurements, track growth milestones, and celebrate every new leaf.")
    plants = db.list_plants(owner_key())
    if not plants:
        st.info("Add a plant to your garden before logging growth observations.")
        return

    labels, plant_ids = plant_options(plants)

    with st.expander("➕ Log New Growth Observation", expanded=True):
        with st.form("growth_form"):
            c1, c2, c3 = st.columns(3)
            selected = c1.selectbox("Plant observed", labels)
            observed_on = c2.date_input("Observation date", value=date.today())
            height = c3.number_input("Height in cm (optional; 0 if not measured)", min_value=0.0, max_value=100_000.0, value=0.0, step=0.5)

            notes = st.text_area("Milestone & observation notes", placeholder="e.g. Unfurled a new leaf with 4 fenestrations, repotted into terracotta pot, or first flower bloom…")
            photo = st.file_uploader("Progress photograph (optional)", type=["png", "jpg", "jpeg", "webp"], key="growth_photo")
            submitted = st.form_submit_button("Save Observation", type="primary")

        if submitted:
            photo_path = ""
            if photo is not None:
                try:
                    photo_path = save_uploaded_image(photo)
                except ValueError as exc:
                    st.error(str(exc))
                    return
            db.add_growth_record(
                owner_key(), plant_ids[selected], observed_on.isoformat(),
                float(height) if height > 0 else None, notes.strip(), photo_path,
            )
            flash_success("Growth observation saved successfully!")

    st.write("")
    st.markdown("#### 📈 Height Growth Progression Chart")
    records = db.list_growth_records(owner_key())
    growth_chart(records)

    st.write("")
    st.markdown("#### 📜 Growth Journal History")
    if not records:
        st.info("No growth observations recorded yet. Log your first measurement above!")
        return

    for record in reversed(records):
        with st.container(border=True):
            date_col, plant_col, height_col = st.columns([1, 2, 1])
            date_col.write(f'🗓️ **{record["observation_date"]}**')
            plant_col.write(f'🌿 **{record["plant_name"]}**')
            height_col.write(f'📏 {record["height_cm"]:g} cm' if record["height_cm"] is not None else "Height not measured")
            if record["notes"]:
                st.markdown(f'<div class="tip-box" style="margin-top:0.4rem">{html.escape(record["notes"])}</div>', unsafe_allow_html=True)

    photos = [record for record in records if record["photo_path"]]
    if photos:
        st.write("")
        st.markdown("#### 📸 Progress Photo Gallery")
        cols = st.columns(min(len(photos), 3))
        for index, record in enumerate(photos):
            path = image_path(record["photo_path"])
            if path:
                cols[index % len(cols)].image(str(path), caption=f'{record["plant_name"]} · {record["observation_date"]}', use_container_width=True)


def render_library() -> None:
    show_page_title("Botanical Plant Library", "Explore 10+ popular indoor and outdoor plants with complete care guidelines.")

    c_search, c_filter = st.columns([2, 1])
    search = c_search.text_input("Find a plant", placeholder="Search by name, category, or care need (e.g. 'Herb', 'Pothos', 'Tomato')…")
    cat_filter = c_filter.selectbox("Category filter", ["All Categories", "Indoor", "Herb", "Vegetable", "Succulent"])

    matches = [
        plant for plant in LIBRARY
        if (cat_filter == "All Categories" or plant["category"] == cat_filter)
        and (not search.strip() or search.casefold() in " ".join(plant.values()).casefold())
    ]
    st.caption(f"Showing {len(matches)} botanical profiles")

    if not matches:
        st.info("No plants found matching those terms. Try a broader search.")
        return

    for start in range(0, len(matches), 2):
        cols = st.columns(2)
        for col, plant in zip(cols, matches[start:start + 2]):
            with col:
                with st.container(border=True):
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;align-items:center">'
                        f'<h3 style="margin:0">🌿 {html.escape(plant["name"])}</h3>'
                        f'{badge(plant["category"], "neutral")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.caption(f'*{plant["scientific"]}*')
                    st.markdown(
                        f'💧 **Water:** {plant["water"]}<br>'
                        f'☀️ **Light:** {plant["light"]}<br>'
                        f'🪴 **Soil:** {plant["soil"]}',
                        unsafe_allow_html=True,
                    )
                    if plant.get("flowering"):
                        st.markdown(f'🌸 **Flowers:** {plant["flowering"]}')
                    if plant.get("fruit"):
                        st.markdown(f'🍓 **Fruits:** {plant["fruit"]}')
                    if plant.get("harvest"):
                        st.markdown(f'✂️ **Harvest:** {plant["harvest"]}')

                    st.markdown(f'<div class="tip-box">💡 {plant["tip"]}</div>', unsafe_allow_html=True)

                    if st.button(f"＋ Add {plant['name']} to My Garden", key=f'library_add_{plant["name"]}', use_container_width=True):
                        st.session_state["plant_preset"] = plant
                        go_to("Add Plant")


def render_settings() -> None:
    show_page_title("Settings & Architecture", "Session management, local data storage details, and cloud persistence notes.")

    st.markdown("#### 👤 Current Gardener Profile")
    if st.session_state.get("user_id") is not None:
        st.write(f'Authenticated Account: **{st.session_state.get("username", "Gardener")}**')
        st.caption("Your plants, schedules, and care notes are stored in the local SQLite database.")
    else:
        st.write("Current Session: **Guest Gardener**")
        st.caption("Guest data is stored locally with a temporary session key. Pre-seeded sample plants are ready for demonstration.")

    st.write("---")
    st.markdown("#### 🗄️ SQLite Database & Cloud Persistence (Architecture Notice)")
    st.markdown(
        """
        PlantCare AI is designed with a **local-first architecture**:
        - **Local Storage**: All users, plant profiles, reminders, and growth notes reside in `plantcare.db`.
        - **Photographs**: Stored locally as optimized JPEGs in the `uploads/` directory.
        - **Security**: Passwords are cryptographically salted and hashed using PBKDF2-HMAC-SHA256 (310,000 iterations).

        > [!IMPORTANT]
        > **Streamlit Community Cloud Storage Limitation**:
        > Streamlit Community Cloud runs apps inside ephemeral container instances. When an app rebuilds or restarts after inactivity, local files (including SQLite `.db` files and local `uploads/`) reset to their Git repository state.
        >
        > **Production Cloud Migration**:
        > For permanent multi-user cloud persistence, connect PlantCare AI to a managed cloud database (e.g. **PostgreSQL on Supabase, Neon, or Google Cloud SQL**) and durable object storage (e.g. **Google Cloud Storage / AWS S3**) by setting connection credentials in `st.secrets`.
        """
    )
    st.markdown("Local database path on this machine:")
    st.code(str(db.DB_PATH), language=None)

    st.write("---")
    st.markdown("#### 🔒 Authentication & Disclaimers")
    st.markdown(
        "- **Demonstration AI**: The Plant Scanner and Plant Health Doctor features are explicitly labeled simulated demonstrations for UI presentation.\n"
        "- **Authentication**: Passwords use salted PBKDF2 hashes, but this prototype has no password reset, email verification, login throttling, or production session controls.\n"
        "- **In-App Reminders**: Care notifications are displayed directly within the web app dashboard and reminder list; no external push or email servers are required."
    )

    st.write("")
    if st.button("Log Out / Reset Session", type="primary"):
        for key in ("user_id", "username", "guest_key", "guest_token", "navigation", "selected_plant_id"):
            st.session_state.pop(key, None)
        st.session_state["page"] = "Welcome"
        st.rerun()


def main() -> None:
    page = render_sidebar()
    message = st.session_state.pop("flash_success", None)
    if message:
        st.success(message)
    if page == "Welcome":
        render_welcome()
    elif page == "Login / Register":
        render_auth()
    elif page == "Dashboard":
        if "guest_key" not in st.session_state and st.session_state.get("user_id") is None:
            go_to("Welcome")
        db.seed_sample_plants(owner_key())
        render_dashboard()
    elif page == "My Plants":
        render_my_plants()
    elif page == "Add Plant":
        preset = st.session_state.pop("plant_preset", None)
        render_add_plant(preset)
    elif page == "Plant Scanner":
        render_scanner()
    elif page == "Plant Health":
        render_health()
    elif page == "Care Reminders":
        render_reminders()
    elif page == "Growth Tracking":
        render_growth()
    elif page == "Plant Library":
        render_library()
    elif page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()
