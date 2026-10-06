"""
Author: Ian Pearson
Date: 4/9/2025
Course: CAP4601/5600

Description:
This module provides functionality for interpreting tarot card spreads using simulated annealing
and generating summaries based on themes, meanings, and advice.

Functions:
- calculate_score: Calculates the score of a solution based on relevance and coherence.
- simulated_annealing_for_summary: Optimizes the selection of themes, meanings, and advice.
- generate_summary: Generates a summary for a tarot card spread.
- initialize_solution: Initializes a solution with random selections.
- generate_neighbor_solution: Generates a neighboring solution by modifying one card's data or advice.
- generate_summary_body: Creates the main body of the summary.
- generate_advice_section: Creates the advice section of the summary.
- generate_general_advice_section: Creates the general advice section of the summary.

Dependencies:
- random: For generating random solutions and neighbors.
- math: For calculations in simulated annealing.
- collections.Counter: For tracking themes and advice.
- json: For loading keyword map data.

Data Files:
- datasets/tarot_interps.json: Contains tarot card interpretations.
- datasets/general_advice.json: Contains general advice data.
- datasets/keyword_map.json: Contains keywords for scoring and summary generation.
"""

from collections import Counter
import random
import math
import json

# Load the keyword map
with open("datasets/keyword_map.json", "r") as f:
    keyword_map = json.load(f)

def get_keywords_by_category(category):
    """
    Fetch keywords for a given category from the keyword map.

    @param category: The category to focus on (e.g., 'life', 'love', 'career').

    @return A set of keywords relevant to the category.
    """
    return set(keyword_map.get(category, []))


def calculate_score(solution, category):
    """
    Calculate the score of a solution based on relevance and coherence.

    @param solution: The current solution being evaluated.
    @param category: The category to focus on for scoring (e.g., 'life', 'love', 'career').

    @return The score of the solution.
    """
    score = 0
    seen_themes = set()
    seen_advice = set()
    matched_keywords = set()

    # Fetch keywords dynamically based on the category
    keywords = get_keywords_by_category(category)

    for card, data in solution["cards"].items():
        # Category-related bonus for theme matching
        if category.lower() in data["themes"].lower():
            score += 5
        score += len(data["themes"]) * 2
        score += len(data["meaning"])
        score += len(data["advice"])

        if data["themes"] in seen_themes:
            score -= 3
        seen_themes.add(data["themes"])

        # Extract keywords from meaning for extra alignment scoring
        for keyword in keywords:
            if keyword in data["meaning"].lower():
                matched_keywords.add(keyword)

    # General advice bonus
    for advice in solution["general_advice"]:
        if category.lower() in advice.lower():
            score += 4
        if advice in seen_advice:
            score -= 2
        seen_advice.add(advice)

    # Reward keyword diversity
    score += len(matched_keywords) * 2

    # Summary length check
    summary_length = sum(len(data["meaning"]) + len(data["advice"]) for data in solution["cards"].values())
    if summary_length > 900:
        score -= (summary_length - 900) * 0.25
    elif summary_length < 600:
        score -= (600 - summary_length) * 0.25

    return score


def simulated_annealing_for_summary(spread, interps, simple_tarot, general_advice, category, max_iterations=1000, initial_temp=100, cooling_rate=0.95):
    """
    Use simulated annealing to optimize the selection of themes, meanings, and advice for the summary.

    @param spread: List of tarot cards in the spread.
    @param interps: Dictionary containing interpretations for each card.
    @param simple_tarot: Additional tarot data (not used in this function).
    @param general_advice: Dictionary of general advice categorized by themes.
    @param category: The category to focus on for optimization.
    @param max_iterations: Maximum number of iterations for the algorithm.
    @param initial_temp: Initial temperature for simulated annealing.
    @param cooling_rate: Cooling rate for temperature reduction.

    @return Optimized solution containing selected themes, meanings, and advice.
    """
    current_solution = initialize_solution(spread, interps, general_advice, category)
    current_score = calculate_score(current_solution, category)
    temperature = initial_temp

    for _ in range(max_iterations):
        neighbor = generate_neighbor_solution(current_solution, spread, interps, general_advice, category)
        neighbor_score = calculate_score(neighbor, category)

        if neighbor_score > current_score or random.random() < math.exp((neighbor_score - current_score) / temperature):
            current_solution, current_score = neighbor, neighbor_score

        temperature *= cooling_rate

    return current_solution


def initialize_solution(spread, interps, general_advice, category):
    """
    Initialize the solution with random selections for themes, meanings, and advice.

    @param spread: List of tarot cards in the spread.
    @param interps: Dictionary containing interpretations for each card.
    @param general_advice: Dictionary of general advice categorized by themes.
    @param category: The category to focus on for optimization.

    @return A dictionary representing the initial solution.
    """
    solution = {"cards": {}, "general_advice": []}
    for card in spread:
        card_data = interps.get(card, {})
        themes = card_data.get("themes", [])
        meanings = card_data.get("meanings", [])
        advices = card_data.get("advice", [])  # Correctly reference "advice" field

        solution["cards"][card] = {
            "themes": random.choice(themes) if themes else "No themes available",
            "meaning": random.choice(meanings) if meanings else "Meaning not found.",
            "advice": random.choice(advices) if advices else "No specific advice available for this card.",
        }
    solution["general_advice"] = random.sample(general_advice.get(category, []), min(2, len(general_advice.get(category, []))))
    return solution


def generate_neighbor_solution(current_solution, spread, interps, general_advice, category):
    """
    Generate a neighboring solution by modifying one card's data or general advice.

    @param current_solution: The current solution being optimized.
    @param spread: List of tarot cards in the spread.
    @param interps: Dictionary containing interpretations for each card.
    @param general_advice: Dictionary of general advice categorized by themes.
    @param category: The category to focus on for optimization.

    @return A dictionary representing the neighboring solution.
    """
    neighbor_solution = {"cards": current_solution["cards"].copy(), "general_advice": current_solution["general_advice"][:]}
    if random.random() < 0.5:
        card = random.choice(spread)
        card_data = interps.get(card, {})
        themes = card_data.get("themes", [])
        meanings = card_data.get("meanings", [])
        advices = card_data.get("advices", [])
        if themes:
            neighbor_solution["cards"][card]["themes"] = random.choice(themes)
        if meanings:
            neighbor_solution["cards"][card]["meaning"] = random.choice(meanings)
        if advices:
            neighbor_solution["cards"][card]["advice"] = random.choice(advices)
    else:
        neighbor_solution["general_advice"] = random.sample(general_advice.get(category, []), min(2, len(general_advice.get(category, []))))
    return neighbor_solution


def generate_summary(spread, interps, simple_tarot, general_advice, category="general"):
    """
    Generates a summary for a tarot card spread based on the selected category.
    Uses optimized data from simulated annealing to create a coherent summary.

    Parameters:
    - spread: List of tarot cards in the spread.
    - interps: Dictionary containing interpretations for each card.
    - simple_tarot: Additional tarot data.
    - general_advice: Dictionary of general advice categorized by themes.
    - category: The category to focus on for the summary (default is 'general').

    Returns:
    - A string containing the generated summary.
    """
    if len(spread) != 3:
        return "Your reading is incomplete."

    optimized_summary = simulated_annealing_for_summary(spread, interps, simple_tarot, general_advice, category)
    summary_lines = generate_summary_body(spread, optimized_summary)
    advice_summary = generate_advice_section(optimized_summary)
    general_advice_summary = generate_general_advice_section(optimized_summary)

    return (
        f"{' '.join(summary_lines)}\n"
        f"{advice_summary}\n"
        f"{general_advice_summary}"
    )


def generate_summary_body(spread, optimized_summary):
    """
    Generate the main body of the summary for the tarot card spread.

    @param spread: List of tarot cards in the spread.
    @param optimized_summary: Optimized summary data.

    @return A list of strings representing the main body of the summary.
    """
    positions = ["Past", "Present", "Future"]
    summary_lines = []
    for i, card in enumerate(spread):
        card_data = optimized_summary["cards"][card]
        summary_lines.append(
            f"\n🔹 {positions[i].upper()} - {card} 🔹\n{card_data['meaning']}\n"
        )
    return summary_lines


def generate_advice_section(optimized_summary):
    """
    Generate the advice section of the summary.

    @param optimized_summary: Optimized summary data.

    @return A string containing the advice section.
    """
    advice_lines = [
        card_data["advice"]
        for card_data in optimized_summary["cards"].values()
        if card_data["advice"]
    ]
    return "\nGuidance:\n" + "\n".join(f"- {advice}" for advice in advice_lines) if advice_lines else ""


def generate_general_advice_section(optimized_summary):
    """
    Generate the general advice section of the summary.

    @param optimized_summary: Optimized summary data.

    @return A string containing the general advice section.
    """
    general_advice_lines = optimized_summary["general_advice"]
    return "\nGeneral Advice:\n" + "\n".join(f"- {advice}" for advice in general_advice_lines) if general_advice_lines else ""
