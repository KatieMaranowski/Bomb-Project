import tkinter as tk
from tkinter import ttk
import random

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class BombGUI(tk.Toplevel):
    def __init__(
        self,
        master,
        open_image_path: str = "virusopen.png",
        closed_image_path: str = "virusclosed.png",
        typing_delay: int = 50
    ):
        super().__init__(master)
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
        self.say("Welcome, Player! The bomb awaits...")

    def say(self, message: str):
        """
        Display and type out a message, toggling mouth images randomly as it goes.
        """
        self._current_message = message + "\n"
        self._typing_index = 0
        # clear previous content
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete("1.0", tk.END)
        # ensure starting with mouth closed
        self._mouth_open = False
        self.photo_label.config(image=self.photo_closed)
        self._type_next_char()

    def _type_next_char(self):
        if self._typing_index < len(self._current_message):
            # randomly decide mouth state for a natural talking effect
            self._mouth_open = random.choice([True, False])
            self.photo_label.config(
                image=self.photo_open if self._mouth_open else self.photo_closed
            )

            # insert next character with center tag
            ch = self._current_message[self._typing_index]
            self.text_box.insert(tk.END, ch, ("center",))
            self.text_box.see(tk.END)
            self._typing_index += 1

            # schedule next char
            self.after(self._typing_delay, self._type_next_char)
        else:
            # finished typing: ensure mouth is closed and disable editing
            self.photo_label.config(image=self.photo_closed)
            self.text_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    gui = BombGUI(
        open_image_path="virusopen.png",
        closed_image_path="virusclosed.png",
        typing_delay=100
    )
    gui.mainloop()
