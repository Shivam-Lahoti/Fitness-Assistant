import os
import sys
import streamlit.web.bootstrap

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the entry point for Streamlit
if __name__ == "__main__":
    # Run the Streamlit app
    streamlit.web.bootstrap.run(["Application/app.py"], command_line_args=[])
