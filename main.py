import customtkinter as ctk
from tkinter import Tk

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Main application window
class NMDS_App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.title("NMDS")
        self.minsize(1280, 720)
        center_window(self, 1280, 720)

        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        # Left-side menu frame
        self.menu_frame = ctk.CTkFrame(self, fg_color="#7261a3", corner_radius=0)
        self.menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.menu_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Logo (Top-left)
        self.logo_label = ctk.CTkLabel(self.menu_frame, text="NMDS", text_color="white", font=("Arial", 24))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Menu Buttons
        self.check_speed_button = ctk.CTkButton(self.menu_frame, text="Check network speed", width=200, height=50)
        self.check_speed_button.grid(row=1, column=0, padx=20, pady=10)

        self.ping_test_button = ctk.CTkButton(self.menu_frame, text="Ping Test", width=200, height=50)
        self.ping_test_button.grid(row=2, column=0, padx=20, pady=10)

        self.scan_ports_button = ctk.CTkButton(self.menu_frame, text="Scan active ports", width=200, height=50)
        self.scan_ports_button.grid(row=3, column=0, padx=20, pady=10)

        self.traceroute_button = ctk.CTkButton(self.menu_frame, text="Traceroute", width=200, height=50)
        self.traceroute_button.grid(row=4, column=0, padx=20, pady=10)

        # Graph section placeholder (center)
        self.graph_frame = ctk.CTkFrame(self, fg_color="#D4D4FF", corner_radius=15)
        self.graph_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.graph_label = ctk.CTkLabel(self.graph_frame, text="Show Graph of network\nspeed, bandwidth usage, latency", font=("Arial", 20))
        self.graph_label.grid(row=0, column=0, padx=20, pady=20)

        # Bottom button frame
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#D4D4FF", corner_radius=15)
        self.bottom_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.bottom_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Bottom buttons
        self.realtime_button = ctk.CTkButton(self.bottom_frame, text="Show realtime network bandwidth usage", width=200, height=50)
        self.realtime_button.grid(row=0, column=0, padx=20, pady=10)

        self.network_coverage_button = ctk.CTkButton(self.bottom_frame, text="Check Network Coverage", width=200, height=50)
        self.network_coverage_button.grid(row=0, column=1, padx=20, pady=10)

        self.port_details_button = ctk.CTkButton(self.bottom_frame, text="Show Port Details", width=200, height=50)
        self.port_details_button.grid(row=0, column=2, padx=20, pady=10)

        self.ip_mac_details_button = ctk.CTkButton(self.bottom_frame, text="Show IP/MAC Address Details", width=200, height=50)
        self.ip_mac_details_button.grid(row=0, column=3, padx=20, pady=10)

# Run the application
if __name__ == "__main__":
    app = NMDS_App()
    app.mainloop()
