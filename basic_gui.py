import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

def show_static_waveform():
    root = tk.Tk()
    root.overrideredirect(True)  # No border
    root.wm_attributes("-topmost", True)
    root.config(bg="black")
    root.wm_attributes("-transparentcolor", "black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    image = Image.open("8c5136de-7714-4e1c-a0e4-36ebea767666.png").convert("RGBA")
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo, bg="black")
    label.image = photo
    label.pack()

    # Centered just above taskbar
    x = (screen_width - image.width) // 2
    y = screen_height - image.height - 80
    root.geometry(f"+{x}+{y}")

    def auto_close():
        time.sleep(5)
        root.destroy()

    threading.Thread(target=auto_close, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    print("🚀 Transparent PNG waveform popup launching...")
    show_static_waveform()
