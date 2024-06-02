import psutil
import time
import curses
from datetime import datetime

def get_vps_specs():
    """
    Retrieve VPS specifications including RAM, disk, CPU, and bandwidth information.
    
    Returns:
        dict: A dictionary containing the specifications.
    """
    try:
        # Get RAM information
        ram_info = psutil.virtual_memory()
        total_ram = ram_info.total / (1024 ** 3)  # Convert bytes to GB
        used_ram = ram_info.used / (1024 ** 3)    # Convert bytes to GB
        available_ram = ram_info.available / (1024 ** 3)  # Convert bytes to GB

        # Get disk information
        disk_info = psutil.disk_usage('/')
        total_disk = disk_info.total / (1024 ** 3)  # Convert bytes to GB
        used_disk = disk_info.used / (1024 ** 3)    # Convert bytes to GB
        free_disk = disk_info.free / (1024 ** 3)    # Convert bytes to GB

        # Get processor information
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_freq_current = cpu_freq.current / 1000  # Convert MHz to GHz

        specs = {
            "RAM": {
                "Total": f"{total_ram:.2f} GB",
                "Used": f"{used_ram:.2f} GB",
                "Available": f"{available_ram:.2f} GB"
            },
            "Disk": {
                "Total": f"{total_disk:.2f} GB",
                "Used": f"{used_disk:.2f} GB",
                "Free": f"{free_disk:.2f} GB"
            },
            "CPU": {
                "Cores": cpu_cores,
                "Current Frequency": f"{cpu_freq_current:.2f} GHz"
            }
        }

        return specs
    except Exception as e:
        return {"Error": str(e)}

def monitor_vps(stdscr):
    """
    Continuously monitor and display VPS specifications and live process usage.
    
    Args:
        stdscr: The curses screen object.
    """
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)  # Make getch() non-blocking
    stdscr.timeout(1000)  # Refresh every 1 second

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    try:
        # Initial bandwidth values
        net_io_initial = psutil.net_io_counters()
        bytes_sent_initial = net_io_initial.bytes_sent
        bytes_recv_initial = net_io_initial.bytes_recv

        while True:
            stdscr.clear()  # Clear the screen

            # Get current specs
            specs = get_vps_specs()
            stdscr.addstr(0, 0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VPS Specs:", curses.color_pair(1))

            # Display specs
            row = 1
            for spec, details in specs.items():
                stdscr.addstr(row, 0, f"{spec}:", curses.color_pair(2))
                row += 1
                for key, value in details.items():
                    stdscr.addstr(row, 2, f"{key}: {value}", curses.color_pair(3))
                    row += 1

            # Calculate bandwidth usage
            net_io_current = psutil.net_io_counters()
            bytes_sent_current = net_io_current.bytes_sent
            bytes_recv_current = net_io_current.bytes_recv

            bytes_sent = (bytes_sent_current - bytes_sent_initial) / (1024 ** 3)  # Convert bytes to GB
            bytes_recv = (bytes_recv_current - bytes_recv_initial) / (1024 ** 3)  # Convert bytes to GB

            stdscr.addstr(row, 0, "Bandwidth (total):", curses.color_pair(2))
            stdscr.addstr(row + 1, 2, f"Bytes Sent: {bytes_sent_current / (1024 ** 3):.2f} GB", curses.color_pair(3))
            stdscr.addstr(row + 2, 2, f"Bytes Received: {bytes_recv_current / (1024 ** 3):.2f} GB", curses.color_pair(3))

            stdscr.addstr(row + 4, 0, "Bandwidth (session):", curses.color_pair(2))
            stdscr.addstr(row + 5, 2, f"Bytes Sent: {bytes_sent:.2f} GB", curses.color_pair(3))
            stdscr.addstr(row + 6, 2, f"Bytes Received: {bytes_recv:.2f} GB", curses.color_pair(3))

            # Update initial values
            bytes_sent_initial = bytes_sent_current
            bytes_recv_initial = bytes_recv_current

            # Display live process usage
            row += 8
            stdscr.addstr(row, 0, "Live Processes:", curses.color_pair(2))
            row += 1
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    stdscr.addstr(row, 2, f"PID: {proc.info['pid']}, Name: {proc.info['name']}, "
                                          f"CPU: {proc.info['cpu_percent']}%, "
                                          f"Memory: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB",
                                curses.color_pair(4))
                    row += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            stdscr.refresh()  # Refresh the screen

            # Exit if a key is pressed
            if stdscr.getch() != -1:
                break
    except KeyboardInterrupt:
        stdscr.addstr(row, 0, "Monitoring stopped.", curses.color_pair(5))
        stdscr.refresh()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(monitor_vps)
