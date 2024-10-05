import customtkinter
from center_window import center_window 
from main_widgets import MainWidgets    
from datamanager import DataManager
from netspeed import networkspeed_data
from PingTest import perform_ping
from trace_route import TraceRoute
from PortScanner import scan_ports

class MainWindow(customtkinter.CTk): 
    def __init__(self):  
        super().__init__() 
        self.minsize(1280, 720) 
        self.title("NMDS")  
        self.resizable(False, False) 
        center_window(self, 1280, 720) 

        try:
            self.wm_iconbitmap(".venv/icons/nmds.ico")  # Use a relative path for the icon
        except Exception as e:
            print(f"Error loading icon: {e}")

        self.app_widgets = MainWidgets(self)  # Initialize MainWidgets instance

        # Define any other necessary instance variables
        self.data_manager = DataManager("network_data.csv")

    def create_network_dataset(self, ip_address, port_range):
        data_manager = DataManager("network_data.csv")

        # Perform Ping Test
        perform_ping(data_manager, ip_address)

        # Perform Speed Test
        networkspeed_data(data_manager)

        # Perform Traceroute Test
        traceroute_instance = TraceRoute()
        traceroute_instance.perform_traceroute(data_manager, traceroute_instance)  # Pass data_manager and ip_address

        # Perform Port Scan
        scan_ports(data_manager, ip_address, port_range)

        print("Network data has been collected and saved to 'network_data.csv'.")

if __name__ == "__main__":
    app = MainWindow() 
    app.mainloop()
