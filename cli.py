"""
Author: Ian Pearson
Date: 4/12/2025
Course: CAP4601/5600

Description:
This script provides a Command Line Interface (CLI) for the Tarot Reader application.
It allows users to select a reading category and receive a tarot reading with a summary.

Functions:
- cli_main: Main function to handle user interaction and display tarot readings.

Dependencies:
- interpreter: For generating summaries of tarot readings.
- tarot_ai: For tarot card selection using simulated annealing.
- json: For loading tarot data from JSON files.

Data Files:
- datasets/simple_tarot.json: Contains tarot card data.
- datasets/tarot_interps.json: Contains tarot card interpretations.
- datasets/general_advice.json: Contains general advice data.
"""

import json
import time
import random
from interpreter import generate_summary
from tarot_ai import simulated_annealing

# Load tarot data
with open("datasets/simple_tarot.json", "r") as f:
    tarot_data = json.load(f)

with open("datasets/tarot_interps.json", "r") as f:
    detailed_interps = json.load(f)

with open("datasets/general_advice.json", "r") as f:
    general_advice = json.load(f)

def cli_main():
    """
    Main function for the Command Line Interface (CLI) of the Tarot Reader.
    Handles user interaction, allows category selection, and displays tarot readings.
    """
    print("🔮 Welcome to the AI Tarot Reader (CLI) 🔮")
    while True:
        print("Choose a reading category:")
        categories = ["life", "love", "career"]
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.capitalize()}")

        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if choice not in range(len(categories)):
                print("Invalid choice. Please try again.\n")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            continue

        category = categories[choice]

        print("\nReading your energy... 🔮")
        time.sleep(random.uniform(1, 3))  # Delay for 1-3 seconds

        spread, _ = simulated_annealing(tarot_data, detailed_interps, category)
        summary = generate_summary(spread, detailed_interps, tarot_data, general_advice, category)

        print("\n🔮 AI Tarot Reading")
        print(f"Category: {category.capitalize()}")
        print("Cards Drawn:")
        for i, card in enumerate(spread):
            print(f"  {['Past', 'Present', 'Future'][i]}: {card}")
        print("\n✨ Summary ✨")
        print(summary)
        print("✨━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✨")

        again = input("\nWould you like to inquire again? (yes/no): ").strip().lower()
        if again != "yes":
            print("Thank you for using the AI Tarot Reader. Goodbye!")
            break

if __name__ == "__main__":
    cli_main()