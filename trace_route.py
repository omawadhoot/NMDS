import customtkinter
import subprocess
import platform
from PIL import Image
from center_window import center_window
import threading

def open_traceroute(parent):
    """Open the Traceroute window."""
    # Check if 'trace_testwindow' exists and is still open
    if hasattr(parent, 'trace_testwindow') and parent.trace_testwindow and parent.trace_testwindow.winfo_exists():
        parent.trace_testwindow.lift()  # Bring the window to the front
        parent.trace_testwindow.focus_force()  # Force focus to the window
        parent.trace_testwindow.attributes('-topmost', True)  # Make sure it's on top
        parent.trace_testwindow.attributes('-topmost', False)  # Disable topmost after bringing it to front
    else:
        # Create a new traceroute window
        parent.trace_testwindow = TraceRoute(parent)
        parent.trace_testwindow.transient(parent)  # Keep the window above the parent
        parent.trace_testwindow.lift()
        parent.trace_testwindow.focus_force()
        parent.trace_testwindow.attributes('-topmost', True)  # Make sure it's on top
        parent.trace_testwindow.attributes('-topmost', False)  # Disable topmost after bringing it to front

class TraceRoute(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        # Window setup
        self.geometry("1280x720")
        self.title("Trace Route")
        self.minsize(1280, 720)
        self.resizable(False, False)
        center_window(self, 1280, 720)

        # Appearance Mode (Globally set)
        customtkinter.set_appearance_mode("default")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # Initialize widgets
        self.create_widgets()

    def on_close(self):
        """Handle the closing of the window."""
        self.destroy()

    def create_widgets(self):

        """Create and place all the widgets on the traceroute window."""
        
        # Configure the top frame to display the title image
        self.title_image = customtkinter.CTkImage(
            light_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/light.png"),
            dark_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/dark.png"),
            size=(50, 50)
        )
        # Header Label
        header_label = customtkinter.CTkLabel(self, text="NMDS", font=("Arial", 20), text_color="white", fg_color="#3B3B3B",
                                        height=78, width=1280, anchor="w", padx=10,image=self.title_image,compound='left')
        header_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Traceroute Title
        title_label = customtkinter.CTkLabel(self, text="TRACEROUTE", font=("Arial", 20, "bold"), text_color="black")
        title_label.grid(row=1, column=0, columnspan=3, pady=(20, 10))

        # IP Address or Domain Name Label
        ip_label = customtkinter.CTkLabel(self, text="IP ADDRESS OR HOSTNAME", font=("Inter", 18), text_color="black")
        ip_label.grid(row=2, column=0, padx=140, pady=5, sticky="w")

        # IP Address or Domain Name Entry placed below the label
        self.ip_input = customtkinter.CTkEntry(self, height=62, width=520, fg_color="#D4D4FF", text_color="black", corner_radius=30,
                                        border_width=1, border_color="black")
        self.ip_input.grid(row=3, column=0, padx=(10, 20), pady=5, sticky="w")

        # Trace Button placed below IP Address input
        trace_button = customtkinter.CTkButton(self, text="TRACE", width=200, height=80, corner_radius=234,
                                        font=("Arial", 18), fg_color="#D4D4FF", text_color="black",
                                        border_width=1, border_color="black", command=self.start_trace_route)
        trace_button.grid(row=4, column=0, padx=150, pady=20, sticky="w")

        # Clear Results Button placed below Trace button
        clear_button = customtkinter.CTkButton(self, text="CLEAR RESULTS", width=200, height=80, corner_radius=234,
                                        fg_color="#D4D4FF", text_color="black", border_width=1,
                                        border_color="black", font=("Arial", 18), command=self.clear_results)
        clear_button.grid(row=5, column=0, padx=139, pady=20, sticky="w")

        # Result Label beside the buttons and IP input
        result_label = customtkinter.CTkLabel(self, text="RESULTS", font=("Arial", 14), text_color="black")
        result_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Result Box for displaying traceroute results
        self.result_box = customtkinter.CTkTextbox(self, height=403, width=480, fg_color="#D4D4FF", text_color="black",
                                            corner_radius=30, border_width=1, border_color="black")
        self.result_box.grid(row=3, column=2, rowspan=4, padx=(10, 20), pady=5, sticky="nsew")

    def start_trace_route(self):
        """Start traceroute in a separate thread."""
        threading.Thread(target=self.trace_route).start()

    def trace_route(self):
        """Start traceroute based on the IP or hostname entered."""
        ip_or_hostname = self.ip_input.get()
        if ip_or_hostname:
            traceroute_results = self.run_traceroute(ip_or_hostname)
            self.result_box.insert("1.0", traceroute_results)
        else:
            self.result_box.insert("1.0", "Please enter a valid IP address or hostname.\n")

    def clear_results(self):
        """Clear the results in the result box."""
        self.result_box.delete("1.0", "end")

    def run_traceroute(self, target):
        """Run traceroute command based on the target (IP or hostname)."""
        system_name = platform.system()

        # Determine command based on platform
        if system_name == "Windows":
            command = ["tracert", target]
        else:
            command = ["traceroute", target]

        try:
            # Execute the traceroute command
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"

        except Exception as e:
            return f"An error occurred: {str(e)}"

