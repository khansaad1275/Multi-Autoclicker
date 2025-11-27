# === Import and Setup ===
import subprocess, sys
import tkinter as tk
from tkinter import messagebox
import time

# Auto-install pyautogui if not present
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import pyautogui
except ImportError:
    install("pyautogui")
    import pyautogui

# === Global Variables ===
anchors = []

# === Floating Anchor Class ===
class FloatingAnchor:
    counter = 1

    def __init__(self, x=300, y=300):
        self.delay = 1
        self.num = FloatingAnchor.counter
        FloatingAnchor.counter += 1

        # Create floating window for the anchor
        self.win = tk.Toplevel()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.geometry(f"50x50+{x}+{y}")
        self.win.configure(bg="#ff00ff")

        # Label on the anchor to show number and delay
        self.label = tk.Label(
            self.win, text=f"{self.num} | {self.delay}s",
            bg="#ff00ff", fg="white", font=("Arial", 10, "bold")
        )
        self.label.place(x=5, y=15)

        # Enable dragging
        self.win.bind("<ButtonPress-1>", self.start_move)
        self.win.bind("<B1-Motion>", self.move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def move(self, event):
        self.win.geometry(f"+{event.x_root - self.x}+{event.y_root - self.y}")

    def get_pos(self):
        return self.win.winfo_rootx(), self.win.winfo_rooty()

    def hide(self):
        self.win.withdraw()

    def show(self):
        self.win.deiconify()

# === Backend Functions ===
def add_anchor():
    anchors.append(FloatingAnchor())

def update_delay():
    try:
        d = float(delay_entry.get())
        if anchors:
            anchors[-1].delay = d
            anchors[-1].label.config(text=f"{anchors[-1].num} | {d}s")
    except ValueError:
        pass  # Ignore invalid input

def start_run():
    try:
        cycles = int(cycle_entry.get()) if cycle_entry.get() else 1
    except ValueError:
        cycles = 1

    for a in anchors:
        a.hide()
    time.sleep(0.2)

    for _ in range(cycles):
        for a in anchors:
            x, y = a.get_pos()
            pyautogui.moveTo(x + 25, y + 25)
            pyautogui.click()
            time.sleep(a.delay)

    for a in anchors:
        a.show()

# === GUI Module ===
# === GUI Module ===

root = tk.Tk()
root.title("Multi-Autoclicker ⚡")
root.attributes("-topmost", True)
root.geometry("400x100")  # Slightly larger to fit the help button

# Function to show help instructions
def show_help():
    help_text = (
        "How to use Multi-Autoclicker:\n"
        "1. Click 'Add Anchor' to place an anchor on the screen.\n"
        "2. Set the delay for the selected anchor and click 'save'.\n"
        "3. Enter the number of cycles and press 'run'.\n"
        "4. Use 'Clear Anchors' to remove all anchors."
    )
    messagebox.showinfo("Help", help_text)

# Add anchor button
tk.Button(root, text="➕ anchor", command=add_anchor).place(x=10, y=10)

# Help button in the corner
tk.Button(root, text="❓", command=show_help).place(x=370, y=10)

# Delay input
delay_entry = tk.Entry(root, width=4)
delay_entry.place(x=100, y=10)
tk.Button(root, text="save", command=update_delay).place(x=140, y=8)

# Cycles input + run button
cycle_entry = tk.Entry(root, width=4)
cycle_entry.place(x=210, y=10)
tk.Button(root, text="▶ run", command=start_run).place(x=260, y=8)

root.mainloop()

