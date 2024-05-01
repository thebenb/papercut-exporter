import json
from flask import Flask, Response
from Metric import Metric
import requests
import re

app = Flask(__name__)


# Load configuration from config.json
def load_configuration():
    try:
        with open("config.json") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Configuration file 'config.json' not found.")
        return None


def fetch_metrics(config):
    urls = config.get("urls", [])
    all_metrics = {}
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            metrics_json = response.json()

            # Process metrics and comments
            metrics = {}
            comments = {}
            for metric_name, value in metrics_json.items():
                if metric_name == "comment":
                    comments[url] = value
                else:
                    metrics[metric_name] = value

            # Create Metric objects and store in all_metrics
            for metric_name, value in metrics.items():
                comment = comments.get(url, "")
                metric = Metric(name=metric_name, value=value, comment=comment)
                all_metrics.setdefault(url, []).append(metric)

        except Exception as e:
            print(f"Error fetching metrics from {url}: {e}")

    return all_metrics


# Function to convert JSON metrics to Prometheus format
def convert_to_prometheus_format(metrics):
    lines = []

    for url, metrics_list in metrics.items():
        for metric in metrics_list:
            lines.append(f"# HELP {metric.name} {metric.comment}")
            lines.append(f"# TYPE {metric.name} gauge")
            lines.append(f"{metric.name} {metric.value}")
    return "\n".join(lines)


# Endpoint to expose metrics in Prometheus format
@app.route("/metrics")
def metrics():
    config = load_configuration()
    if config:
        papercut_metrics = fetch_metrics(config)
        prometheus_metrics = convert_to_prometheus_format(papercut_metrics)
        return Response(prometheus_metrics, mimetype="text/plain")
    else:
        return Response("Error loading configuration", status=500)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000)
