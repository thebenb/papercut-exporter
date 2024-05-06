from papercut_exporter import app
from waitress import serve
import json
import requests

config = None
VERSION = "1.1.0"


# Load configuration from config.json when the application starts
def load_configuration():
    global config
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Configuration file 'config.json' not found.")
        config = None


# Check GitHub for new release
def check_github_for_new_release():
    try:

        # Make a GET request to the GitHub releases API
        response = requests.get(
            f"https://api.github.com/repos/thebenb/papercut-exporter/releases/latest"
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response JSON
        release_data = response.json()
        latest_version = release_data["tag_name"]  # Get the latest release version

        return latest_version

    except Exception as e:
        print(f"Error checking for new release: {e}")
        return None


if __name__ == "__main__":
    load_configuration()  # Load configuration when the application starts

    # Check for new release on GitHub
    latest_version = check_github_for_new_release()
    if latest_version:
        if latest_version != VERSION:
            print(
                f"A new version ({latest_version}) is available. Please consider updating."
            )
        else:
            print(f"You are running the latest version: {latest_version}")

    if config:
        port = config.get("port", 8000)
        print(f"Running on port: {port}")
        serve(app, host="0.0.0.0", port=config.get("port"))
    else:
        print("Configuration not loaded. Exiting...")
