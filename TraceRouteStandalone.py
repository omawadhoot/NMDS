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

        self.create_widgets()

    def create_widgets(self):
        # Left Panel with Buttons
        left_panel = ctk.CTkFrame(self, width=200)
        left_panel.grid(row=0, column=0, sticky="nswe")
        left_panel.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        # Logo at the top-left corner
        logo_label = ctk.CTkLabel(left_panel, text="NMDS", font=("Arial", 24, "bold"))
        logo_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Buttons for tools
        self.speedtest_button = ctk.CTkButton(left_panel, text="Network Speed Test", command=self.show_speedtest)
        self.speedtest_button.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        self.pingtest_button = ctk.CTkButton(left_panel, text="Ping Test", command=self.show_pingtest)
        self.pingtest_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        self.portscanner_button = ctk.CTkButton(left_panel, text="Port Scanner", command=self.show_portscanner)
        self.portscanner_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

        self.traceroute_button = ctk.CTkButton(left_panel, text="Traceroute", command=self.show_traceroute)
        self.traceroute_button.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

        # Right Panel for displaying content
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

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

    # Function to perform the speed test
    def perform_speedtest(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000      # Convert to Mbps
            latency = st.results.ping                   # Latency in ms
            provider = st.results.server['sponsor']     # Provider name
            server = st.results.server['host']          # Server IP

            # Update the labels with results
            self.download_label.configure(text=f"{download_speed:.2f} Mbps")
            self.upload_label.configure(text=f"{upload_speed:.2f} Mbps")
            self.latency_label.configure(text=f"{latency:.2f} ms")
            self.provider_label.configure(text=provider)
            self.server_label.configure(text=server)
        except Exception as e:
            self.download_label.configure(text="Error")
            self.upload_label.configure(text="")
            self.latency_label.configure(text="")
            self.provider_label.configure(text="")
            self.server_label.configure(text="")

    # Function to start the speed test thread
    def start_speedtest_thread(self):
        threading.Thread(target=self.perform_speedtest).start()

    # Ping Test UI
    def pingtest_ui(self):
        # Title
        title_label = ctk.CTkLabel(self.content_frame, text="PING TEST", font=("Arial", 30))
        title_label.pack(pady=20)

        # Input Frame
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(pady=10)

        # IP Address label
        ip_label = ctk.CTkLabel(input_frame, text="IP ADDRESS OR DOMAIN", font=("Arial", 20))
        ip_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        # Input field for IP or domain
        self.ping_input = ctk.CTkEntry(input_frame, width=400, font=("Arial", 18))
        self.ping_input.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="w")

        # Ping button beside the input field
        ping_button = ctk.CTkButton(input_frame, text="PING", width=100, height=40, command=self.perform_ping)
        ping_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Result display box
        self.result_display = ctk.CTkTextbox(self.content_frame, height=300)
        self.result_display.pack(pady=20, fill="both", expand=True)

    def perform_ping(self):
        ip_address = self.ping_input.get()  # Get the IP or domain from input
        if ip_address:
            try:
                # Execute the ping command
                command = f"ping -c 4 {shlex.quote(ip_address)}"  # Adapt for macOS/Linux
                result = subprocess.check_output(command, shell=True, text=True)  # Capture output
                self.update_ping_result(result)  # Update the display with the results
            except subprocess.CalledProcessError as e:
                self.update_ping_result(f"Ping failed: {e}")  # Handle errors
        else:
            self.update_ping_result("Please enter a valid IP address or domain.")

    def update_ping_result(self, retrieved_data):
        # Clear existing text
        self.result_display.configure(state="normal")  # Temporarily enable editing to clear
        self.result_display.delete("1.0", "end")
        # Insert new data
        self.result_display.insert("1.0", retrieved_data)
        self.result_display.configure(state="disabled")  # Disable editing again

    # Port Scanner UI
    def portscanner_ui(self):
        # Title
        title_label = ctk.CTkLabel(self.content_frame, text="PORT SCANNER", font=("Arial", 30))
        title_label.pack(pady=20)

        # Input Frame
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(pady=10)

        # IP Address label
        ip_label = ctk.CTkLabel(input_frame, text="IP ADDRESS OR HOSTNAME", font=("Arial", 20))
        ip_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Input field for IP or domain
        self.ip_input = ctk.CTkEntry(input_frame, width=300, font=("Arial", 18))
        self.ip_input.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Start Port label
        start_port_label = ctk.CTkLabel(input_frame, text="START PORT", font=("Arial", 20))
        start_port_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Start Port input
        self.start_port_input = ctk.CTkEntry(input_frame, width=150, font=("Arial", 18))
        self.start_port_input.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # End Port label
        end_port_label = ctk.CTkLabel(input_frame, text="END PORT", font=("Arial", 20))
        end_port_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # End Port input
        self.end_port_input = ctk.CTkEntry(input_frame, width=150, font=("Arial", 18))
        self.end_port_input.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Scan Button
        scan_button = ctk.CTkButton(input_frame, text="SCAN", width=100, height=40, command=self.start_port_scan_thread)
        scan_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Result display box
        self.port_result_display = ctk.CTkTextbox(self.content_frame, height=300)
        self.port_result_display.pack(pady=20, fill="both", expand=True)

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
        self.port_result_display.configure(state='normal')  # Allow editing the textbox
        self.port_result_display.delete(1.0, 'end')  # Clear previous results
        if open_ports:
            self.port_result_display.insert('end', f"Open Ports: {', '.join(map(str, open_ports))}\n")
        else:
            self.port_result_display.insert('end', "No open ports found.\n")
        self.port_result_display.configure(state='disabled')  # Disable editing again

    def start_port_scan_thread(self):
        """Start the port scan in a separate thread."""
        ip = self.ip_input.get()
        try:
            start_port = int(self.start_port_input.get())
            end_port = int(self.end_port_input.get())
            if start_port > end_port:
                self.update_port_result("Start port must be less than or equal to end port.")
                return
            scan_thread = threading.Thread(target=self.scan_ports, args=(ip, start_port, end_port))
            scan_thread.start()
        except ValueError:
            self.update_port_result("Please enter valid port numbers.")

    def update_port_result(self, message):
        self.port_result_display.configure(state='normal')  # Allow editing the textbox
        self.port_result_display.delete(1.0, 'end')  # Clear previous results
        self.port_result_display.insert('end', message + "\n")
        self.port_result_display.configure(state='disabled')  # Disable editing again

    # Traceroute UI
    def traceroute_ui(self):
        # Title
        title_label = ctk.CTkLabel(self.content_frame, text="TRACEROUTE", font=("Arial", 30))
        title_label.pack(pady=20)

        # Input Frame
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(pady=10)

        # IP Address label
        ip_label = ctk.CTkLabel(input_frame, text="IP ADDRESS OR HOSTNAME", font=("Arial", 20))
        ip_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Input field for IP or domain
        self.traceroute_input = ctk.CTkEntry(input_frame, width=400, font=("Arial", 18))
        self.traceroute_input.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Trace Button
        trace_button = ctk.CTkButton(input_frame, text="TRACE", width=100, height=40, command=self.start_traceroute)
        trace_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Result display box
        self.traceroute_result_display = ctk.CTkTextbox(self.content_frame, height=300)
        self.traceroute_result_display.pack(pady=20, fill="both", expand=True)

    def start_traceroute(self):
        ip_address = self.traceroute_input.get()
        if ip_address:
            self.traceroute_result_display.configure(state="normal")
            self.traceroute_result_display.insert("end", f"Tracing route to {ip_address}...\n")
            self.traceroute_result_display.configure(state="disabled")
            # Start traceroute in a new thread
            traceroute_thread = threading.Thread(target=self.run_traceroute, args=(ip_address,))
            traceroute_thread.start()
        else:
            self.update_traceroute_result("Please enter a valid IP address or domain.")

    def run_traceroute(self, ip_address):
        try:
            # Run the traceroute command
            result = subprocess.run(['traceroute', ip_address], stdout=subprocess.PIPE, text=True)
            self.update_traceroute_result(result.stdout)
        except Exception as e:
            self.update_traceroute_result(f"Error running traceroute: {e}")

    def update_traceroute_result(self, content):
        self.traceroute_result_display.configure(state="normal")
        self.traceroute_result_display.insert("end", content + "\n")
        self.traceroute_result_display.configure(state="disabled")

if __name__ == "__main__":
    app = NMDSApp()
    app.mainloop()
