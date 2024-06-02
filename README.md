# VPS Monitoring Tool

This tool continuously monitors and displays various VPS specifications, including RAM, disk usage, CPU information, bandwidth usage, and live process details. The output is color-coded for better readability and is refreshed every second.

## Features

- **RAM Usage**: Displays total, used, and available RAM.
- **Disk Usage**: Displays total, used, and free disk space.
- **CPU Information**: Displays the number of CPU cores and the current CPU frequency.
- **Bandwidth Usage**: Displays the total and session bandwidth usage (bytes sent and received).
- **Live Process Information**: Displays live process details including PID, name, CPU usage, and memory usage.
- **Color-Coded Output**: Different sections and details are color-coded for easy differentiation.

## Prerequisites

- Python 3.x
- `psutil` library
- `curses` library (available in the standard Python library for Unix-like systems)

## Installation

1. Clone the repository or download the script:
    ```bash
    git clone https://github.com/yourusername/vps-monitoring-tool.git
    cd vps-monitoring-tool
    ```

2. Install the required Python library:
    ```bash
    pip install psutil
    ```

## Usage

Run the script using Python:
```bash
python monitor_vps.py
