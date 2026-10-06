[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5wxSp5jk)

## Team:

Bailey Goodrich and Ian Pearson

# 🔮 AI Tarot Card Reader – Project 2 (Intro to AI)

## Overview
This project is an interactive, AI-enhanced Tarot Card Reader built using Python with a GUI powered by Tkinter and Pygame. It presents users with a 3-card spread (Past, Present, Future) based on one of three themes: **Life**, **Love**, or **Career**.

Behind the scenes, the card selection and summary generation are powered by core concepts: **Simulated Annealing** and **Heuristic Scoring**.

---

## Components

### 1. **Simulated Annealing for Card Selection**
The first simulated annealing algorithm is used to intelligently **select a meaningful 3-card spread**. When a user chooses a category (like Love), the algorithm searches through all possible combinations of tarot cards to find a trio with strong thematic alignment. 

#### Heuristic Scoring for Card Selection:
- **Keyword Matching**: Each card's interpretation is scored based on the presence of emotionally resonant keywords fetched dynamically from the `keyword_map.json` file (e.g., "heart", "truth", "growth").
- **Theme Diversity**: Cards with unique themes are rewarded, while repetitive themes are penalized.
- **Duplicate Phrase Penalty**: Repeated phrases across cards are penalized to ensure variety in the spread.
- **Spread Reuse Penalty**: Frequently repeated spreads are penalized to encourage diversity.

This creates the illusion of a divinely chosen spread, but it's really algorithms behind the curtain.

---

### 2. **Simulated Annealing for Summary Optimization**
The second simulated annealing algorithm is used to **generate an optimized summary** of the reading. This includes selecting the most relevant themes, meanings, and advice for the chosen category.

#### Heuristic Scoring for Summary Optimization:
- **Category Relevance**: Themes and advice that align with the chosen category (Life, Love, or Career) are given higher weight using keywords dynamically fetched from the `keyword_map.json` file.
- **Coherence**: The algorithm ensures that the summary is coherent and avoids repetitive themes or advice.
- **Keyword Diversity**: Summaries with a variety of relevant keywords are rewarded.
- **Length Optimization**: Summaries are penalized if they are too short or too long, ensuring a concise yet meaningful output.

This ensures that the summary feels personalized and meaningful, enhancing the user's experience.

---

## Features

- **3-Card Tarot Spread**: Past, Present, and Future cards drawn for Life, Love, or Career.
- **Guided Card Selection**: Meaningful spreads selected via simulated annealing based on theme relevance and keyword matching.
- **Optimized Reading Summary**: Summaries generated using a second simulated annealing algorithm for coherence and relevance.
- **Dynamic Keyword Mapping**: Keywords for each category are dynamically fetched from the `keyword_map.json` file to ensure alignment with the chosen theme.
- **Card Flip Animation**: Visuals and sound effects simulate flipping physical tarot cards.
- **Mystical Interpretations**: Predefined card meanings sourced from a JSON dataset.
- **General Advice Integration**: Provides actionable insights based on the chosen category.

---

## Project Structure
```text
project/
│
├── assets/                   # Tarot card images and flip sound
│   ├── card_back.png
│   ├── The Fool.png
│   ├── ...
│   └── flip_sound.wav
│
├── datasets/
│   ├── simple_tarot.json     # All card meanings (categorized by life/love/career)
│   ├── tarot_interps.json    # Detailed card interpretations (themes, advice, etc.)
│   ├── general_advice.json   # General advice for life, love, and career
│   └── keyword_map.json      # Category-specific keywords for heuristic scoring
│
├── gui.py                    # Main GUI logic with Tkinter and Pygame
├── tarot_ai.py               # Simulated Annealing logic for card selection
├── interpreter.py            # Summary generation with simulated annealing
├── cli.py                    # Command-line interface for tarot readings
├── main.py                   # Entry point – runs the actual tarot reader
├── test_ai.py                # Unit tests for components
└── test_gui.py               # GUI testing with randomized spread (optional)

```

---

## Requirements

- Python 3.x
- Libraries:
    - `tkinter` (Built into Python)
    - `Pillow` (Image Handling)
    - `pygame` (Ease of GUI)

### Install dependencies

```bash
pip install -r requirements.txt
```

### WSL audio setup (optional, for GUI sound effects)

On WSL, `pygame.mixer` needs PulseAudio client tools to reach WSLg's audio server:

```bash
sudo apt install -y pulseaudio-utils alsa-utils
```

Verify with `pactl info` and `aplay /usr/share/sounds/alsa/Front_Center.wav`. If this step is skipped, the GUI still runs but without sound effects.

---

## How to Run

You can interact with the Tarot Reader using either the **Command-Line Interface (CLI)** or the **Graphical User Interface (GUI)**.

### Run the CLI Version (For the Linux Server)

The CLI version provides a text-based interaction for generating tarot spreads and summaries:

```bash
python3 cli.py
```

Follow the prompts to select a category (Life, Love, or Career) and view the generated tarot spread and summary.

---

### Run the GUI Version (For Inclass Demonstration)

The GUI version offers a visual and interactive experience with card animations and sound effects:

```bash
python gui.py
```

Use the GUI to select a category, flip cards, and view the generated tarot spread and summary.

---

### Run Unit Tests

To test the components and ensure everything is working as expected:

```bash
python test_ai.py
```

For GUI-specific testing with randomized spreads:

```bash
python test_gui.py
```

---

## Acknowledgments

Card images sourced from the Gummy Bear Tarot Deck © U.S. Games Systems, Inc.

Special thanks to Python, Tkinter, and the mystical vibes of algorithms.