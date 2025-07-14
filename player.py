import time
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
from tkinter import messagebox

class Player:
    def __init__(self, click_data):
        self.click_data = click_data
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()

    def playback(self):
        if not self.click_data:
            messagebox.showinfo("Info", "No clicks recorded to replay.")
            return

        def playback_thread():
            try:
                for event in self.click_data:
                    time.sleep(event.get("delta", 0))
                    if event.get("type") == "custom":
                        message = event.get("message", "")
                        # Simulate typing the message
                        for char in message:
                            self.keyboard_controller.press(char)
                            self.keyboard_controller.release(char)
                            time.sleep(0.05)  # optional delay between keystrokes
                    elif event.get("type") == "mouse":
                        pos = event["position"]
                        button_name = event["button"]
                        self.mouse_controller.position = (pos["x"], pos["y"])
                        btn = Button.left if button_name == "left" else Button.right if button_name == "right" else Button.middle
                        self.mouse_controller.press(btn)
                        self.mouse_controller.release(btn)
            except Exception as e:
                messagebox.showerror("Playback Error", str(e))

        threading.Thread(target=playback_thread, daemon=True).start()