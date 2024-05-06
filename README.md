# papercut-exporter
 
A prometheus exporter for the [PaperCut MF](https://www.papercut.com/products/mf/) print management system. Functional enough to publish, but young enough to still call "Work in Progress".

# Installation

## Windows

### Option 1 (Recommended) 

1. Download the latest binary from [Releases](https://github.com/thebenb/papercut-exporter/releases) onto a network-accessible machine of your choice. This should be a machine that can connect to PaperCut and Prometheus. 
    - This can be the machine running Prometheus and/or PaperCut itself, or a different machine entirely. 
2. Create a configuration file following the [configuration](#configuration) template / following the guide.
3. Run the project.

### Option 2

See: [Running the project directly.](#running-the-project-directly)

## Running the project directly

If you prefer running from source, you will need to:

1. Install Python 
2. Install dependencies `pip install -r requirements.txt`
3. Run `app_runner.py` to get the proper WSGI webserver for the project.
    - You can run `papercut_exporter.py` if you'd like to use the Flask development server. 

> [!NOTE]  
> If you are doing this because you are making modifications / improvements to the project, please make a pull request so others can benefit as well.

## Prometheus

Just a simple job with a static config in your `prometheus.yml` will do the trick:

```yml
  - job_name: 'PaperCut'
    static_configs:
      - targets: ['EXPORTER_HOST:PORT']
```

# Configuration

Papercut MF provides multiple official endpoints which are accessible via the GUI. Each http endpoint is formatted like this: `HOST:PORT/api/METRIC?Authorization=AUTH`

Copy and paste each link into a JSON-formatted config. Feel free to rename `config_template.json` to do this. Make sure to pick an unused port.

## Example:

```json
{
  "urls": [
    "http://PAPERCUT_HOST:9191/api/stats/recent-pages-count?minutes=60&Authorization=AUTHKEY",
    "http://PAPERCUT_HOST:9191/api/stats/held-jobs-count?Authorization=AUTHKEY",
    "http://PAPERCUT_HOST:9191/api/health?Authorization=AUTHKEY"
  ],
  "port": 8000
}
```

# Disclaimer

This project is not affiliated with or endorsed by PaperCut Software Pty Ltd. This project is an unofficial tool that utilises official the endpoints provided by a locally hosted instance of PaperCut and translates them into a format compatible with [Prometheus](https://prometheus.io/). While efforts have been made to ensure compatibility and accuracy, I assume no responsibility for any issues or discrepancies that may arise from the use of this tool. No warranty is provided, and you are advised to use this project at your own risk.
