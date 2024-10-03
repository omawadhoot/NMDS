import customtkinter as ctk
import threading
import speedtest
import subprocess
import socket
import shlex

# Function to center the window
def center_window(window, width, height):
    """Center the window on the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class NMDSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Network Management Diagnostic Suite")
        self.geometry("1280x720")
        self.minsize(800, 600)
        self.resizable(True, True)
        center_window(self, 1280, 720)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)  # Left panel
        self.grid_columnconfigure(1, weight=3)  # Right panel
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Left Panel with Buttons
        left_panel = ctk.CTkFrame(self, width=200)
        left_panel.grid(row=0, column=0, sticky="nswe")
        left_panel.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        # Logo at the top-left corner
        logo_label = ctk.CTkLabel(left_panel, text="NMDS", font=("Arial", 24, "bold"))
        logo_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Buttons for tools
        self.speedtest_button = ctk.CTkButton(left_panel, text="Check network speed", command=self.show_speedtest)
        self.speedtest_button.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        self.pingtest_button = ctk.CTkButton(left_panel, text="Ping Test", command=self.show_pingtest)
        self.pingtest_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        self.portscanner_button = ctk.CTkButton(left_panel, text="Scan active ports", command=self.show_portscanner)
        self.portscanner_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

        self.traceroute_button = ctk.CTkButton(left_panel, text="Traceroute", command=self.show_traceroute)
        self.traceroute_button.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

        # Right Panel for displaying content
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Bottom Section with additional functionalities
        bottom_frame = ctk.CTkFrame(self.content_frame)
        bottom_frame.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        bottom_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Add buttons for additional features
        show_graph_button = ctk.CTkButton(bottom_frame, text="Show realtime network bandwidth usage")
        show_graph_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        check_network_button = ctk.CTkButton(bottom_frame, text="Check Network Coverage")
        check_network_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        port_details_button = ctk.CTkButton(bottom_frame, text="Show Port Details")
        port_details_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ip_mac_button = ctk.CTkButton(bottom_frame, text="Show IP/MAC Address Details")
        ip_mac_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # Initialize variables to hold current content
        self.current_tool = None

    # Function to clear the content frame
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # Function to show Network Speed Test
    def show_speedtest(self):
        self.clear_content_frame()
        self.current_tool = 'speedtest'

        # Create UI elements for Network Speed Test
        self.speedtest_ui()

    # Function to show Ping Test
    def show_pingtest(self):
        self.clear_content_frame()
        self.current_tool = 'pingtest'

        # Create UI elements for Ping Test
        self.pingtest_ui()

    # Function to show Port Scanner
    def show_portscanner(self):
        self.clear_content_frame()
        self.current_tool = 'portscanner'

        # Create UI elements for Port Scanner
        self.portscanner_ui()

    # Function to show Traceroute
    def show_traceroute(self):
        self.clear_content_frame()
        self.current_tool = 'traceroute'

        # Create UI elements for Traceroute
        self.traceroute_ui()

    # Network Speed Test UI
    def speedtest_ui(self):
        # Title
        title_label = ctk.CTkLabel(self.content_frame, text="NETWORK SPEED TEST", font=("Arial", 30))
        title_label.pack(pady=20)

        # Create circular button in the center
        button = ctk.CTkButton(self.content_frame, text="Ready", font=("Arial", 30), width=120, height=120, corner_radius=60,
                               fg_color="#6B5FBE", hover_color="#4A39BA", command=self.start_speedtest_thread)
        button.pack(pady=20)

        # Results Frame
        results_frame = ctk.CTkFrame(self.content_frame)
        results_frame.pack(pady=20, fill="both", expand=True)
        results_frame.grid_columnconfigure((0,1,2), weight=1)
        results_frame.grid_rowconfigure((0,1), weight=1)

        # Speed result panels
        download_frame = ctk.CTkFrame(results_frame, fg_color="#D9D9D9", corner_radius=20)
        download_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.download_label = ctk.CTkLabel(download_frame, text="Download Speed", font=("Arial", 20))
        self.download_label.pack(pady=10)

        upload_frame = ctk.CTkFrame(results_frame, fg_color="#D9D9D9", corner_radius=20)
        upload_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.upload_label = ctk.CTkLabel(upload_frame, text="Upload Speed", font=("Arial", 20))
        self.upload_label.pack(pady=10)

        latency_frame = ctk.CTkFrame(results_frame, fg_color="#D9D9D9", corner_radius=20)
        latency_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.latency_label = ctk.CTkLabel(latency_frame, text="Latency", font=("Arial", 20))
        self.latency_label.pack(pady=10)

        # Additional info panels
        provider_frame = ctk.CTkFrame(results_frame, fg_color="#D9D9D9", corner_radius=20)
        provider_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.provider_label = ctk.CTkLabel(provider_frame, text="Provider", font=("Arial", 20))
        self.provider_label.pack(pady=10)

        server_frame = ctk.CTkFrame(results_frame, fg_color="#D9D9D9", corner_radius=20)
        server_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.server_label = ctk.CTkLabel(server_frame, text="Server", font=("Arial", 20))
        self.server_label.pack(pady=10)

    def start_speedtest_thread(self):
        speedtest_thread = threading.Thread(target=self.perform_speedtest)
        speedtest_thread.start()

    def perform_speedtest(self):
        self.download_label.configure(text="Testing...")
        self.upload_label.configure(text="Testing...")
        self.latency_label.configure(text="Testing...")
        self.provider_label.configure(text="Testing...")
        self.server_label.configure(text="Testing...")

        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        latency = st.results.ping  # Latency in ms
        server = st.results.server['sponsor']  # Server name
        provider = st.results.client['isp']  # Provider name

        self.download_label.configure(text=f"Download Speed: {download_speed:.2f} Mbps")
        self.upload_label.configure(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        self.latency_label.configure(text=f"Latency: {latency:.2f} ms")
        self.provider_label.configure(text=f"Provider: {provider}")
        self.server_label.configure(text=f"Server: {server}")

    # Ping Test UI
    def pingtest_ui(self):
        title_label = ctk.CTkLabel(self.content_frame, text="PING TEST", font=("Arial", 30))
        title_label.pack(pady=20)

        ip_label = ctk.CTkLabel(self.content_frame, text="IP Address or Domain", font=("Arial", 20))
        ip_label.pack(pady=10)

        self.ping_input = ctk.CTkEntry(self.content_frame, width=300, height=40, font=("Arial", 16))
        self.ping_input.pack(pady=10)

        ping_button = ctk.CTkButton(self.content_frame, text="Ping", command=self.start_pingtest_thread)
        ping_button.pack(pady=10)

        self.ping_result_box = ctk.CTkTextbox(self.content_frame, width=500, height=300, font=("Arial", 14))
        self.ping_result_box.pack(pady=10)

    def start_pingtest_thread(self):
        ip_address = self.ping_input.get()
        ping_thread = threading.Thread(target=self.perform_pingtest, args=(ip_address,))
        ping_thread.start()

    def perform_pingtest(self, ip_address):
        if ip_address:
            try:
                command = f"ping -c 4 {shlex.quote(ip_address)}"  # Adjust for macOS/Linux
                result = subprocess.check_output(command, shell=True, text=True)
                self.ping_result_box.configure(state="normal")
                self.ping_result_box.delete("1.0", "end")
                self.ping_result_box.insert("end", result)
                self.ping_result_box.configure(state="disabled")
            except subprocess.CalledProcessError as e:
                self.ping_result_box.configure(state="normal")
                self.ping_result_box.delete("1.0", "end")
                self.ping_result_box.insert("end", f"Ping failed: {e}")
                self.ping_result_box.configure(state="disabled")
        else:
            self.ping_result_box.configure(state="normal")
            self.ping_result_box.delete("1.0", "end")
            self.ping_result_box.insert("end", "Please enter a valid IP address or domain.")
            self.ping_result_box.configure(state="disabled")

    # Port Scanner UI
    def portscanner_ui(self):
        title_label = ctk.CTkLabel(self.content_frame, text="PORT SCANNER", font=("Arial", 30))
        title_label.pack(pady=20)

        ip_label = ctk.CTkLabel(self.content_frame, text="IP Address or Hostname", font=("Arial", 20))
        ip_label.pack(pady=10)

        self.portscan_ip_input = ctk.CTkEntry(self.content_frame, width=300, height=40, font=("Arial", 16))
        self.portscan_ip_input.pack(pady=10)

        start_port_label = ctk.CTkLabel(self.content_frame, text="Start Port", font=("Arial", 20))
        start_port_label.pack(pady=10)

        self.portscan_start_input = ctk.CTkEntry(self.content_frame, width=150, height=40, font=("Arial", 16))
        self.portscan_start_input.pack(pady=10)

        end_port_label = ctk.CTkLabel(self.content_frame, text="End Port", font=("Arial", 20))
        end_port_label.pack(pady=10)

        self.portscan_end_input = ctk.CTkEntry(self.content_frame, width=150, height=40, font=("Arial", 16))
        self.portscan_end_input.pack(pady=10)

        scan_button = ctk.CTkButton(self.content_frame, text="Scan Ports", command=self.start_portscan_thread)
        scan_button.pack(pady=10)

        self.portscan_result_box = ctk.CTkTextbox(self.content_frame, width=500, height=300, font=("Arial", 14))
        self.portscan_result_box.pack(pady=10)

    def start_portscan_thread(self):
        ip = self.portscan_ip_input.get()
        start_port = int(self.portscan_start_input.get())
        end_port = int(self.portscan_end_input.get())
        scan_thread = threading.Thread(target=self.perform_portscan, args=(ip, start_port, end_port))
        scan_thread.start()

    def perform_portscan(self, ip, start_port, end_port):
        open_ports = []
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        self.portscan_result_box.configure(state="normal")
        self.portscan_result_box.delete("1.0", "end")
        if open_ports:
            self.portscan_result_box.insert("end", f"Open Ports: {', '.join(map(str, open_ports))}\n")
        else:
            self.portscan_result_box.insert("end", "No open ports found.\n")
        self.portscan_result_box.configure(state="disabled")

    # Traceroute UI
    def traceroute_ui(self):
        title_label = ctk.CTkLabel(self.content_frame, text="TRACEROUTE", font=("Arial", 30))
        title_label.pack(pady=20)

        ip_label = ctk.CTkLabel(self.content_frame, text="IP Address or Hostname", font=("Arial", 20))
        ip_label.pack(pady=10)

        self.traceroute_input = ctk.CTkEntry(self.content_frame, width=300, height=40, font=("Arial", 16))
        self.traceroute_input.pack(pady=10)

        trace_button = ctk.CTkButton(self.content_frame, text="Trace", command=self.start_traceroute_thread)
        trace_button.pack(pady=10)

        self.traceroute_result_box = ctk.CTkTextbox(self.content_frame, width=500, height=300, font=("Arial", 14))
        self.traceroute_result_box.pack(pady=10)

    def start_traceroute_thread(self):
        ip_address = self.traceroute_input.get()
        trace_thread = threading.Thread(target=self.perform_traceroute, args=(ip_address,))
        trace_thread.start()

    def perform_traceroute(self, ip_address):
        if ip_address:
            try:
                command = f"traceroute {shlex.quote(ip_address)}"  # Adjust for macOS/Linux
                result = subprocess.check_output(command, shell=True, text=True)
                self.traceroute_result_box.configure(state="normal")
                self.traceroute_result_box.delete("1.0", "end")
                self.traceroute_result_box.insert("end", result)
                self.traceroute_result_box.configure(state="disabled")
            except subprocess.CalledProcessError as e:
                self.traceroute_result_box.configure(state="normal")
                self.traceroute_result_box.delete("1.0", "end")
                self.traceroute_result_box.insert("end", f"Traceroute failed: {e}")
                self.traceroute_result_box.configure(state="disabled")
        else:
            self.traceroute_result_box.configure(state="normal")
            self.traceroute_result_box.delete("1.0", "end")
            self.traceroute_result_box.insert("end", "Please enter a valid IP address or domain.")
            self.traceroute_result_box.configure(state="disabled")

if __name__ == "__main__":
    app = NMDSApp()
    app.mainloop()

