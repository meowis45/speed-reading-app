import streamlit.web.cli as stcli
import os, sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app_path = get_resource_path("app.py")
    
    # Check if app.py actually exists where we think it is
    if not os.path.exists(app_path):
        print(f"Error: Could not find app.py at {app_path}")
        sys.exit(1)

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.port=8501",
        "--server.address=localhost",
    ]
    sys.exit(stcli.main())
