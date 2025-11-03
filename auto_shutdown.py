import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

shutdown_thread = None
stop_flag = False

def schedule_shutdown():
    global stop_flag
    stop_flag = False

    try:
        minutes = int(entry.get())
        seconds = minutes * 60
    except:
        messagebox.showerror("Error", "Enter a valid number!")
        return

    status_label.config(text=f"Shutdown in {minutes} min")

    def countdown():
        global stop_flag
        t = seconds
        while t > 0 and not stop_flag:
            mins, secs = divmod(t, 60)
            counter_label.config(text=f"{mins:02}:{secs:02}")
            root.update()
            time.sleep(1)
            t -= 1

        if not stop_flag:
            # Windows shutdown
            os.system("shutdown /s /t 1")

    threading.Thread(target=countdown, daemon=True).start()

def cancel_shutdown():
    global stop_flag
    stop_flag = True

    # Cancel Windows scheduled shutdown
    os.system("shutdown /a")

    status_label.config(text="Shutdown Cancelled")
    counter_label.config(text="--:--")

# ==== UI ====
root = tk.Tk()
root.title("Auto Shutdown")
# Get screen size and compute window size as a fraction so it looks good on any monitor
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# Choose window size as percentage of screen (adjustable)
win_w = max(300, int(screen_w * 0.28))
win_h = max(240, int(screen_h * 0.22))

# Center window
pos_x = (screen_w - win_w) // 2
pos_y = (screen_h - win_h) // 2
root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

# Allow the user to resize; set sensible minimums
root.minsize(300, 260)
root.resizable(True, True)

# Create scaled fonts based on window height
base_font_size = max(10, int(win_h / 20))
header_font = tkfont.Font(family="Helvetica", size=base_font_size)
label_font = tkfont.Font(family="Helvetica", size=max(9, base_font_size - 1))
counter_font = tkfont.Font(family="Helvetica", size=max(18, int(base_font_size * 1.8)))

tk.Label(root, text="Echnology.co", font=header_font, anchor="w").pack(fill='x', pady=5, padx=10)
tk.Label(root, text="Minutes to Shutdown:", font=label_font).pack(pady=5)
entry = tk.Entry(root, font=label_font)
entry.pack(fill='x', padx=20)

start_button = tk.Button(root, text="Start", command=schedule_shutdown, font=label_font)
start_button.pack(pady=10, fill='x', padx=40)

cancel_button = tk.Button(root, text="Stop", command=cancel_shutdown, font=label_font)
cancel_button.pack(pady=6, fill='x', padx=40)

status_label = tk.Label(root, text="Status: Waiting", font=label_font)
status_label.pack(pady=6)

counter_label = tk.Label(root, text="--:--", font=counter_font)
counter_label.pack(pady=10)

root.mainloop()