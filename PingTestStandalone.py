import customtkinter
from PIL import Image
import subprocess
import shlex

class PingTest(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.geometry("1280x720")
        self.title("Ping Test")
        customtkinter.set_appearance_mode("light")
        self.configure(fg_color="#f1f2f6")

        # Build the UI
        self.build_ping_test_ui()

    def build_ping_test_ui(self):
        # Top frame for NMDS title
        self.top_frame = customtkinter.CTkFrame(self, width=1280, height=77, fg_color="#50514F")
        self.top_frame.grid(row=0, column=0, sticky="nwe", columnspan=3)
        
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=0)

        # Logo and title
        self.title_image = customtkinter.CTkImage(
            light_image=Image.open("/Users/kshitijksawant/Programs/NMDS/NMDS/images/light.png"),
            dark_image=Image.open("/Users/kshitijksawant/Programs/NMDS/NMDS/images/dark.png"),
            #light_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/light.png"),
            #dark_image=Image.open("C:/Users/omawa/OneDrive/Desktop/PYTHON NMDS/.venv/images/dark.png"),
            size=(50, 50)
        )
        self.header_label = customtkinter.CTkLabel(self.top_frame, text="NMDS", font=("Inter", 24), padx=20, pady=25,
                                                   image=self.title_image, compound='left', width=240, height=20)
        self.header_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0)

        # Main label for "Ping Test"
        self.ping_testtitle = customtkinter.CTkLabel(self, text="PING TEST", font=("Inter", 35), text_color="black")
        self.ping_testtitle.grid(row=1, column=0, columnspan=3, pady=(50, 20), padx=10, sticky="n")

        # IP Address label
        self.ping_label2 = customtkinter.CTkLabel(self, text="IP ADDRESS OR DOMAIN", font=("Inter", 25), text_color="black")
        self.ping_label2.grid(row=2, column=0, padx=(50, 0), pady=(10, 20), sticky="w")

        # Input field for IP or domain
        self.ping_input = customtkinter.CTkEntry(self, height=84, width=927, fg_color="#D4D4FF",
                                                 text_color="black", corner_radius=30, border_width=1, border_color="black", font=("Inter", 25))
        self.ping_input.grid(row=3, column=0, padx=(48, 5), pady=(10, 0), sticky="w")

        # Ping button beside the input field
        self.ping_button = customtkinter.CTkButton(self, text="PING", width=228, height=84, corner_radius=30,
                                                   fg_color="#AEB8FE", text_color="black", hover_color="#8493FF",
                                                   border_width=1, border_color="black", font=("Inter", 30),
                                                   command=self.perform_ping)
        self.ping_button.grid(row=3, column=1, padx=(10, 58), pady=(10, 25), sticky="w")

        # Result label
        self.pingresult_label = customtkinter.CTkLabel(self, text="RESULTS", font=("Inter", 25), text_color="black")
        self.pingresult_label.grid(row=4, column=0, columnspan=2, padx=(50, 0), pady=(10, 0), sticky="w")

        # Result display box
        self.result_display = customtkinter.CTkTextbox(self, height=150, width=927, fg_color="#D4D4FF", text_color="black",
                                                       corner_radius=30, border_width=1, border_color="black")
        self.result_display.grid(row=5, column=0, columnspan=2, padx=(48, 58), pady=(20, 50), sticky="ew")

    def perform_ping(self):
        ip_address = self.ping_input.get()  # Get the IP or domain from input
        if ip_address:
            try:
                # Execute the ping command
                command = f"ping -c 4 {shlex.quote(ip_address)}"  # Adapt for macOS
                result = subprocess.check_output(command, shell=True, text=True)  # Capture output
                self.update_result_display(result)  # Update the display with the results
            except subprocess.CalledProcessError as e:
                self.update_result_display(f"Ping failed: {e}")  # Handle errors
        else:
            self.update_result_display("Please enter a valid IP address or domain.")

    def update_result_display(self, retrieved_data):
        # Clear existing text
        self.result_display.configure(state="normal")  # Temporarily enable editing to clear
        self.result_display.delete("1.0", "end")
        # Insert new data
        self.result_display.insert("1.0", retrieved_data)
        self.result_display.configure(state="disabled")  # Disable editing again


if __name__ == "__main__":
    app = PingTest()
    app.mainloop()
