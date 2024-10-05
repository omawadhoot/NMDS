import pandas as pd
from datetime import datetime
import os

# Create a DataManager class to handle data storage
class DataManager:
    def __init__(self, filepath='network_data.csv'):
        self.filepath = filepath
        self.columns = [
            "Timestamp", "Test Type", "IP/Domain", "Packets Sent", 
            "Packets Received", "Packet Loss", "Average Latency", 
            "Download Speed", "Upload Speed", "Ping Speed", 
            "Number of Hops", "Hop IPs", "Port", "Port Status"
        ]
        self.create_csv_if_not_exists()
        self.load_existing_data()

    def create_csv_if_not_exists(self):
        """Create the CSV file with headers if it doesn't already exist."""
        if not os.path.isfile(self.filepath):
            self.data = pd.DataFrame(columns=self.columns)
            self.data.to_csv(self.filepath, index=False)

    def load_existing_data(self):
        try:
            self.data = pd.read_csv(self.filepath)
        except pd.errors.EmptyDataError:
            self.data = pd.DataFrame(columns=self.columns)

    def save_data(self, entry):
        try:
            entry_df = pd.DataFrame([entry])
            entry_df.to_csv(self.filepath, mode='a', header=False, index=False)
        except PermissionError:
            print(f"Permission denied: Unable to write to {self.filepath}. Please close any open files or check permissions.")

# Collect network data from different modules and store using DataManager
def save_ping_data(data_manager, ping_data):
    entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Type": "Ping Test",
        "IP Address": ping_data.get("ip_address"),
        "Packets Sent": ping_data.get("packets_sent"),
        "Packets Received": ping_data.get("packets_received"),
        "Packets Lost": ping_data.get("packet_loss"),  # Updated from 'Packet Loss'
        "Minimum RTT (ms)": ping_data.get("min_latency"),  # Use min latency if available
        "Maximum RTT (ms)": ping_data.get("max_latency"),  # Use max latency if available
        "Average RTT (ms)": ping_data.get("avg_latency"),  # Ensure this key exists in ping_data
        "Ping Speed": ping_data.get("ping_speed"),  # Correctly reference the ping speed
        "Download Speed": None,
        "Upload Speed": None,
        "Number of Hops": None,
        "Hop IPs": None,
        "Port": None,
        "Port Status": None
    }
    data_manager.save_data(entry)

def save_speed_data(data_manager, speed_data):
    entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Type": "Speed Test",
        "IP/Domain": None,
        "Average Latency": None,
        "Download Speed": speed_data.get("download_speed"),
        "Upload Speed": speed_data.get("upload_speed"),
        "Ping Speed": speed_data.get("ping_speed"),
        "Number of Hops": None,
        "Hop IPs": None,
        "Port": None,
        "Port Status": None
    }
    data_manager.save_data(entry)

def save_traceroute_data(data_manager, traceroute_data):
    # Prepare the entry to save the traceroute results
    entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Type": "Traceroute",
        "IP/Domain": traceroute_data.get("ip_address"),
        "Packets Sent": None,  # Not applicable for traceroute
        "Packets Received": None,  # Not applicable for traceroute
        "Packet Loss": None,  # Not applicable for traceroute
        "Average Latency": None,  # Not applicable for traceroute
        "Download Speed": None,  # Not applicable for traceroute
        "Upload Speed": None,  # Not applicable for traceroute
        "Ping Speed": None,  # Not applicable for traceroute
        "Number of Hops": traceroute_data.get("number_of_hops"),
        "Hop IPs": traceroute_data.get("hop_ips"),  # Ensure this contains a string or a list
        "Port": None,  # Not applicable for traceroute
        "Port Status": None  # Not applicable for traceroute
    }
    
    # Call the save_data method from the data_manager to store the entry
    data_manager.save_data(entry)


def save_port_scan_data(data_manager, port_scan_data):
    entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Type": "Port Scan",
        "IP/Domain": port_scan_data.get("ip_address"),
        "Packets Sent": None,
        "Packets Received": None,
        "Packet Loss": None,
        "Average Latency": None,
        "Download Speed": None,
        "Upload Speed": None,
        "Ping Speed": None,
        "Number of Hops": None,
        "Hop IPs": None,
        "Port": port_scan_data.get("port"),
        "Port Status": port_scan_data.get("port_status")
    }
    data_manager.save_data(entry)

# Example usage with data from external modules
def create_network_dataset():
    data_manager = DataManager("network_data.csv")
    
    # Get ping data from PingTest.py
    from PingTest import get_ping_data
    ping_data = get_ping_data("8.8.8.8")  # Example IP
    save_ping_data(data_manager, ping_data)
    
    # Get speed test data from netspeed.py
    from netspeed import get_speed_data
    speed_data = get_speed_data()
    save_speed_data(data_manager, speed_data)
    
    # Get traceroute data from trace_route.py
    from trace_route import get_traceroute_data
    traceroute_data = get_traceroute_data("8.8.8.8")
    save_traceroute_data(data_manager, traceroute_data)
    
    # Get port scan data from PortScan.py
    from PortScanner import get_port_scan_data
    port_scan_data = get_port_scan_data("8.8.8.8", range(80, 83))  # Example IP and ports
    save_port_scan_data(data_manager, port_scan_data)
    
    print("Network data has been collected and saved to 'network_data.csv'.")
    print(os.getcwd())

# Run the tests
if __name__ == "__main__":
    create_network_dataset()
