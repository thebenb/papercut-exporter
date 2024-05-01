from papercut_exporter import app
from waitress import serve

if __name__ == "__main__":
    # For Waitress WSGI server
    serve(app, host="0.0.0.0", port=8000)
