from tkinter import N
from PIL import Image
import customtkinter   
from center_window import center_window
import speedtest
import threading
from datamanager import DataManager
from datetime import datetime

class NetworkSpeed(customtkinter.CTkToplevel):
    
    _instance = None

    @classmethod
    def get_instance(cls, parent):
        if cls._instance is None or not cls._instance.winfo_exists():
            cls._instance = cls(parent)
        else:
            cls._instance.lift()
            cls._instance.focus_force()
        return cls._instance

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.geometry("1280x720")
        self.title("NMDS: Network Speed Test")
        self.minsize(1280, 720)
        self.resizable(False, False)
        networkspeed_widgets(self)
        center_window(self, 1280, 720)
        self.data_manager = DataManager()  # Create an instance of DataManager
        self.set_appearance_mode("default")

        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.transient(parent)
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.attributes('-topmost', False)

    def on_close(self):
        """Handle the closing of the window."""
        # Set the parent window's reference to None when this window is closed
        NetworkSpeed._instance = None
        self.destroy()


def open_networkspeed(parent):
    if not hasattr(parent, 'network_speed_window'):
        parent.network_speed_window = None  # Initialize if not present

    if parent.network_speed_window is not None and parent.network_speed_window.winfo_exists():
        parent.network_speed_window.lift()  # Bring the window to the front
        parent.network_speed_window.focus_force()  # Focus on the window
        return  # Exit function to avoid creating a new window

    parent.network_speed_window = NetworkSpeed(parent)
    parent.network_speed_window.transient(parent)
    parent.network_speed_window.lift()  # Bring it to the front
    parent.network_speed_window.focus_force()  # Focus on the window
    parent.network_speed_window.attributes('-topmost', True)  # Ensure it's on top initially
    parent.network_speed_window.attributes('-topmost', False)  # Disable always-on-top to restore normal behavior


def networkspeed_widgets(self):

    self.rowconfigure(0, weight=0)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)  # Add a third column for more space

    self.background_frame = customtkinter.CTkFrame(master=self, fg_color="#f1f2f6")
    self.background_frame.grid(row=0, column=0, sticky="nsew", columnspan=3, rowspan=2)  # Use 3 columns now
    self.background_frame.rowconfigure(0, weight=1)
    self.background_frame.columnconfigure(0, weight=1)

    self.top_frame = customtkinter.CTkFrame(self, width=1280, height=77, fg_color="#50514F", border_width=-2)
    self.top_frame.grid(row=0, column=0, sticky="nwe", columnspan=3)
    self.top_frame.rowconfigure(0, weight=1)


    self.top_frame.grid_columnconfigure(0, weight=1)
    self.top_frame.grid_rowconfigure(0, weight=1)

   # Configure the top frame to display the title image
    self.title_image = customtkinter.CTkImage(
        light_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/light.png"),
        dark_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/dark.png"),
        size=(50, 50)
    )

    self.header_label = customtkinter.CTkLabel(self.top_frame, text="NMDS", font=("Inter", 24),padx=20,pady=25,
            image=self.title_image,compound='left',width=240,height=20)
    self.header_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0)

    self.title_label = customtkinter.CTkLabel(
        master=self.background_frame,
        text="NETWORK SPEED TEST",
        font=("Inter", 35),
        text_color="black",
        width=651,
        height=59,
    )
    self.title_label.grid(row=0, column=0, pady=(130, 10), sticky="n", columnspan=3,rowspan=3)  # Adjusted columnspan


    # Ensure the background_frame is properly configured
    self.background_frame.grid(row=0, column=0, sticky="nsew")
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1,weight=1)

    # Create a circular button on the background_frame, place it in the second column (center)
    self.circular_button = customtkinter.CTkButton(
        master=self.background_frame,
        text="Ready",
        font=("Inter", 50),
        width=250,
        height=250,
        corner_radius=139,  # This makes the button circular
        fg_color="#6B5FBE",
        text_color="white",
        border_color="black",
        border_width=5,
        hover_color="#4A39BA",
        command=lambda: start_speedtest_thread(self, self.data_manager)  # Pass the data manager instance
    )
    self.circular_button.grid(row=1, column=1, padx=(20, 20), pady=(40, 50), sticky="n", rowspan=2)

    # Create the dspeed_frame and place it in the first column (left side)
    self.dspeed_frame = customtkinter.CTkFrame(master=self.background_frame, width=229, height=193, 
                                               fg_color="#D9D9D9" , corner_radius= 50)
    self.dspeed_frame.grid(row=1, column=0, padx = (100,10),pady=(50, 50), sticky="nw", rowspan = 2 )
    self.dspeed_frame.grid_propagate(False)

    # Configure the label's row and column to allow it to expand within the frame
    self.dspeed_frame.grid_rowconfigure(0, weight=1)  # Allow label's row to expand
    self.dspeed_frame.grid_columnconfigure(0, weight=1)  # Allow label's column to expand
    
    self.dspeed_label  = customtkinter.CTkLabel(master = self.dspeed_frame, text = "Download Speed",text_color="black",wraplength=200,font=("Inter",25))
    self.dspeed_label.grid(row=0, column=0)

    self.uspeed_frame = customtkinter.CTkFrame(master=self.background_frame,fg_color="#D9D9D9", width = 229 , height = 193 , corner_radius=50 )
    self.uspeed_frame.grid(row=1, column=2, padx=(10, 100), pady=(50, 50), sticky="ne" , rowspan = 2 )

    self.uspeed_frame.grid_propagate(False)

     # Configure the label's row and column to allow it to expand within the frame
    self.uspeed_frame.grid_rowconfigure(0, weight=1)  # Allow label's row to expand
    self.uspeed_frame.grid_columnconfigure(3, weight=1)  # Allow label's column to expand

    self.uspeed_label  = customtkinter.CTkLabel(master = self.uspeed_frame , text = "Upload Speed", text_color="black",wraplength=200,font=("Inter",25))
    self.uspeed_label.grid(row=0, column=3)
    
    self.provider_frame = customtkinter.CTkFrame(master=self.background_frame, width=229, height=193, 
                                               fg_color="#D9D9D9" , corner_radius= 50)
    self.provider_frame.grid(row=2, column=0, padx = (100,10),pady=(160, 20), sticky="nw" , rowspan = 2)
    self.provider_frame.grid_propagate(False)

    # Configure the label's row and column to allow it to expand within the frame
    self.provider_frame.grid_rowconfigure(2, weight=1)  # Allow label's row to expand
    self.provider_frame.grid_columnconfigure(0, weight=1)  # Allow label's column to expand

    self.provider_label  = customtkinter.CTkLabel(master = self.provider_frame , text = "Provider" , text_color = "black",wraplength=200,font=("Inter",25))
    self.provider_label.grid(row=2, column=0)

    self.latency_frame = customtkinter.CTkFrame(master=self.background_frame,fg_color="#D9D9D9", width = 229 , height = 193 , corner_radius=50 )
    self.latency_frame.grid(row=2, column=1, padx=(133, 50), pady=(170, 20), sticky="nw" , rowspan = 2)

    self.latency_frame.grid_propagate(False)

    # Configure the label's row and column to allow it to expand within the frame
    self.latency_frame.grid_rowconfigure(2, weight=1)  # Allow label's row to expand
    self.latency_frame.grid_columnconfigure(1, weight=1)  # Allow label's column to expand

    self.latency_label  = customtkinter.CTkLabel(master = self.latency_frame , text = "Latency", text_color = "black",wraplength=200,font=("Inter",25))
    self.latency_label.grid(row=2, column=1)

    self.server_frame = customtkinter.CTkFrame(master=self.background_frame,fg_color="#D9D9D9", width = 229 , height = 193 , corner_radius=50 )
    self.server_frame.grid(row=2, column=2, padx=(10, 100), pady=(160, 20), sticky="ne" , rowspan = 2)

    self.server_frame.grid_propagate(False)
    
    # Configure the label's row and column to allow it to expand within the frame
    self.server_frame.grid_rowconfigure(2, weight=1)  # Allow label's row to expand
    self.server_frame.grid_columnconfigure(3, weight=1)  # Allow label's column to expand

    self.server_label  = customtkinter.CTkLabel(master = self.server_frame ,text = "Server",text_color="black",wraplength=200,font=("Inter",25))
    self.server_label.grid(row=2, column=3)

    # Adjust the grid configuration to account for multiple columns
    self.background_frame.grid_rowconfigure(1, weight=1)
    self.background_frame.grid_columnconfigure(0, weight=1)
    self.background_frame.grid_columnconfigure(1, weight=1)
    self.background_frame.grid_columnconfigure(2, weight=1)

def networkspeed_data(self, data_manager):
    try:
        # Create a Speedtest object and perform the speed test
        st = speedtest.Speedtest()

        # Get the best server
        st.get_best_server()

        # Perform download and upload speed tests
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        latency = st.results.ping  # Latency in ms
        server = st.results.server['sponsor']  # Service provider name
        server_ip = st.results.server['host']  # Server IP address

        # Update the UI with the results
        self.after(0, lambda: self.dspeed_label.configure(text=f"Download Speed: {download_speed:.2f} Mbps"))
        self.after(0, lambda: self.uspeed_label.configure(text=f"Upload Speed: {upload_speed:.2f} Mbps"))
        self.after(0, lambda: self.latency_label.configure(text=f"Latency: {latency} ms"))
        self.after(0, lambda: self.provider_label.configure(text=f"Provider: {server}"))
        self.after(0, lambda: self.server_label.configure(text=f"Server IP: {server_ip}"))

        # Log the data in DataManager
        entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Type": "Speed Test",
            "Download Speed (Mbps)": download_speed,
            "Upload Speed (Mbps)": upload_speed,
            "Latency (ms)": latency,
            "Provider": server,
            "Server IP": server_ip
        }
        data_manager.log_data(entry)

    except Exception as e:
        # If there's an error during the speed test, display an error message
        error_message = f"Error occurred: {str(e)}"
        self.after(0, lambda: self.dspeed_label.configure(text=error_message))
        self.after(0, lambda: self.uspeed_label.configure(text=""))
        self.after(0, lambda: self.latency_label.configure(text=""))
        self.after(0, lambda: self.provider_label.configure(text=""))
        self.after(0, lambda: self.server_label.configure(text=""))

    finally:
        # Re-enable the button and change its text back to "Ready"
        self.after(0, lambda: self.circular_button.configure(state="normal", text="Ready"))


def start_speedtest_thread(self, data_manager):
    # Disable the button and change its text to "Testing..."
    self.circular_button.configure(state="disabled", text="Testing...")

    # Start a new thread for the speed test to avoid freezing the UI
    threading.Thread(target=networkspeed_data, args=(self, data_manager), daemon=True).start()


def open_networkspeed(parent, data_manager):
    if not hasattr(parent, 'network_speed_window'):
        parent.network_speed_window = None  # Initialize if not present

    if parent.network_speed_window is not None and parent.network_speed_window.winfo_exists():
        parent.network_speed_window.lift()  # Bring the window to the front
        parent.network_speed_window.focus_force()  # Focus on the window
        return  # Exit function to avoid creating a new window

    parent.network_speed_window = NetworkSpeed(parent)
    parent.network_speed_window.transient(parent)
    parent.network_speed_window.lift()  # Bring it to the front
    parent.network_speed_window.focus_force()  # Focus on the window
    parent.network_speed_window.attributes('-topmost', True)  # Ensure it's on top initially
    parent.network_speed_window.attributes('-topmost', False)  # Disable always-on-top to restore normal behavior

    # Start the speed test thread, passing the data_manager
    start_speedtest_thread(parent.network_speed_window, data_manager)  # Ensure data_manager has a save_data method