"""
Author: Bailey Goodrich
Date: 4/7/2025
Course: CAP4601/5600

Description:
This module implements the graphical user interface (GUI) for the Tarot Reader application.
It provides an interactive experience for users to select a reading category, flip tarot cards, and view generated summaries.

Key Features:
- **Main Menu**: Allows users to choose a reading category (Life, Love, or Career).
- **Card Flip Animation**: Simulates flipping tarot cards with visuals and sound effects.
- **AI Integration**: Uses simulated annealing to select meaningful card spreads and generate coherent summaries.
- **Dynamic Summary Display**: Presents a personalized summary based on the selected category and card spread.

Dependencies:
- **tkinter**: For GUI components.
- **Pillow (PIL)**: For image handling.
- **pygame**: For sound effects.
- **tarot_ai**: For card selection.
- **interpreter**: For generating summaries of tarot readings.
- **json**: For loading tarot data from JSON files.
- **os**: For file path handling.

Data Files:
- **datasets/simple_tarot.json**: Contains tarot card data.
- **datasets/tarot_interps.json**: Contains tarot card interpretations.
- **datasets/general_advice.json**: Contains general advice data.
- **assets/**: Contains card images and sound files.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import pygame
from tarot_ai import simulated_annealing
import interpreter

pygame.init()

# Load tarot data
with open("datasets/simple_tarot.json", "r") as f:
    tarot_data = json.load(f)

with open("datasets/tarot_interps.json", "r") as f:
    detailed_interps = json.load(f)

with open("datasets/general_advice.json", "r") as f:
    general_advice = json.load(f)

CARD_BACK_IMAGE = "assets/card_back.png"
CARD_FOLDER = "assets/"
CARD_SIZE = (150, 250)
BG_COLOR = "#001f3f"

class TarotApp:
    """
    Initializes the TarotApp class, setting up the main application window,
    loading resources, and displaying the main menu.

    Parameters:
    - root: The root Tkinter window for the application.
    """
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600")
        self.root.title("AI Tarot Reader")
        self.root.configure(bg=BG_COLOR)
        try:
            pygame.mixer.init()
            self.flip_sound = pygame.mixer.Sound("assets/flip_sound.wav")
        except pygame.error:
            self.flip_sound = None
        self.category = None
        self.card_widgets = []
        self.card_images = []
        self.spread = []
        self.revealed = [False, False, False]
        self.summary = ""
        self.summary_text = None

        self.main_menu()

    def main_menu(self):
        """
        Displays the main menu for selecting a tarot reading category.
        Clears the current screen and shows category options.
        """
        self.clear_screen()
        try:
            logo_img = Image.open(CARD_BACK_IMAGE).resize((CARD_SIZE))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.root, image=logo_photo, bg=BG_COLOR)
            logo_label.image = logo_photo
            logo_label.pack(pady=(20, 10))
        except FileNotFoundError:
            pass

        tk.Label(self.root, text="🔮 Choose a Reading Category 🔮", font=("Helvetica", 16), bg=BG_COLOR, fg="white").pack(pady=10)
        for cat in ["life", "love", "career"]:
            tk.Button(
                self.root, text=f"{cat.capitalize()} ✨", font=("Helvetica", 14),
                bg="#003366", fg="white", activebackground="#004080",
                command=lambda c=cat: self.start_reading(c)
            ).pack(pady=5)

    def start_reading(self, category):
        """
        Starts the tarot reading process for the selected category.
        Generates a card spread and prepares a summary.

        Parameters:
        - category: The selected reading category (e.g., 'life', 'love', 'career').
        """
        self.category = category
        self.spread, _ = simulated_annealing(tarot_data, detailed_interps, category)
        self.revealed = [False, False, False]
        self.card_images = []
        self.summary = interpreter.generate_summary(self.spread, detailed_interps, tarot_data, general_advice, self.category)
        self.show_loading()
        self.root.after(1500, self.show_spread)

    def show_loading(self):
        """
        Displays a loading screen while the tarot reading is being prepared.
        """
        self.clear_screen()
        tk.Label(self.root, text=f"🔮 Preparing your {self.category.capitalize()} reading... 🔮",
                 font=("Helvetica", 14), bg=BG_COLOR, fg="white").pack(pady=50)

    def show_spread(self):
        """
        Displays the tarot card spread for the reading.
        Allows users to reveal cards and view their interpretations.
        """
        self.clear_screen()

        tk.Label(self.root, text=f"{self.category.capitalize()} Reading", font=("Helvetica", 18, "bold"),
                 bg=BG_COLOR, fg="white").pack(pady=(10, 0))

        tk.Label(self.root, text="🌟✨🔮🌙⭐️🔮🌙⭐️🔮✨🌟", font=("Helvetica", 14),
                 fg="lightblue", bg=BG_COLOR).pack(pady=5)

        layout_frame = tk.Frame(self.root, bg=BG_COLOR)
        layout_frame.pack(fill="both", expand=True, padx=10)

        # Left: card spread
        card_frame = tk.Frame(layout_frame, bg=BG_COLOR)
        card_frame.pack(side="left", padx=10)

        labels = ["Past", "Present", "Future"]
        self.card_widgets = []
        self.card_images = []

        for i in range(3):
            column_frame = tk.Frame(card_frame, bg=BG_COLOR)
            column_frame.grid(row=0, column=i, padx=10)

            img = Image.open(CARD_BACK_IMAGE).resize(CARD_SIZE)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(column_frame, image=photo, bg=BG_COLOR)
            label.image = photo
            self.card_images.append(photo)
            label.bind("<Button-1>", lambda e, idx=i: self.reveal_card(idx))
            label.pack()

            text = tk.Label(column_frame, text=labels[i], font=("Helvetica", 12), bg=BG_COLOR, fg="white")
            text.pack(pady=5)

            self.card_widgets.append((label, text))

        # Right: reserved space for summary (initially empty)
        self.summary_frame = tk.Frame(layout_frame, bg=BG_COLOR, width=300, height=400)
        self.summary_frame.pack(side="right", fill="y", padx=10)

        # Bottom buttons
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=(10, 5))

        tk.Button(
            button_frame, text="🔁 Inquire Again?", font=("Helvetica", 12),
            bg="#003366", fg="white", activebackground="#004080",
            command=self.main_menu
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame, text="❌ Exit the Realm", font=("Helvetica", 12),
            bg="#003366", fg="white", activebackground="#004080",
            command=self.root.quit
        ).grid(row=0, column=1, padx=10)

        # Copyright
        tk.Label(self.root, text="Gummy Bear deck © U.S. Games Systems, Inc.",
                 font=("Helvetica", 8), bg=BG_COLOR, fg="white", anchor="sw"
                 ).place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def reveal_card(self, index):
        """
        Handles the logic for flipping and revealing a card in the spread.

        Parameters:
        - index: The index of the card to reveal (0 for Past, 1 for Present, 2 for Future).
        """
        if self.revealed[index]:
            return

        if self.flip_sound:
            self.flip_sound.play()

        label, _ = self.card_widgets[index]

        try:
            flip_img = Image.open(CARD_BACK_IMAGE).resize(CARD_SIZE)
            flip_photo = ImageTk.PhotoImage(flip_img)
            label.configure(image=flip_photo)
            label.image = flip_photo
            self.card_images[index] = flip_photo
            self.root.after(200, lambda: self.complete_reveal(index))

        except FileNotFoundError:
            messagebox.showerror("Error", f"Image for {self.spread[index]} not found.")

    def complete_reveal(self, index):
        """
        Completes the card reveal process by displaying the card's image
        and updating the summary if all cards are revealed.

        Parameters:
        - index: The index of the card being revealed.
        """
        card_name = self.spread[index]
        image_path = os.path.join(CARD_FOLDER, f"{card_name}.png")
        img = Image.open(image_path).resize(CARD_SIZE)
        photo = ImageTk.PhotoImage(img)

        label, _ = self.card_widgets[index]
        label.configure(image=photo)
        label.image = photo
        self.card_images[index] = photo

        self.revealed[index] = True

        if all(self.revealed):
            scrollbar = tk.Scrollbar(self.summary_frame, background="#001f3f", troughcolor="#003366")
            scrollbar.pack(side="right", fill="y")

            self.summary_text = tk.Text(
                self.summary_frame,
                wrap="word",
                font=("Helvetica", 10),
                bg="#001f3f",         # Dark blue background
                fg="white",           # White text
                relief="groove",
                bd=2,
                yscrollcommand=scrollbar.set,
                height=22
            )

            self.summary_text.insert("1.0", self.summary)
            self.summary_text.config(state="disabled")
            self.summary_text.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=self.summary_text.yview)

    def clear_screen(self):
        """
        Clears all widgets from the current screen to prepare for new content.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()