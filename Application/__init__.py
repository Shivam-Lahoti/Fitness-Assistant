import os
import subprocess

if __name__ == "__main__":
    # Get the absolute path to app.py
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

    # Run Streamlit via subprocess
    subprocess.run(["streamlit", "run", app_path])
