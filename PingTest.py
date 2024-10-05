import customtkinter
from PIL import Image
from center_window import center_window
import subprocess
import shlex
from datetime import datetime
from datamanager import DataManager  # Ensure this module is properly implemented
import re

class PingTest(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1280x720")
        self.title("Ping Test")
        customtkinter.set_appearance_mode("dark")
        self.minsize(1280, 720)
        self.resizable(False, False)
        center_window(self, 1280, 720)
        self.data_manager = DataManager()
        self.open_pingtest_widgets()

    def open_pingtest_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)  # Stretch across width
        self.grid_columnconfigure(1, weight=0)  # Column for Ping button
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.background_frame = customtkinter.CTkFrame(master=self, fg_color="#f1f2f6")
        self.background_frame.grid(row=0, column=0, sticky="nsew", columnspan=2, rowspan=2)
        self.background_frame.rowconfigure(0, weight=1)
        self.background_frame.rowconfigure(1, weight=0)
        self.background_frame.rowconfigure(2, weight=0)
        self.background_frame.rowconfigure(3, weight=0)
        self.background_frame.rowconfigure(4, weight=1)
        self.background_frame.rowconfigure(5, weight=0)
        self.background_frame.columnconfigure(0, weight=1)
        self.background_frame.columnconfigure(1, weight=1)

        # Top frame
        self.top_frame = customtkinter.CTkFrame(self, width=1280, height=77, fg_color="#50514F", border_width=-2)
        self.top_frame.grid(row=0, column=0, sticky="nwe", columnspan=3)

        # Configure the grid for the top frame to center the label
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=0)

        # Configure the top frame to display the title image
        self.title_image = customtkinter.CTkImage(
            light_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/light.png"),
            dark_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/dark.png"),
            size=(50, 50)
        )

        self.header_label = customtkinter.CTkLabel(self.top_frame, text="NMDS", font=("Inter", 24), padx=20, pady=25,
                                                image=self.title_image, compound='left', width=240, height=20)
        self.header_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0)

        # Ping Test title label
        self.ping_testtitle = customtkinter.CTkLabel(self.background_frame, text="PING TEST", font=("Inter", 35), text_color="black")
        self.ping_testtitle.grid(row=1, column=0, columnspan=3, pady=(110, 0), padx=10, sticky="n")

        # IP Address or Domain label
        self.ping_label2 = customtkinter.CTkLabel(self.background_frame, text="IP ADDRESS OR DOMAIN", font=("Inter", 25),
                                                text_color="black", height=60, width=550, anchor='w')
        self.ping_label2.grid(row=2, column=0, columnspan=2, padx=(50, 0), pady=(80, 20), sticky="w")

        # Input field for IP or domain
        self.ping_input = customtkinter.CTkEntry(self.background_frame, height=84, width=927, fg_color="#D4D4FF",
                                                text_color="black", corner_radius=30, border_width=1, border_color="black", font=("Inter", 25))
        self.ping_input.grid(row=3, column=0, padx=(48, 5), pady=(10, 0), sticky="nw")

        # Ping button placed beside the input field
        self.ping_button = customtkinter.CTkButton(self.background_frame, text="PING", width=228, height=84, corner_radius=40,
                                                fg_color="#D4D4FF", text_color="black", border_width=1, border_color="black", hover_color="#8493FF", font=("Inter", 30),
                                                command=lambda: perform_ping(self))  # Pass instance to perform_ping
        self.ping_button.grid(row=3, column=1, padx=(5, 58), pady=(10, 25), sticky="n")

        # Result label
        self.pingresult_label = customtkinter.CTkLabel(self.background_frame, text="RESULTS", font=("Inter", 25), text_color="black",
                                                    height=50, width=550, anchor='nw')
        self.pingresult_label.grid(row=4, column=0, columnspan=2, padx=(50, 0), pady=(5, 0), sticky="w")

        # Result display box
        self.result_display = customtkinter.CTkTextbox(self.background_frame, height=150, width=550, fg_color="#D4D4FF", text_color="black",
                                                    corner_radius=30, border_width=1, border_color="black")
        self.result_display.grid(row=5, column=0, columnspan=2, padx=(48, 58), pady=(0, 50), sticky="ew")

        # Scrollbar for the result display
        self.result_scrollbar = customtkinter.CTkScrollbar(self.background_frame, command=self.result_display.yview)
        self.result_scrollbar.grid(row=5, column=2, sticky="ns")  # Positioning scrollbar next to textbox

        # Link scrollbar to textbox
        self.result_display['yscrollcommand'] = self.result_scrollbar.set

def perform_ping(ping_test_instance):
    ip_address = ping_test_instance.ping_input.get()
    if ip_address:
        try:
            command = f"ping -n 4 {shlex.quote(ip_address)}"
            result = subprocess.check_output(command, shell=True, text=True)
            update_result_display(ping_test_instance, result)

            # Extracting the necessary data using regex
            packets_info = re.search(r"Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)", result)
            rtt_info = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", result)
            
            # Set default values if the regex didn't match
            packets_sent = packets_info.group(1) if packets_info else 0
            packets_received = packets_info.group(2) if packets_info else 0
            packets_lost = packets_info.group(3) if packets_info else 0
            min_rtt = rtt_info.group(1) if rtt_info else 0
            max_rtt = rtt_info.group(2) if rtt_info else 0
            avg_rtt = rtt_info.group(3) if rtt_info else 0

            # Save results to DataManager with extracted ping data
            entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test Type": "Ping Test",
                "IP Address": ip_address,
                "Results": result,  # Full result text if needed for reference
                "Packets Sent": packets_sent,
                "Packets Received": packets_received,
                "Packets Lost": packets_lost,
                "Minimum RTT (ms)": min_rtt,
                "Maximum RTT (ms)": max_rtt,
                "Average RTT (ms)": avg_rtt
            }
            ping_test_instance.data_manager.save_data(entry)  # Use instance to save data

        except subprocess.CalledProcessError as e:
            update_result_display(ping_test_instance, f"Ping failed. Error: {e.returncode}. Please check your connection and try again.")
    else:
        update_result_display(ping_test_instance, "Please enter a valid IP address or domain.")

def update_result_display(ping_test_instance, retrieved_data):
    # Clear existing text
    ping_test_instance.result_display.configure(state="normal")  # Temporarily enable editing to clear
    ping_test_instance.result_display.delete("1.0", "end")  
    # Insert new data
    ping_test_instance.result_display.insert("1.0", retrieved_data)  
    ping_test_instance.result_display.configure(state="disabled")  # Disable editing again

def open_pingtest(parent):
    # Check if 'ping_testwindow' exists and is still open
    if hasattr(parent, 'ping_testwindow') and parent.ping_testwindow and parent.ping_testwindow.winfo_exists():
        parent.ping_testwindow.lift()  # Bring the window to the front
        parent.ping_testwindow.focus_force()  # Force focus to the window
        parent.ping_testwindow.attributes('-topmost', True)  # Make sure it's on top
        parent.ping_testwindow.attributes('-topmost', False)  # Disable topmost after bringing it to front
    else:
        # Create a new ping test window
        parent.ping_testwindow = PingTest(parent)
        parent.ping_testwindow.transient(parent)  # Keep the window above the parent
        parent.ping_testwindow.lift()
        parent.ping_testwindow.focus_force()
        parent.ping_testwindow.attributes('-topmost', True)  # Make sure it's on top
        parent.ping_testwindow.attributes('-topmost', False)  # Disable topmost after bringing it to front
