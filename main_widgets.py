from ast import Import
import customtkinter
from PIL import Image
from netspeed import open_networkspeed
from PingTest import open_pingtest
from trace_route import open_traceroute
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PortScanner import PortScanner
import psutil
import subprocess
import time
from threading import Thread
import socket 
import uuid 
import re
from datamanager import DataManager  # Import DataManager

class MainWidgets:
    def __init__(self, root):
        self.root = root
        self.data_manager = DataManager()  # Create an instance of DataManager
        self.main_frames()
        self.main_sidebar_buttons()
        self.main_page1_panels()
        self.main_switcher()

    # Function to create the frames on the main window
    def main_frames(self):
        # Configure root grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=3)  # Adjusted weights for middle frame
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.root.columnconfigure(5, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=2)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=0)

        # Top frame
        self.top_frame = customtkinter.CTkFrame(self.root, width=1280, height=77, fg_color="#50514F", border_width=-2)
        self.top_frame.grid(row=0, column=0, sticky="nwe", columnspan=3)

        # Configure the grid for the top frame to center the label
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)

        # Configure the top frame to display the title image
        self.title_image = customtkinter.CTkImage(
            light_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/light.png"),
            dark_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/dark.png"),
            size=(50, 50)
        )
        # Title Label for the main window
        self.title_label = customtkinter.CTkLabel(
            master=self.top_frame, text="NMDS", font=("Inter", 24), padx=20, pady=25,
            image=self.title_image, compound='left', width=240, height=20
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=0)

        # Left frame
        self.left_frame = customtkinter.CTkFrame(self.root, width=290, height=643, fg_color="#6b5fbe", border_width=-4)
        self.left_frame.grid(row=1, column=0, sticky="nswe", rowspan=5)

        # Right frame (with space for both large and mini panels)
        self.right_frame = customtkinter.CTkFrame(self.root, width=998, height=644, fg_color="#f1f2f6", border_width=-2)
        self.right_frame.grid(row=1, column=1, sticky="nswe", rowspan=4, columnspan=2)

        # Configure the right_frame grid layout with 4 columns
        self.right_frame.rowconfigure(0, weight=1)  # Top row for large panels
        self.right_frame.rowconfigure(1, weight=1)  # Bottom row for mini-panels
        self.right_frame.columnconfigure(0, weight=1)  # Columns for panel spacing
        self.right_frame.columnconfigure(1, weight=1)
        self.right_frame.columnconfigure(2, weight=1)
        self.right_frame.columnconfigure(3, weight=1)

    def main_sidebar_buttons(self):
        # Configure the buttons in GUI with vertical spacing of 90
        self.button1 = customtkinter.CTkButton(
            self.left_frame, text="Check Network Speed", fg_color="#AEB8FE", corner_radius=15, width=253, height=70, 
            bg_color="#6b5fbe", command=lambda: open_networkspeed(self.root, self.data_manager), hover_color="#EEEEF0", 
            text_color="black", font=("Inter", 24)
        )
        self.button1.grid(row=1, column=0, sticky="news", padx=10, pady=(30, 45))  # 45 for half of 90px

        self.button2 = customtkinter.CTkButton(
            self.left_frame, text="Ping Test", fg_color="#AEB8FE", corner_radius=15, width=253, height=70, 
            bg_color="#6b5fbe", command=lambda: open_pingtest(self.root), hover_color="#EEEEF0", 
            text_color="black", font=("Inter", 24)
        )
        self.button2.grid(row=2, column=0, sticky="news", padx=10, pady=(45, 45))  # Add vertical padding of 90px total

        self.button3 = customtkinter.CTkButton(
            self.left_frame, text="Scan Ports",  
            fg_color="#AEB8FE", corner_radius=15, width=253, height=70, 
            bg_color="#6b5fbe", hover_color="#EEEEF0", text_color="black", font=("Inter", 24),  
            command=lambda: self.open_portscanner()  # Ensure this line is correct
        )
        self.button3.grid(row=3, column=0, sticky="news", padx=10, pady=(45, 45))  # Add vertical padding of 90px total
        
        self.button4 = customtkinter.CTkButton(
            self.left_frame, text="Traceroute", fg_color="#AEB8FE", corner_radius=15, width=253, height=70, 
            bg_color="#6b5fbe", hover_color="#EEEEF0", text_color="black", font=("Inter", 24),
            command=lambda: open_traceroute(self.root) 
        )
        self.button4.grid(row=4, column=0, sticky="news", padx=10, pady=(45, 30))  # Keep equal padding as above


    def main_page1_panels(self):
    # Configure the top large panel (previously panel1 and panel2, now combined)
        self.panel1 = customtkinter.CTkFrame(
            self.right_frame, width=894, height=369, fg_color="#dcdff8", corner_radius=15, 
            border_color="black", border_width=2
        )
        self.panel1.grid(row=0, column=0, sticky="nsew", padx=(46, 46), pady=30, columnspan=4)  # Spanning four columns

        # Configure the bottom mini-panels uniformly, height increased and padding adjusted
        self.panel3 = customtkinter.CTkFrame(
            self.right_frame, width=205, height=240, fg_color="#dcdff8", corner_radius=15, 
            border_color="black", border_width=2
        )
        self.panel3.grid(row=1, column=0, sticky="nsew", padx=(46, 15), pady=(20, 30))  # Adjusted pady

        self.panel4 = customtkinter.CTkFrame(
            self.right_frame, width=205, height=240, fg_color="#dcdff8", corner_radius=15, 
            border_color="black", border_width=2
        )
        self.panel4.grid(row=1, column=1, sticky="nsew", padx=(15, 15), pady=(20, 30))  # Adjusted pady

        self.panel5 = customtkinter.CTkFrame(
            self.right_frame, width=205, height=240, fg_color="#dcdff8", corner_radius=15, 
            border_color="black", border_width=2
        )
        self.panel5.grid(row=1, column=2, sticky="nsew", padx=(15, 15), pady=(20, 30))  # Adjusted pady

        self.panel6 = customtkinter.CTkFrame(
            self.right_frame, width=205, height=240, fg_color="#dcdff8", corner_radius=15, 
            border_color="black", border_width=2
        )
        self.panel6.grid(row=1, column=3, sticky="nsew", padx=(15, 46), pady=(20, 30))  # Adjusted pady
        self.panel6.grid_propagate(False)

        def update_coverage_details(self,coverage_results):
            """Update the network coverage results label."""
            self.coverage_label.configure(text=coverage_results)  # Update with the coverage results

        # Fetch and display IP and MAC address details
        self.display_ip_mac()

    def display_ip_mac(self):
        ip_address = socket.gethostbyname(socket.gethostname())
        mac_address = self.get_mac_address()

        # Using grid instead of pack
        ip_label = customtkinter.CTkLabel(self.panel6, text=f"IP Address: {ip_address}", font=("Inter", 20), text_color="black",wraplength=200)
        ip_label.grid(row=0, column=0,padx = (20,5) ,pady=(20,30), sticky="nesw")

        mac_label = customtkinter.CTkLabel(self.panel6, text=f"MAC Address: {mac_address}", font=("Inter", 20), text_color="black",wraplength=200)
        mac_label.grid(row=1, column=0, padx = (20,5),pady=(20,30), sticky="nesw")

    def get_mac_address(self):
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return mac

    def main_switcher(self):
        self.switcher_button = customtkinter.CTkButton(
            master=self.top_frame, text="Switch to Dark Mode", command=self.switch_theme, 
            fg_color="white", hover_color="lightgray", text_color="black"
        )
        self.switcher_button.grid(row=0, column=1, padx=(20, 0))

    def switch_theme(self):
        if customtkinter.get_appearance_mode() == "Light":
            customtkinter.set_appearance_mode("Dark")
            self.switcher_button.configure(text="Switch to Light Mode")
        else:
            customtkinter.set_appearance_mode("Light")
            self.switcher_button.configure(text="Switch to Dark Mode")

    def open_portscanner(self):
        """Open the Port Scanner window."""
        port_scanner_window = PortScanner(self.root)  # Create the PortScanner window
        port_scanner_window.transient(self.root)  # Keep it above the main window
        port_scanner_window.lift()  # Bring it to the front
        port_scanner_window.focus_force()  # Force focus to the window

# To use this in your main.py
if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("1280x720")
    app = MainWidgets(root)
    root.mainloop()