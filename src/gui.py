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
        self.root.geometry("350x400")
        self.root.resizable(False, False)
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # === Recording Section ===
        self.record_frame = tk.LabelFrame(self.root, text="Recording", padx=10, pady=10)
        self.record_frame.grid(padx=10, pady=10, sticky="nsew")

        self.toggle_btn = tk.Button(self.record_frame, text="Start Recording", command=self.toggle_callback)
        self.toggle_btn.grid(row=0, column=0, sticky="we", pady=10)

        self.status_label = tk.Label(self.record_frame, text="Paused", fg="green")
        self.status_label.grid(row=0, column=1, sticky="we", pady=10)

        
        self.record_hint = tk.Label(self.record_frame, text="Press [Ctrl + Space] to toggle recording", fg="gray")
        self.record_hint.grid(row=1, column=0, columnspan=2)

        self.custom_entry = tk.Entry(self.record_frame, width=30)
        self.custom_entry.grid(row=2, column=0, sticky="we", pady=10)

        self.add_event_btn = tk.Button(self.record_frame, text="Add Text", command=self.add_custom_event)
        self.add_event_btn.grid(row=2, column=1, sticky="we", pady=10)
        
        self.custom_entry.bind("<Return>", self.on_enter_pressed)
        
        self.Return_hint = tk.Label(self.record_frame, text="Press [Return] to save text", fg="gray")
        self.Return_hint.grid(row=3, column=0, columnspan=2)
        
        self.clear_btn = tk.Button(self.record_frame, text="Clear All", fg="red", command=self.confirm_clear)
        self.clear_btn.grid(row=4, column=0, sticky="we", pady=10)

        self.count_label = tk.Label(self.record_frame, text="Clicks recorded: 0")
        self.count_label.grid(row=4, column=1, sticky="we", pady=10)
        

        # === Replay Section ===
        self.replay_frame = tk.LabelFrame(self.root, text="Replay", padx=10, pady=10)
        self.replay_frame.grid(padx=10, pady=10, sticky="nsew")

        self.play_btn = tk.Button(self.replay_frame, text="Play", command=self.play_callback)
        self.play_btn.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="we")
        
        self.replay_hint = tk.Label(self.replay_frame, text="Press [Ctrl + Alt] to stop", fg="gray")
        self.replay_hint.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="we")
       

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
