import customtkinter as ctk
import socket
import threading

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
        print("Setting up port scanner widgets...")  # Debugging statement

        # Title Label
        title_label = ctk.CTkLabel(self, text="PORT SCANNER", font=("Arial", 16), text_color="black")
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # IP Address or Domain Name Label
        ip_label = ctk.CTkLabel(self, text="IP ADDRESS OR DOMAIN NAME", font=("Inter", 18), text_color="black")
        ip_label.grid(row=1, column=0, padx=23, pady=5, sticky="w")

        # IP Address or Domain Name Entry
        self.ip_input = ctk.CTkEntry(self, height=62, width=520, fg_color="#D4D4FF", text_color="black", corner_radius=30,
                                    border_width=1, border_color="black")
        self.ip_input.grid(row=2, column=0, padx=(10, 20), pady=5, sticky="w")

        # START Port Label
        start_port_label = ctk.CTkLabel(self, text="START PORT", font=("Inter", 18), text_color="black")
        start_port_label.grid(row=3, column=0, padx=70, pady=5, sticky="w")

        # START Port Input Field
        self.start_port_input = ctk.CTkEntry(self, height=50, width=241, fg_color="#D4D4FF", text_color="black", corner_radius=30,
                                            border_width=1, border_color="black")
        self.start_port_input.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="w")

        # END Port Label
        end_port_label = ctk.CTkLabel(self, text="END PORT", font=("Inter", 18), text_color="black")
        end_port_label.grid(row=3, column=1, padx=30, pady=5, sticky="w")

        # END Port Input Field
        self.end_port_input = ctk.CTkEntry(self, height=50, width=241, fg_color="#D4D4FF", text_color="black", corner_radius=30,
                                            border_width=1, border_color="black")
        self.end_port_input.grid(row=4, column=1, padx=(10, 20), pady=5, sticky="w")

        # Scan Button
        scan_button = ctk.CTkButton(self, text="SCAN", width=200, height=80, corner_radius=234,
                                    fg_color="#D4D4FF", text_color="black", border_width=1, border_color="black",
                                    command=self.start_port_scan_thread)  # Connect to the scanning function
        scan_button.grid(row=5, column=0, columnspan=2, padx=150, pady=20, sticky="w")

        # Result Label
        result_label = ctk.CTkLabel(self, text="RESULTS", font=("Arial", 14), text_color="black")
        result_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Result Box for displaying scan results
        self.result_box = ctk.CTkTextbox(self, height=403, width=480, fg_color="#D4D4FF", text_color="black", corner_radius=30,
                                        border_width=1, border_color="black")
        self.result_box.grid(row=2, column=2, rowspan=4, padx=(10, 20), pady=5, sticky="nsew")
        print("Widgets set up complete.")  # Debugging statement

    def scan_ports(self, ip, start_port, end_port):
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
        self.result_box.configure(state='normal')  # Allow editing the textbox
        self.result_box.delete(1.0, 'end')  # Clear previous results
        if open_ports:
            self.result_box.insert('end', f"Open Ports: {', '.join(map(str, open_ports))}\n")
        else:
            self.result_box.insert('end', "No open ports found.\n")
        self.result_box.configure(state='disabled')  # Disable editing again

    def start_port_scan_thread(self):
        """Start the port scan in a separate thread."""
        ip = self.ip_input.get()
        start_port = int(self.start_port_input.get())
        end_port = int(self.end_port_input.get())
        scan_thread = threading.Thread(target=self.scan_ports, args=(ip, start_port, end_port))
        scan_thread.start()
