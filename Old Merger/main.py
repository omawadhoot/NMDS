import customtkinter
from center_window import center_window 
from main_widgets import MainWidgets    

class MainWindow(customtkinter.CTk): 
    def __init__(self):  
        super().__init__() 
        self.minsize(1280, 720) 
        self.title("NMDS")  
        self.resizable(False, False) 
        center_window(self, 1280, 720) 

        try:
            self.wm_iconbitmap("icons/nmds.ico")  # Use a relative path for the icon
        except Exception as e:
            print(f"Error loading icon: {e}")

        self.app_widgets = MainWidgets(self)  # Initialize MainWidgets instance

if __name__ == "__main__":
    app = MainWindow() 
    app.mainloop()
    