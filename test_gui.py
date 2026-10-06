"""
Author: Bailey GoodRick
Date: 4/8/2025
Course: CAP4601/5600

This script tests the GUI functionality of the Tarot Reader application.
It overrides the tarot spread generation with a random spread generator for testing purposes.

Functions:
- generate_random_spread: Generates a random tarot card spread for testing.
- test_start_reading: Overrides the start_reading method of the TarotApp class for testing.

Dependencies:
- tkinter: For GUI components.
- gui: Contains the TarotApp class.
- random: For generating random spreads.
- json: For loading tarot data from JSON files.

Data Files:
- datasets/simple_tarot.json: Contains tarot card data.

Usage:
Run this script to launch the GUI with the patched functionality for testing purposes.
"""

import tkinter as tk
from gui import TarotApp
import random
import json

# Load tarot data
with open("datasets/simple_tarot.json", "r") as f:
    tarot_data = json.load(f)

# Temporary override of tarot spread generator
def generate_random_spread():
    """
    Generate a random tarot card spread for testing.

    @return A list of three randomly selected tarot cards.
    """
    return random.sample(list(tarot_data.keys()), 3)

# Patch the TarotApp class for testing
original_start_reading = TarotApp.start_reading

def test_start_reading(self, category):
    """
    Overrides the start_reading method of the TarotApp class for testing purposes.
    Replaces tarot spread generation with a random spread generator.

    Parameters:
    - category: The selected reading category (e.g., 'life', 'love', 'career').
    """
    self.category = category
    self.spread = generate_random_spread()
    self.show_loading()
    self.root.after(1500, self.show_spread)

TarotApp.start_reading = test_start_reading

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()