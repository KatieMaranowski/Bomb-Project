import tkinter as tk
from tkinter import ttk
import random

class BombGUI(tk.Tk):
    def __init__(
        self,
        open_image_path: str = "virusopen.png",
        closed_image_path: str = "virusclosed.png",
        typing_delay: int = 50
    ):
        super().__init__()
        self.title("Bomb Interface")
        self.minsize(600, 500)

        # typing config
        self._typing_delay = typing_delay  # ms per character
        self._typing_index = 0
        self._current_message = ""
        self._mouth_open = False

        # load images for talking animation
        if PIL_AVAILABLE:
            img_o = Image.open(open_image_path).resize((300, 300), Image.LANCZOS)
            img_c = Image.open(closed_image_path).resize((300, 300), Image.LANCZOS)
            self.photo_open = ImageTk.PhotoImage(img_o)
            self.photo_closed = ImageTk.PhotoImage(img_c)
        else:
            self.photo_open = tk.PhotoImage(file=open_image_path)
            self.photo_closed = tk.PhotoImage(file=closed_image_path)

        # start with mouth closed
        self.photo_label = ttk.Label(self, image=self.photo_closed)
        self.photo_label.pack(pady=20)

        # dialogue text box
        self.text_frame = ttk.Frame(self)
        self.text_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.text_box = tk.Text(
            self.text_frame,
            height=4,
            wrap=tk.WORD,
            font=("Arial", 14),
            state=tk.DISABLED,
            relief=tk.SUNKEN,
            bd=2
        )
        self.text_box.pack(fill=tk.X)
        # configure center alignment tag
        self.text_box.tag_configure("center", justify="center")

        # initial message
        self.say("Welcome, Player! The bomb awaits.")

        # --- Status display below dialogue ---
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.X, padx=20, pady=(0,20))

        self.lbl_timer   = ttk.Label(self.status_frame, text="Time left: ")
        self.lbl_timer.grid(row=0, column=0, padx=5, sticky="w")
        self.lbl_keypad  = ttk.Label(self.status_frame, text="Keypad: ")
        self.lbl_keypad.grid(row=0, column=1, padx=5, sticky="w")
        self.lbl_wires   = ttk.Label(self.status_frame, text="Wires: ")
        self.lbl_wires.grid(row=0, column=2, padx=5, sticky="w")
        self.lbl_button  = ttk.Label(self.status_frame, text="Button: ")
        self.lbl_button.grid(row=1, column=0, padx=5, sticky="w")
        self.lbl_toggles = ttk.Label(self.status_frame, text="Toggles: ")
        self.lbl_toggles.grid(row=1, column=1, padx=5, sticky="w")
        self.lbl_strikes = ttk.Label(self.status_frame, text="Strikes left: ")
        self.lbl_strikes.grid(row=1, column=2, padx=5, sticky="w")

    def update_status(self, timer, keypad, wires, button, toggles, strikes):
        """
        Refresh all status labels. Call this periodically (e.g., from bomb.py check_phases()).
        """
        self.lbl_timer["text"]   = f"Time left: {timer}"
        self.lbl_keypad["text"]  = f"Keypad: {keypad}"
        self.lbl_wires["text"]   = f"Wires: {wires}"
        self.lbl_button["text"]  = f"Button: {button}"
        self.lbl_toggles["text"] = f"Toggles: {toggles}"
        self.lbl_strikes["text"] = f"Strikes left: {strikes}"
