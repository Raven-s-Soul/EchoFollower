import time
import json
import threading
from pynput import mouse
from tkinter import messagebox

class Recorder:
    def __init__(self, log_file, update_ui_callback):
        self.log_file = log_file
        self.update_ui = update_ui_callback

        self.click_data = []
        self.global_start_time = time.time()
        self.pause_offset = 0.0
        self.pause_start_time = None
        self.last_click_time = None

        self.mouse_listener = None
        self.recording = False

        self.load_data()

    def load_data(self):
        try:
            with open(self.log_file, "r") as f:
                import os
                if os.path.exists(self.log_file):
                    self.click_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.click_data = []

    def save_data(self):
        with open(self.log_file, "w") as f:
            json.dump(self.click_data, f, indent=4)

    def get_adjusted_time(self):
        if self.recording:
            return time.time() - self.global_start_time - self.pause_offset
        else:
            return self.pause_start_time - self.global_start_time - self.pause_offset if self.pause_start_time else 0

    def on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            now = self.get_adjusted_time()
            delta = 0 if self.last_click_time is None else round(now - self.last_click_time, 6)
            self.last_click_time = now

            event = {
                "type": "mouse",
                "delta": delta,
                "button": button.name,
                "position": {"x": x, "y": y}
            }
            self.click_data.append(event)
            self.save_data()
            self.update_ui()

    def start(self):
        if self.recording:
            return
        if self.pause_start_time:
            self.pause_offset += time.time() - self.pause_start_time
            self.pause_start_time = None
        else:
            self.global_start_time = time.time()
            self.last_click_time = None
        self.recording = True
        self.update_ui()
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        threading.Thread(target=self.mouse_listener.start, daemon=True).start()

    def stop(self):
        if not self.recording:
            return
        self.pause_start_time = time.time()
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        self.recording = False
        self.update_ui()

    def toggle(self):
        if self.recording:
            self.stop()
        else:
            self.start()

    def clear(self):
        if messagebox.askyesno("Clear Data", "Clear all recorded clicks?"):
            self.click_data = []
            self.last_click_time = None
            self.pause_offset = 0.0
            self.pause_start_time = None
            self.global_start_time = time.time()
            self.save_data()
            self.update_ui()

    def add_custom_event(self, message):
        if not self.recording:
            messagebox.showinfo("Info", "Start recording first to add custom events.")
            return
        now = self.get_adjusted_time()
        delta = 0 if self.last_click_time is None else round(now - self.last_click_time, 6)
        self.last_click_time = now

        event = {
            "type": "custom",
            "delta": delta,
            "message": message
        }
        self.click_data.append(event)
        self.save_data()
        self.update_ui()
        
    def clear(self):
        self.click_data.clear()
