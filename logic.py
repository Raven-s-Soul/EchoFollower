import time
import threading
from tkinter import messagebox
from pynput import mouse, keyboard
from player import Player
from recorder import Recorder

recorder = None
player = None
gui = None

keyboard_listener = None

def set_gui(gui_instance):
    global gui, recorder, player
    gui = gui_instance
    recorder = Recorder(log_file="mouse_clicks.json", update_ui_callback=gui.update_ui)
    player = Player(click_data=recorder.click_data)

def toggle_recording():
    if recorder is None:
        return
    if recorder.recording:
        recorder.stop()
    else:
        recorder.start()

def clear_clicks():
    if recorder is None:
        return
    recorder.clear()

def get_click_count():
    if recorder is None:
        return 0
    return len(recorder.click_data)

def get_status_text():
    if recorder is None:
        return "Paused"
    return "Recording…" if recorder.recording else "Paused"

def start_keyboard_listener():
    global keyboard_listener
    if keyboard_listener is None:
        def on_key_press(key):
            try:
                if key == keyboard.Key.space:
                    toggle_recording()
            except Exception:
                pass
        keyboard_listener = keyboard.Listener(on_press=on_key_press)
        keyboard_listener.start()

def start_playback():
    if player:
        player.playback()

def add_custom_event(message):
    if recorder:
        recorder.add_custom_event(message)

def clear_clicks():
    if recorder:
        recorder.clear()


# Initialize keyboard listener on module import
start_keyboard_listener()
