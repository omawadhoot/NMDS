# center_window.py

def center_window(window, window_width=1280, window_height=720):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate x and y coordinates for the window to be centered
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry to widthxheight+x+y
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
