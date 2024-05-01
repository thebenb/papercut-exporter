from papercut_exporter import app
from waitress import serve
import json

config = None


# Load configuration from config.json when the application starts
def load_configuration():
    global config
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Configuration file 'config.json' not found.")
        config = None


if __name__ == "__main__":
    load_configuration()  # Load configuration when the application starts
    if config:
        port = config.get("port", 8000)
        serve(app, host="0.0.0.0", port=config.get("port"))
    else:
        print("Configuration not loaded. Exiting...")
