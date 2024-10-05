import customtkinter as ctk
import socket
import threading
from datetime import datetime
from datamanager import DataManager

def center_window(window, width, height):
    """Center the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class PortScanner(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("1280x720")
        self.title("NMDS: Port Scanner")
        self.minsize(1280, 720)
        self.resizable(False, False)
        # Center the window
        center_window(self, 1280, 720)

        # Call the widget setup function
        self.portscanner_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Handle the closing of the window."""
        self.destroy()

    def portscanner_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="PORT SCANNER", font=("Arial", 40, "bold"), text_color="#333333")
        title_label.grid(row=0, column=0, columnspan=2, pady=(30, 30), sticky="n")

        # Left side input fields
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=1, column=0, rowspan=4, sticky="nsew", padx=(20, 10), pady=(20, 20))

        # Configure left frame grid for resizing
        left_frame.grid_columnconfigure(0, weight=1)

        # IP Address or Hostname Label
        ip_label = ctk.CTkLabel(left_frame, text="IP ADDRESS OR HOSTNAME", font=("Arial", 20), text_color="#333333")
        ip_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        # IP Address or Domain Name Entry
        self.ip_input = ctk.CTkEntry(left_frame, height=50, width=300, fg_color="#E0E7FF", text_color="black", corner_radius=15,
                                     border_width=2, border_color="#B4C2FF", font=("Arial", 18))
        self.ip_input.grid(row=1, column=0, padx=(10, 10), pady=(10, 20), sticky="ew")

        # START Port Label
        start_port_label = ctk.CTkLabel(left_frame, text="START PORT", font=("Arial", 20), text_color="#333333")
        start_port_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        # START Port Input Field
        self.start_port_input = ctk.CTkEntry(left_frame, height=50, width=300, fg_color="#E0E7FF", text_color="black", corner_radius=15,
                                             border_width=2, border_color="#B4C2FF", font=("Arial", 18))
        self.start_port_input.grid(row=3, column=0, padx=(10, 10), pady=(10, 20), sticky="ew")

        # END Port Label
        end_port_label = ctk.CTkLabel(left_frame, text="END PORT", font=("Arial", 20), text_color="#333333")
        end_port_label.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        # END Port Input Field
        self.end_port_input = ctk.CTkEntry(left_frame, height=50, width=300, fg_color="#E0E7FF", text_color="black", corner_radius=15,
                                           border_width=2, border_color="#B4C2FF", font=("Arial", 18))
        self.end_port_input.grid(row=5, column=0, padx=(10, 10), pady=(10, 20), sticky="ew")

        # Scan Button
        scan_button = ctk.CTkButton(left_frame, text="SCAN", width=180, height=60, corner_radius=15,
                                    fg_color="#4A74E8", text_color="white", hover_color="#334FA7",
                                    border_width=2, border_color="#4A74E8", font=("Arial", 20, "bold"),
                                    command=self.start_port_scan_thread)
        scan_button.grid(row=6, column=0, pady=(30, 20), padx=(10, 10), sticky="ew")

        # Result Box for displaying scan results
        self.result_box = ctk.CTkTextbox(self, height=500, width=600, fg_color="#E0E7FF", text_color="black", corner_radius=15,
                                         border_width=2, border_color="#B4C2FF", font=("Arial", 16))
        self.result_box.grid(row=1, column=1, rowspan=4, pady=(10, 20), padx=(20, 20), sticky="nsew")

    def start_port_scan_thread(self):
        """Start the port scan in a separate thread."""
        ip = self.ip_input.get()
        start_port = int(self.start_port_input.get())
        end_port = int(self.end_port_input.get())
        scan_thread = threading.Thread(target=scan_ports, args=(self, ip, start_port, end_port))
        scan_thread.start()

def scan_ports(port_scanner, ip, start_port, end_port):
    """Scan ports on the given IP address."""
    open_ports = []
    for port in range(start_port, end_port + 1):  # Scanning specified port range
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout after 1 second
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    # Update the results box with the open ports
    port_scanner.result_box.configure(state='normal')  # Allow editing the textbox
    port_scanner.result_box.delete(1.0, 'end')  # Clear previous results
    if open_ports:
        result_message = f"Open Ports: {', '.join(map(str, open_ports))}\n"
        port_scanner.result_box.insert('end', result_message)
        
        # Save results to DataManager
        entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Type": "Port Scan",
            "Results": result_message,
            "IP Address": ip,
            "Start Port": start_port,
            "End Port": end_port
        }
        DataManager.save_data(entry)
    else:
        port_scanner.result_box.insert('end', "No open ports found.\n")
    port_scanner.result_box.configure(state='disabled')  # Disable editing again
