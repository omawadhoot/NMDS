import customtkinter as ctk
import subprocess
import threading

def center_window(window, width, height):
    """Center the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class TracerouteApp(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("NMDS: Traceroute")
        self.minsize(1280, 720)
        self.resizable(True, True)
        center_window(self, 1280, 720)
        
        self.create_widgets()

    def create_widgets(self):
        # Configure rows and columns for layout
        self.grid_rowconfigure(0, weight=1)  # Title Row
        self.grid_rowconfigure(1, weight=1)  # Inputs and Results Row
        self.grid_rowconfigure(2, weight=6)  # Inputs Row
        self.grid_rowconfigure(3, weight=1)  # Results Box Row
        self.grid_columnconfigure(0, weight=1)  # Input Column
        self.grid_columnconfigure(1, weight=2)  # Results Column
        
        # Title
        self.title_label = ctk.CTkLabel(self, text="TRACEROUTE", font=("Arial", 28))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

        # Left Section: Inputs
        self.ip_label = ctk.CTkLabel(self, text="IP ADDRESS OR HOSTNAME", font=("Arial", 18))
        self.ip_label.grid(row=1, column=0, padx=(40, 10), pady=(20, 5), sticky="w")
        
        self.ip_entry = ctk.CTkEntry(self, height=40, width=400, corner_radius=20)
        self.ip_entry.grid(row=2, column=0, padx=(40, 10), pady=(10, 20), sticky="nw")
        
        self.trace_button = ctk.CTkButton(self, text="TRACE", height=50, corner_radius=20, 
                                          command=self.start_traceroute)
        self.trace_button.grid(row=2, column=0, padx=(40, 10), pady=(100, 10), sticky="nw")
        
        self.clear_button = ctk.CTkButton(self, text="CLEAR RESULTS", height=50, corner_radius=20,
                                          command=self.clear_results)
        self.clear_button.grid(row=2, column=0, padx=(40, 10), pady=(180, 10), sticky="nw")

        # Right Section: Results
        self.result_label = ctk.CTkLabel(self, text="RESULTS", font=("Arial", 18))
        self.result_label.grid(row=1, column=1, padx=(20, 10), pady=(20, 5), sticky="w")
        
        self.result_box = ctk.CTkTextbox(self, height=500, width=700, corner_radius=20)
        self.result_box.grid(row=2, column=1, rowspan=2, padx=(10, 40), pady=(10, 40), sticky="nsew")
    
    def start_traceroute(self):
        ip_address = self.ip_entry.get()
        if ip_address:
            self.result_box.configure(state="normal")
            self.result_box.insert("end", f"Tracing route to {ip_address}...\n")
            self.result_box.configure(state="disabled")
            # Start traceroute in a new thread
            traceroute_thread = threading.Thread(target=self.run_traceroute, args=(ip_address,))
            traceroute_thread.start()

    def run_traceroute(self, ip_address):
        try:
            # Run the traceroute command
            result = subprocess.run(['traceroute', ip_address], stdout=subprocess.PIPE, text=True)
            self.update_result_box(result.stdout)
        except Exception as e:
            self.update_result_box(f"Error running traceroute: {e}")

    def update_result_box(self, content):
        self.result_box.configure(state="normal")
        self.result_box.insert("end", content + "\n")
        self.result_box.configure(state="disabled")

    def clear_results(self):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", "Results will be displayed here.")
        self.result_box.configure(state="disabled")

# Run the app
if __name__ == "__main__":
    app = TracerouteApp()
    app.mainloop()
