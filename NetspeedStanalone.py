import customtkinter as ctk
import speedtest
import threading


# Function to perform the speed test
def perform_speedtest():
    button.config(state="disabled", text="Testing...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        latency = st.results.ping  # Latency in ms
        provider = st.results.server['sponsor']  # Provider name
        server = st.results.server['host']  # Server IP

        # Update the labels with results
        download_label.configure(text=f"{download_speed:.2f} Mbps")
        upload_label.configure(text=f"{upload_speed:.2f} Mbps")
        latency_label.configure(text=f"{latency:.2f} ms")
        provider_label.configure(text=provider)
        server_label.configure(text=server)
    except Exception as e:
        download_label.configure(text="Error")
        upload_label.configure(text="")
        latency_label.configure(text="")
        provider_label.configure(text="")
        server_label.configure(text="")
    button.config(state="normal", text="Ready")


# Function to start the speed test thread
def start_speedtest_thread():
    threading.Thread(target=perform_speedtest).start()


# Create the main window
app = ctk.CTk()
app.title("NMDS: Network Speed Test")
app.geometry("900x450")

# Configure grid layout
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=2)
app.grid_rowconfigure(2, weight=1)

# Top frame for title
top_frame = ctk.CTkFrame(master=app, width=900, height=50, fg_color="#50514F")
top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

title_label = ctk.CTkLabel(top_frame, text="NETWORK SPEED TEST", font=("Arial", 30))
title_label.pack(pady=10)

# Create circular button in the center
button = ctk.CTkButton(app, text="Ready", font=("Arial", 30), width=120, height=120, corner_radius=60,
                       fg_color="#6B5FBE", hover_color="#4A39BA", command=start_speedtest_thread)
button.grid(row=1, column=1)

# Speed result panels
download_frame = ctk.CTkFrame(app, width=200, height=150, fg_color="#D9D9D9", corner_radius=20)
download_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
download_label = ctk.CTkLabel(download_frame, text="Download Speed", font=("Arial", 20))
download_label.pack(pady=10)

upload_frame = ctk.CTkFrame(app, width=200, height=150, fg_color="#D9D9D9", corner_radius=20)
upload_frame.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")
upload_label = ctk.CTkLabel(upload_frame, text="Upload Speed", font=("Arial", 20))
upload_label.pack(pady=10)

# Bottom result panels
provider_frame = ctk.CTkFrame(app, width=200, height=150, fg_color="#D9D9D9", corner_radius=20)
provider_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
provider_label = ctk.CTkLabel(provider_frame, text="Provider", font=("Arial", 20))
provider_label.pack(pady=10)

latency_frame = ctk.CTkFrame(app, width=200, height=150, fg_color="#D9D9D9", corner_radius=20)
latency_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
latency_label = ctk.CTkLabel(latency_frame, text="Latency", font=("Arial", 20))
latency_label.pack(pady=10)

server_frame = ctk.CTkFrame(app, width=200, height=150, fg_color="#D9D9D9", corner_radius=20)
server_frame.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")
server_label = ctk.CTkLabel(server_frame, text="Server", font=("Arial", 20))
server_label.pack(pady=10)

# Run the main event loop
app.mainloop()
