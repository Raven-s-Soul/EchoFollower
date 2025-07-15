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
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def playback(self):
        if not self.click_data:
            messagebox.showinfo("Info", "No clicks recorded to replay.")
            return

        self.stop_flag = False  # Reset stop flag before starting

        def playback_thread():
            try:
                for event in self.click_data:
                    if self.stop_flag:
                        break  # Stop playback immediately
                    time.sleep(event.get("delta", 0))
                    if event.get("type") == "custom":
                        message = event.get("message", "")
                        if message == "do_combo_1":
                            self.keyboard_controller.press(Key.ctrl)
                            self.keyboard_controller.press('c')
                            self.keyboard_controller.release('c')
                            self.keyboard_controller.release(Key.ctrl)
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
