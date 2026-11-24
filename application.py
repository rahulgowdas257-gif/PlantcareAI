"""
PlantCare AI - Plant Care Reminder System Launcher
To launch directly via Streamlit:
    streamlit run app.py
"""
import sys
import subprocess

if __name__ == "__main__":
    print("🌿 Welcome to PlantCare AI – Plant Care Reminder System!")
    print("Launching Streamlit application at http://localhost:8501 ...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\nPlantCare AI stopped. Happy gardening!")
