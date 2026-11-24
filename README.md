# PlantCare AI – Plant Care Reminder System

A complete, beginner-friendly Python web application built with **Streamlit** featuring a botanical interface in forest green, light green, and soft white. PlantCare AI helps gardeners manage plant care routines, track growth milestones, and stay on top of watering and fertilization schedules.

---

## 🌿 Key Features

1. **Botanical Interface**: Responsive UI themed in forest green (`#143b2c`, `#23744f`), light sage (`#e7f2e9`, `#b9dca7`), and soft white (`#f6faf6`).
2. **Welcome Landing & Authentication**:
   - **Continue as Guest**: 1-click access with sample plants preloaded for immediate demonstration.
   - **Log In & Register**: Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes.
3. **Garden Dashboard**:
   - Live metrics (Total Plants, Healthy Plants, Attention Needed, Due Today).
   - Responsive **Plant Cards & Care Summaries** with quick-action care buttons (`Mark Watered`).
   - Upcoming care reminders list and SVG height growth trend chart.
4. **Comprehensive Plant Profiles (CRUD)**:
   - Full botanical records: Plant Name, Species (scientific name), Category, Age, Growth Stage, Health Status.
   - Environmental care needs: Watering schedule, Sunlight, Humidity, Soil, Fertilization.
   - Reproductive & harvest information: Flowering details, Fruit development, and Harvest tips.
   - Plant photograph upload (stored locally and optimized).
   - Edit and delete plants with safety confirmation checks.
5. **Plant Scanner Demonstration (No AI Model)**:
   - Upload a photograph for preview and manually select a sample plant profile.
   - The image is not analyzed; no plant identification or confidence score is produced.
   - 1-click "Save Sample Plant to My Collection".
6. **Plant Health Guide (Not a Diagnosis)**:
   - Reference guidance for common leaf and pest-related signs.
   - Uploaded photographs are displayed only and are not analyzed.
   - Possible causes and cautious next steps are not diagnoses; consult a local horticulture professional for persistent problems.
7. **Care Reminders & Schedules**:
   - Overdue (red alert), Due Today (amber tag), and Upcoming (green badge) countdowns.
   - 1-click "Mark Complete" which logs the care event and recalculates the next due date.
   - Custom schedule builder for watering and fertilization intervals.
8. **Growth Tracking & Journal**:
   - Log observations: date, height in cm, milestone notes, and progress photos.
   - Responsive SVG growth height line chart.
   - Historical progress photo gallery.
9. **Curated Plant Library**:
   - Browse 10+ popular houseplants, herbs, and vegetables.
   - Filter by category and search by care needs.
   - 1-click "Add to My Garden" pre-fills the new plant form.
10. **Pre-seeded Sample Plants**:
    - Preloaded with Tulsi, Money Plant, and Cherry Tomato examples and related care schedules.

## Prototype limitations

- Authentication is for a local demonstration only. Although passwords are salted and hashed, there is no password reset, email verification, rate limiting, or production-grade session security.
- Guest collections use a temporary session key. Local files and SQLite data persist on this computer, but Community Cloud's local filesystem is ephemeral.
- Care reminders are shown in the app only; no external email or push notifications are sent.
- The scanner and health guide do not identify plants or diagnose diseases. Do not treat their sample data as image-based analysis or professional advice.

---

## 🗄️ Architecture & Cloud Persistence Notes

- **Local Persistence**: Uses SQLite (`plantcare.db`) with foreign key constraints, normalized tables, and transactions.
- **Image Storage**: Normalized JPEG uploads stored locally in the `uploads/` directory.

> [!IMPORTANT]
> **Streamlit Community Cloud Storage Limitation**:
> Streamlit Community Cloud runs in ephemeral container instances. When an app sleeps, rebuilds, or restarts, local files (including SQLite `.db` files and local `uploads/`) reset to their initial Git repository state.
>
> **Production Cloud Migration**:
> To deploy permanently for multiple cloud users:
> 1. Replace SQLite with a managed relational database such as **PostgreSQL** (e.g. Supabase, Neon, or Google Cloud SQL).
> 2. Store user-uploaded photos in an object storage bucket (e.g. **AWS S3** or **Google Cloud Storage**).
> 3. Store database and storage credentials securely using Streamlit Secrets (`st.secrets`).

---

## 🚀 How to Launch Locally

### 1. Requirements
- Python 3.10 to 3.15.
- PowerShell or Terminal.

### 2. Create Virtual Environment & Install Dependencies
Open PowerShell in the project directory:

```powershell
# Create dedicated virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Application
Launch Streamlit:

```powershell
streamlit run app.py
```

The browser will automatically open at `http://localhost:8501`.

### 4. Running the Automated Test Suite
To verify database integrity and application routes:

```powershell
python -m unittest discover -s tests -v
```

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this project folder to your GitHub repository:
   ```powershell
   git init
   git add app.py database.py components tests sample_data.py styles.py requirements.txt README.md .gitignore .streamlit uploads
   git commit -m "Initial commit of PlantCare AI"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/PlantCareAI.git
   git push -u origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io).
3. Click **Create app** and select your repository, branch (`main`), and set the main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud will install packages from `requirements.txt` and launch the app.

---

## 📁 Project Structure

```
PlantCareAI/
├── .streamlit/
│   └── config.toml           # Botanical theme colors & server config
├── components/
│   ├── __init__.py
│   └── ui.py                 # Botanical styling, badges, cards & SVG chart
├── tests/
│   ├── __init__.py
│   ├── test_app.py           # App integration & constant tests
│   └── test_database.py      # Database CRUD, auth & lifecycle tests
├── uploads/
│   └── .gitkeep              # Directory for uploaded plant photographs
├── .gitignore                # Excludes DB, virtual environments & uploads
├── app.py                    # Main Streamlit web application
├── database.py               # SQLite database access & seeding layer
├── sample_data.py            # Botanical reference and manually selected demo profiles
├── styles.py                 # Additional botanical CSS reference
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation & run guide
```
