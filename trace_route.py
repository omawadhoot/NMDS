import customtkinter
from PIL import Image
from center_window import center_window
import subprocess
import shlex
from datetime import datetime
from datamanager import DataManager
from datamanager import save_traceroute_data
import threading
import re

class TraceRoute(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1280x720")
        self.title("Traceroute")
        customtkinter.set_appearance_mode("dark")
        self.minsize(1280, 720)
        self.resizable(False, False)
        center_window(self, 1280, 720)
        self.data_manager = DataManager()  # Create an instance of DataManager
        self.traceroute_thread = None  # Initialize thread attribute
        self.open_traceroute_widgets()

    def open_traceroute_widgets(self):
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)  # Stretch across width
        self.grid_columnconfigure(1, weight=0)  # Column for Trace button
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.background_frame = customtkinter.CTkFrame(master=self, fg_color="#f1f2f6")
        self.background_frame.grid(row=0, column=0, sticky="nsew", columnspan=2, rowspan=2)
        self.background_frame.rowconfigure(0, weight=1)
        self.background_frame.rowconfigure(1, weight=0)
        self.background_frame.rowconfigure(2, weight=0)
        self.background_frame.rowconfigure(3, weight=1)
        self.background_frame.rowconfigure(4, weight=0)
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

        # Traceroute title label
        self.traceroute_title = customtkinter.CTkLabel(self.background_frame, text="TRACEROUTE", font=("Inter", 35), text_color="black")
        self.traceroute_title.grid(row=1, column=0, columnspan=2, pady=(110, 0), padx=10, sticky="n")

        # Destination label
        self.dest_label = customtkinter.CTkLabel(self.background_frame, text="DESTINATION IP OR DOMAIN", font=("Inter", 25),
                                                  text_color="black", height=60, width=550, anchor='w')
        self.dest_label.grid(row=2, column=0, columnspan=2, padx=(50, 0), pady=(80, 20), sticky="w")

        # Input field for destination
        self.dest_input = customtkinter.CTkEntry(self.background_frame, height=84, width=927, fg_color="#D4D4FF",
                                                  text_color="black", corner_radius=30, border_width=1, border_color="black", font=("Inter", 25))
        self.dest_input.grid(row=3, column=0, padx=(48, 5), pady=(10, 0), sticky="nw")

        # Trace button
        self.trace_button = customtkinter.CTkButton(self.background_frame, text="TRACE", width=228, height=84, corner_radius=40,
                                                     fg_color="#D4D4FF", text_color="black", border_width=1, border_color="black", hover_color="#8493FF", font=("Inter", 30),
                                                     command=self.start_traceroute_thread)  # Start thread instead of direct call
        self.trace_button.grid(row=3, column=1, padx=(5, 58), pady=(10, 25), sticky="n")

        # Result label
        self.result_label = customtkinter.CTkLabel(self.background_frame, text="RESULTS", font=("Inter", 25), text_color="black",
                                                    height=50, width=550, anchor='nw')
        self.result_label.grid(row=4, column=0, columnspan=2, padx=(50, 0), pady=(5, 0), sticky="w")

        # Result display box
        self.result_display = customtkinter.CTkTextbox(self.background_frame, height=150, width=550, fg_color="#D4D4FF", text_color="black",
                                                        corner_radius=30, border_width=1, border_color="black")
        self.result_display.grid(row=5, column=0, columnspan=2, padx=(48, 58), pady=(0, 50), sticky="ew")

        # Scrollbar for the result display
        self.result_scrollbar = customtkinter.CTkScrollbar(self.background_frame, command=self.result_display.yview)
        self.result_scrollbar.grid(row=5, column=2, sticky="ns")  # Use grid instead of pack

        # Link scrollbar to textbox
        self.result_display['yscrollcommand'] = self.result_scrollbar.set

    def start_traceroute_thread(self):
        """Start the traceroute operation in a separate thread."""
        if self.traceroute_thread is None or not self.traceroute_thread.is_alive():
            self.trace_button.configure(state="disabled")  # Disable the button to indicate the process has started
            self.traceroute_thread = threading.Thread(target=self.perform_traceroute)
            self.traceroute_thread.start()

    def update_result_display(self, retrieved_data):
        """Update the result display with the traceroute output."""
        self.result_display.configure(state="normal")  # Enable editing for inserting text
        self.result_display.delete(1.0, customtkinter.END)  # Clear previous content
        self.result_display.insert(customtkinter.END, retrieved_data)  # Insert the new data
        self.result_display.configure(state="disabled")  # Make the text box read-only again

    def perform_traceroute(self):
        ip_address = self.dest_input.get()  # Use dest_input instead of traceroute_input
        if ip_address:
            try:
                command = f"tracert {shlex.quote(ip_address)}"
                result = subprocess.check_output(command, shell=True, text=True)
                parsed_data = parse_traceroute_output(result)

                # Update the display with the results
                self.update_result_display(result)

                # Create an instance of DataManager and save results
                data_manager = DataManager()  # This can be done once in the class's __init__ method
                save_traceroute_data(data_manager, parsed_data)  # Call the function to save data

            except subprocess.CalledProcessError as e:
                self.update_result_display(f"Traceroute failed. Error: {e.returncode}. Please check your connection and try again.")
            finally:
                self.trace_button.configure(state="normal")  # Re-enable the button after completion
        else:
            self.update_result_display("Please enter a valid IP address or domain.")

def parse_traceroute_output(output):
    lines = output.strip().splitlines()
    hops = []
    total_hops = 0
    ip_address = None  # Initialize ip_address

    for line in lines[4:]:  # Skip the header lines
        match = re.match(r'^\s*(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(.*)', line)
        if match:
            hop_number = int(match.group(1))
            rtt_times = [float(match.group(2)), float(match.group(3)), float(match.group(4))]
            ip_address = match.group(5).split(' ')[-1]  # Get the last part which is the IP
            
            hops.append({
                "hop_number": hop_number,
                "ip_address": ip_address,
                "rtt_times": rtt_times
            })
            total_hops += 1

    return {
        "hops": hops,
        "total_hops": total_hops
    }

def open_traceroute(parent):
    # Check if 'traceroute_window' exists and is not destroyed
    if not hasattr(parent, 'traceroute_window') or parent.traceroute_window is None or not parent.traceroute_window.winfo_exists():
        parent.traceroute_window = TraceRoute(parent)  # Create new instance of TraceRoute
    else:
        parent.traceroute_window.focus()  # Bring the existing window to front
