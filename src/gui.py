import tkinter as tk
from tkinter import messagebox


class RecorderGUI:
    def __init__(self, root, toggle_callback, clear_callback, get_click_count, get_status_text, play_callback, add_custom_callback):
        self.root = root
        self.toggle_callback = toggle_callback
        self.clear_callback = clear_callback
        self.get_click_count = get_click_count
        self.get_status_text = get_status_text
        self.add_custom_callback = add_custom_callback
        self.play_callback = play_callback

        self.root.title("EchoFollower")
        self.root.geometry("335x340")
        self.root.resizable(False, False)

        # === Recording Section ===
        self.record_frame = tk.LabelFrame(self.root, text="Recording", padx=10, pady=10)
        self.record_frame.pack(fill="x", padx=10, pady=10)

        top_row = tk.Frame(self.record_frame)
        top_row.pack(fill="x", pady=5)

        # Center container to hold both widgets with some space between
        center_container = tk.Frame(top_row)
        center_container.pack(expand=True)  # This centers horizontally in top_row

        self.toggle_btn = tk.Button(center_container, text="Start Recording", command=self.toggle_callback)
        self.toggle_btn.pack(side="left", padx=(0, 10))  # Fixed size, natural width

        self.status_label = tk.Label(center_container, text="Paused", fg="green", width=12, anchor="center")
        self.status_label.pack(side="left")

        # Second row: hint label
        self.record_hint = tk.Label(self.record_frame, text="Press [Ctrl + Space] to toggle recording", fg="gray")
        self.record_hint.pack(pady=5)

        # Third row: entry + add button
        entry_row = tk.Frame(self.record_frame)
        entry_row.pack(fill="x", pady=5)

        self.custom_entry = tk.Entry(entry_row)
        self.custom_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.custom_entry.bind("<Return>", self.on_enter_pressed)

        self.add_event_btn = tk.Button(entry_row, text="Add Text", command=self.add_custom_event)
        self.add_event_btn.pack(side="left")
        
        # === Cleaning Section ===
        self.cleaning_frame = tk.LabelFrame(self.root, text="Cleaning", padx=10, pady=10)
        self.cleaning_frame.pack(fill="x", padx=10, pady=5)

        self.cleaning_row = tk.Frame(self.cleaning_frame)
        self.cleaning_row.pack(fill="x")

        # Container frame to center both widgets together
        center_container = tk.Frame(self.cleaning_row)
        center_container.pack(expand=True)  # expands to take all available space and centers children by default

        self.clear_btn = tk.Button(center_container, text="Clear All", fg="red", command=self.confirm_clear)
        self.clear_btn.pack(side="left", padx=(0, 10))  # small gap between button and label

        self.count_label = tk.Label(center_container, text="Clicks recorded: 0")
        self.count_label.pack(side="left")

        # === Replay Section ===
        self.replay_frame = tk.LabelFrame(self.root, text="Replay", padx=10, pady=10)
        self.replay_frame.pack(fill="x", padx=10, pady=5)

        self.play_btn = tk.Button(self.replay_frame, text="Play", command=self.play_callback)
        self.play_btn.pack(fill="x", pady=(0, 5))

        self.replay_hint = tk.Label(self.replay_frame, text="Press [Ctrl + Alt] to stop", fg="gray")
        self.replay_hint.pack()

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
