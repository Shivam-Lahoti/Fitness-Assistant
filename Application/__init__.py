import os
import sys
import streamlit.web.bootstrap

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Entry point for the Streamlit app
if __name__ == "__main__":
    # Provide the path to your app.py file
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

    # Run the Streamlit app
    streamlit.web.bootstrap.run(
        app_path,  # Path to the app.py file
        command_line=f"streamlit run {app_path}",
        args=[],  # Additional arguments (empty)
        flag_options={}  # Additional flags (empty)
    )
