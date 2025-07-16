import tkinter as tk
from tkinter import PhotoImage
import traceback

from src.gui import RecorderGUI
from src import logic

def run():
    root = tk.Tk()
    icon = PhotoImage(file="assets/icon.png")
    root.iconphoto(False, icon)

    gui = RecorderGUI(
        root=root,
        toggle_callback=logic.toggle_recording,
        clear_callback=logic.clear_clicks,
        get_click_count=logic.get_click_count,
        get_status_text=logic.get_status_text,
        play_callback=logic.start_playback,
        add_custom_callback=logic.add_custom_event
    )


    logic.set_gui(gui)
    gui.update_ui()

    root.mainloop()

if __name__ == "__main__":
    try:
        run()
    except Exception:
        with open("error.log", "w") as f:
            traceback.print_exc(file=f)
