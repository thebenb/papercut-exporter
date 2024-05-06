import json
import requests
from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest, Counter

app = Flask(__name__)


# Load configuration from config.json
def load_configuration():
    try:
        with open("config.json") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Configuration file 'config.json' not found.")
        return None


# Fetch metrics from URLs specified in the config
def fetch_metrics(config):
    all_metrics = {}
    for url in config.get("urls", []):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            metrics_json = response.json()
            all_metrics[url] = flatten_dict(metrics_json)
        except Exception as e:
            print(f"Error fetching metrics from {url}: {e}")
    return all_metrics


# Flatten nested dictionaries
def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, (int, float)):
            items.append((new_key, float(v)))
        elif isinstance(v, str) and "." in v:  # Check if the value contains a dot
            continue  # Skip this key-value pair
        else:
            items.append((new_key, str(v)))  # Treat non-numeric values as strings
    return dict(items)


def convert_to_prometheus_format(metrics):
    registry = CollectorRegistry()
    for url, flattened_metrics in metrics.items():
        for metric_name, value in flattened_metrics.items():
            if metric_name != "comment":  # Exclude comment metrics
                # Convert camelCase metric name to snake_case
                snake_case_name = metric_name.replace(" ", "_").lower()
                # Remove _count suffix if present
                if snake_case_name.endswith("_count"):
                    snake_case_name = snake_case_name[:-6]
                # Check if value is numeric
                if isinstance(value, (int, float)):
                    metric = Gauge(
                        snake_case_name, "", registry=registry
                    )  # No description
                    metric.set(value)
                else:
                    # If value is not numeric, treat it as a label
                    metric = Counter(
                        snake_case_name, "", ["value"], registry=registry
                    )  # No description
                    metric.labels(value).inc()
    return generate_latest(registry)


@app.route("/metrics")
def metrics():
    config = load_configuration()
    papercut_metrics = fetch_metrics(config)
    prometheus_metrics = convert_to_prometheus_format(papercut_metrics)
    return Response(prometheus_metrics, mimetype="text/plain")


if __name__ == "__main__":
    config = load_configuration()
    if config:
        app.run(host="0.0.0.0", port=config.get("port"))
    else:
        print("Exiting due to missing configuration.")
