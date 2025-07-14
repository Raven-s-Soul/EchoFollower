import tkinter as tk
from tkinter import messagebox

class RecorderGUI:
    def __init__(self, root, toggle_callback, clear_callback, get_click_count, get_status_text, play_callback, add_custom_callback):
        self.root = root
        self.toggle_callback = toggle_callback
        self.clear_callback = clear_callback
        self.get_click_count = get_click_count
        self.get_status_text = get_status_text
        self.play_callback = play_callback
        self.add_custom_callback = add_custom_callback

        self.root.title("EchoFollower")
        self.root.geometry("400x280")
        self.root.resizable(False, False)

        # --- Top Row: Toggle Button + Status ---
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        self.toggle_btn = tk.Button(self.top_frame, text="Start Recording", command=self.toggle_callback)
        self.toggle_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.status_label = tk.Label(self.top_frame, text="Paused", fg="green")
        self.status_label.pack(side=tk.LEFT)

        # --- Hint ---
        self.hint_label = tk.Label(self.root, text="Press [Ctrl + Space] to toggle recording", fg="gray")
        self.hint_label.pack(pady=(0, 5))

        # --- Middle Row: Clear + Count (Centered) ---
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=5)

        self.clear_btn = tk.Button(self.middle_frame, text="Clear All", fg="red", command=self.confirm_clear)
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        self.count_label = tk.Label(self.middle_frame, text="Clicks recorded: 0")
        self.count_label.pack(side=tk.LEFT, padx=10)

        # --- Custom Event Entry ---
        self.custom_frame = tk.Frame(self.root)
        self.custom_frame.pack(pady=10)

        self.custom_entry = tk.Entry(self.custom_frame, width=30)
        self.custom_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.custom_entry.bind("<Return>", self.on_enter_pressed)

        self.add_event_btn = tk.Button(self.custom_frame, text="Add Event", command=self.add_custom_event)
        self.add_event_btn.pack(side=tk.LEFT)
        
        # --- Hint ---
        self.hint_label = tk.Label(self.root, text="Press [Return] to Confirm", fg="gray")
        self.hint_label.pack(pady=(0, 5))

        # --- Separator Line ---
        self.separator = tk.Frame(self.root, height=1, bd=1, relief=tk.SUNKEN)
        self.separator.pack(fill=tk.X, padx=10, pady=10)

        # --- Bottom Row: Play Button (Centered) ---
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack()

        self.play_btn = tk.Button(self.bottom_frame, text="▶ Play", command=self.play_callback)
        self.play_btn.pack()

    def update_ui(self):
        status = self.get_status_text()
        count = self.get_click_count()

        self.status_label.config(text=status, fg="red" if "Recording" in status else "green")
        self.toggle_btn.config(text="Stop Recording" if "Recording" in status else "Start Recording")
        self.count_label.config(text=f"Clicks recorded: {count}")

    def confirm_clear(self):
        if messagebox.askyesno("Clear Data", "Are you sure you want to clear all recorded clicks?"):
            self.clear_callback()
            self.update_ui()
            

    def add_custom_event(self):
        message = self.custom_entry.get().strip()
        #if message and self.get_status_text() == "Recording…":
        self.add_custom_callback(message)
        self.custom_entry.delete(0, tk.END)
        #elif not self.get_status_text() == "Recording…":
        #   messagebox.showinfo("Paused", "You can only add custom events while recording.")

    def on_enter_pressed(self, event):
        self.add_custom_event()