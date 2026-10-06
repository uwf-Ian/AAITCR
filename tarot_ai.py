"""
Author: Ian Pearson
Date: 4/8/2025
Course: CAP4601/5600

Description:
This module implements functionality for tarot card selection and evaluation using simulated annealing.
It includes methods for generating random states, evaluating states, and optimizing card selection.

Functions:
- get_random_state: Selects a random set of tarot cards.
- evaluate_state: Evaluates a state based on keywords and theme diversity.
- get_neighbor: Generates a neighboring state by replacing one card.
- simulated_annealing: Optimizes card selection using simulated annealing.

Dependencies:
- random: For generating random states and neighbors.
- math: For calculations in simulated annealing.
- collections.Counter: For tracking used spreads.
- json: For loading keyword map data.

Data Files:
- datasets/simple_tarot.json: Contains tarot card data.
- datasets/tarot_interps.json: Contains tarot card interpretations.
- datasets/keyword_map.json: Contains keywords for each category.
"""

import random
import math
import json
from collections import Counter

# Load the keyword map
with open("datasets/keyword_map.json", "r") as f:
    keyword_map = json.load(f)

used_spreads_global = Counter()

def get_random_state(deck):
    """
    Select a random set of three tarot cards from the deck.

    @param deck: Dictionary representing the tarot card deck.
    
    @return A list of three randomly selected tarot cards.
    """
    return random.sample(list(deck.keys()), 3)

def get_keywords_by_category(category):
    """
    Fetch keywords for a given category from the keyword map.

    @param category: The category to focus on (e.g., 'life', 'love', 'career').

    @return A set of keywords relevant to the category.
    """
    return set(keyword_map.get(category, []))

def evaluate_state(state, category, deck, interp_data, used_spreads=None):
    """
    Evaluate a state based on keyword relevance, theme diversity, and unique advice strength.

    @param state: List of tarot cards in the current state.
    @param category: The category to focus on for evaluation ('life', 'love', or 'career').
    @param deck: Dictionary representing the tarot card deck (e.g., simple_tarot).
    @param interp_data: Detailed interpretation data (e.g., tarot_interps.json).
    @param used_spreads: Counter to track how often spreads have been used (optional).

    @return A score representing the quality of the state.
    """
    score = 0
    seen_phrases = set()
    seen_themes = set()
    seen_cards = set()
    matched_keywords = set()

    if used_spreads is None:
        used_spreads = Counter()

    # Fetch keywords dynamically based on the category
    keywords = get_keywords_by_category(category)

    for card in state:
        if card in seen_cards:
            score -= 3
        seen_cards.add(card)

        for time in ['past', 'present', 'future']:
            phrase = deck[card][category][time]
            for keyword in keywords:
                if keyword in phrase.lower():
                    matched_keywords.add(keyword)
            if phrase in seen_phrases:
                score -= 2
            seen_phrases.add(phrase)

        themes = interp_data.get(card, {}).get('themes', [])
        for theme in themes:
            if theme in seen_themes:
                score -= 2
            else:
                score += 3
            seen_themes.add(theme)

    # Bonus for keyword variety and card diversity
    score += len(matched_keywords) * 2
    score += len(seen_cards) * 2

    # Penalize frequently repeated spreads
    spread_key = tuple(sorted(state))
    repeat_penalty = used_spreads[spread_key]
    score -= repeat_penalty * 2  # Stronger penalty for overused combos

    return score


def get_neighbor(state, deck):
    """
    Generate a neighboring state by replacing one card in the current state.

    @param state: List of tarot cards in the current state.
    @param deck: Dictionary representing the tarot card deck.

    @return A new state with one card replaced.
    """
    new_state = state[:]
    new_card = random.choice([c for c in deck if c not in new_state])
    replace_idx = random.randint(0, 2)
    new_state[replace_idx] = new_card
    return new_state

def simulated_annealing(deck, interp_data, category, iterations=500, temp=100.0, cooling_rate=0.90):
    """
    Optimizes tarot card selection using simulated annealing.

    Parameters:
    - deck: Tarot deck (simple_tarot.json structure).
    - interp_data: Detailed interpretation data (tarot_interps.json).
    - category: The category to focus on ('life', 'love', 'career').
    - iterations: Number of steps for the algorithm.
    - temp: Initial temperature for simulated annealing.
    - cooling_rate: Cooling rate for temperature reduction.

    Returns:
    - A tuple (best_state, best_score) representing the optimal card spread and its score.
    """
    global used_spreads_global

    current = random.sample(list(deck.keys()), 3)
    current_score = evaluate_state(current, category, deck, interp_data, used_spreads=used_spreads_global)

    for _ in range(iterations):
        temp *= cooling_rate
        neighbor = get_neighbor(current, deck)
        neighbor_score = evaluate_state(neighbor, category, deck, interp_data, used_spreads=used_spreads_global)
        delta = neighbor_score - current_score

        if delta > 0 or math.exp(delta / temp) > random.random():
            current, current_score = neighbor, neighbor_score

    used_spreads_global[tuple(sorted(current))] += 1
    return current, current_score
