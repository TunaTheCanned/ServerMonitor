# ServerMonitor
ServerMonitor is a read-only REST API built to return the current system diagnostics.
It uses flask to expose the endpoints and psutil to get information about the system.

## Features
 - CPU usage and CPU times
 - Temperature (if available)
 - Memory and Disk usage
 - System uptime, load or architecture
 - Network I/O counters
 - Running processes

## Requirements
- Python 3
- Dependencies listed in "requirements.txt"


## Install and run on Linux
Run these commands on the server you want to monitor. The example uses Ubuntu and clones the project into your home directory.

```bash
sudo apt update
sudo apt install git python3-venv python3-pip
cd ~
git clone https://github.com/TunaTheCanned/ServerMonitor.git
cd ServerMonitor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install waitress
waitress-serve --host 0.0.0.0 --port 5000 --call app:create_app
```

Waitress keeps running in the foreground. Press `Ctrl+C` to stop it.


## Endpoints
All endpoints use `GET` and return JSON.

| Endpoint | Query parameters | Description |  
|---|---|---|
| `/api/v1/health` | — | Basic API health status |
| `/api/v1/cpu-usage` | `per-cpu=true` or `false` | Overall or per-core CPU usage |
| `/api/v1/cpu-times` | — | CPU time counters for each core |
| `/api/v1/temperature` | — | Hardware temperatures, if available |
| `/api/v1/memory` | — | Memory statistics |
| `/api/v1/disk` | — | Disk usage for accessible partitions |
| `/api/v1/cores` | `logical=true` or `false` | Logical or physical CPU core count |
| `/api/v1/uptime` | — | System uptime in seconds |
| `/api/v1/load` | — | System load averages |
| `/api/v1/system` | — | Operating system, version, and architecture |
| `/api/v1/network` | — | Network I/O counters |
| `/api/v1/processes` | `sort-by=cpu` or `memory`; `limit=<positive integer>` | Process information, optionally sorted and limited |

For `/api/v1/processes`, `sort-by` can be omitted, set to `cpu`, or set to `memory`. `limit` must be a positive integer. A process’s CPU percentage may exceed 100% if it uses multiple CPU cores.
## Tests
From the project directory, with the virtual environment activated, run:

```bash
python -m pytest -q
```

## Some Notes
- The API has no authentication
- Metrics describe the machine the application is running on
- Temperature readings depend on hardware and operating system
