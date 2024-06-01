import psutil

def get_vps_specs():
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

    # Get bandwidth information
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent / (1024 ** 3)  # Convert bytes to GB
    bytes_recv = net_io.bytes_recv / (1024 ** 3)  # Convert bytes to GB

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
        },
        "Bandwidth": {
            "Bytes Sent": f"{bytes_sent:.2f} GB",
            "Bytes Received": f"{bytes_recv:.2f} GB"
        }
    }

    return specs

if __name__ == "__main__":
    vps_specs = get_vps_specs()
    for spec, details in vps_specs.items():
        print(f"{spec}:")
        for key, value in details.items():
            print(f"  {key}: {value}")
