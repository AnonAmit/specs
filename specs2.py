import psutil
import time
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
        print(f"An error occurred while retrieving VPS specs: {e}")
        return {}

def print_specs(specs):
    """
    Print the VPS specifications.
    
    Args:
        specs (dict): The specifications to print.
    """
    for spec, details in specs.items():
        print(f"{spec}:")
        for key, value in details.items():
            print(f"  {key}: {value}")

def monitor_vps():
    """
    Continuously monitor and display VPS specifications and live process usage.
    """
    try:
        # Initial bandwidth values
        net_io_initial = psutil.net_io_counters()
        bytes_sent_initial = net_io_initial.bytes_sent
        bytes_recv_initial = net_io_initial.bytes_recv

        while True:
            # Get current specs
            specs = get_vps_specs()
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VPS Specs:")
            print_specs(specs)

            # Calculate bandwidth usage
            net_io_current = psutil.net_io_counters()
            bytes_sent_current = net_io_current.bytes_sent
            bytes_recv_current = net_io_current.bytes_recv

            bytes_sent = (bytes_sent_current - bytes_sent_initial) / (1024 ** 3)  # Convert bytes to GB
            bytes_recv = (bytes_recv_current - bytes_recv_initial) / (1024 ** 3)  # Convert bytes to GB

            print("Bandwidth:")
            print(f"  Bytes Sent: {bytes_sent:.2f} GB")
            print(f"  Bytes Received: {bytes_recv:.2f} GB")

            # Update initial values
            bytes_sent_initial = bytes_sent_current
            bytes_recv_initial = bytes_recv_current

            # Display live process usage
            print("\nLive Processes:")
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    print(f"  PID: {proc.info['pid']}, Name: {proc.info['name']}, "
                          f"CPU: {proc.info['cpu_percent']}%, "
                          f"Memory: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            # Wait for 5 seconds before updating again
            time.sleep(5)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    monitor_vps()
