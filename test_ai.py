"""
Author: Ian Pearson
Date: 4/12/2025
Course: CAP4601/5600

Description:
This script tests the functionality of the tarot card selection and summary generation.
It evaluates the performance of the selection algorithm and the coherence of generated summaries.

Functions:
- test_simulated_annealing: Runs multiple simulations to test the tarot card selection algorithm.

Dependencies:
- tarot_ai: For tarot card selection and evaluation.
- interpreter: For generating summaries of tarot readings.
- json: For loading tarot data from JSON files.
- collections.Counter: For tracking card and spread statistics.
- time: For measuring runtime performance.

Data Files:
- datasets/simple_tarot.json: Contains tarot card data.
- datasets/tarot_interps.json: Contains tarot card interpretations.
- datasets/general_advice.json: Contains general advice data.
- datasets/keyword_map.json: Contains category-specific keywords.
"""

import json
import time
from collections import Counter
from tarot_ai import simulated_annealing, evaluate_state
from interpreter import generate_summary

# Load tarot data
with open("datasets/simple_tarot.json", "r") as f:
    tarot_data = json.load(f)

with open("datasets/tarot_interps.json", "r") as f:
    detailed_interps = json.load(f)

with open("datasets/general_advice.json", "r") as f:
    general_advice = json.load(f)

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

def test_simulated_annealing(runs, category):
    """
    Tests the simulated annealing algorithm by running it multiple times.
    Evaluates the quality of generated tarot spreads and their summaries.

    Parameters:
    - runs: Number of times to run the simulation.
    - category: The category to focus on for the test (e.g., 'life', 'love', 'career').

    Outputs:
    - Statistics on card pull frequency, spread diversity, and runtime performance.
    """
    card_counter = Counter()
    summary_lengths = []
    unique_spreads = set()
    spread_scores = []
    keyword_counts = Counter()
    runtimes = []
    coherence_scores = []
    spread_counter = Counter()

    print(f"Running {runs} simulations for category: {category.capitalize()}...\n")

    for _ in range(runs):
        # Measure runtime
        start_time = time.time()
        # Run simulated annealing to select a spread
        spread, _ = simulated_annealing(tarot_data, detailed_interps, category)  # Updated to handle the new return value
        runtimes.append(time.time() - start_time)

        unique_spreads.add(tuple(sorted(spread)))
        spread_counter[tuple(sorted(spread))] += 1

        # Evaluate the spread quality
        spread_score = evaluate_state(spread, category, tarot_data, detailed_interps)  # Updated to include interp_data
        spread_scores.append(spread_score)

        # Tally how many times each card is pulled
        card_counter.update(spread)

        # Generate a summary and record its length
        summary = generate_summary(spread, detailed_interps, tarot_data, general_advice, category)
        summary_lengths.append(len(summary))

        # Count category-specific keywords in the summary
        keywords = get_keywords_by_category(category)
        for keyword in keywords:
            keyword_counts[keyword] += summary.lower().count(keyword)

        # Filter themes and advice based on the cards in the spread
        unique_themes = set(
            theme
            for card in spread
            for theme in detailed_interps.get(card, {}).get("themes", [])
            if isinstance(detailed_interps.get(card, {}).get("themes"), list)
        )
        unique_advice = set(
            detailed_interps.get(card, {}).get("advice")
            for card in spread
            if isinstance(detailed_interps.get(card, {}).get("advice"), str)
        )
        coherence_scores.append(len(unique_themes) + len(unique_advice))

    # Display results
    print("Card Pull Frequency:")
    for card, count in card_counter.most_common():
        print(f"  {card}: {count} times")

    # Display the number of unique cards pulled
    total_cards = len(tarot_data)  # Total number of cards in the deck
    unique_cards_pulled = len(card_counter)
    print(f"\nUnique Cards Pulled: {unique_cards_pulled}/{total_cards} (higher is better for diversity)")

    print("\nUnique Spreads Generated:", len(unique_spreads), f"(higher is better for spread diversity)")

    print("Average Summary Length:", sum(summary_lengths) / len(summary_lengths))
    print("Shortest Summary Length:", min(summary_lengths))
    print("Longest Summary Length:", max(summary_lengths))

    # Display spread quality metrics
    print("\nSpread Quality Metrics (higher is better, no fixed maximum):")
    print(f"  Average Spread Score: {sum(spread_scores) / len(spread_scores):.2f}")
    print(f"  Minimum Spread Score: {min(spread_scores)} (lower indicates a weaker spread)")
    print(f"  Maximum Spread Score: {max(spread_scores)} (higher indicates a stronger spread)")

    # Display runtime metrics
    print("\nRuntime Performance (lower is better):")
    print(f"  Average Runtime per Run: {sum(runtimes) / len(runtimes):.4f} seconds")
    print(f"  Fastest Run: {min(runtimes):.4f} seconds")
    print(f"  Slowest Run: {max(runtimes):.4f} seconds")

    # Analyze spread diversity
    print("\nSpread Diversity Analysis:")
    for spread in list(unique_spreads)[:5]:  # Show up to 5 unique spreads
        print(f"  {spread}")

    # Display most common spreads
    print("\nMost Common Spreads:")
    for spread, count in spread_counter.most_common(5):  # Show top 5 most common spreads
        print(f"  {spread}: {count} times")

    # Display keyword coverage
    print("\nCategory-Specific Keyword Coverage (higher means better alignment with the category, no fixed maximum):")
    for keyword, count in keyword_counts.items():
        print(f"  {keyword}: {count} occurrences")

    # Display summary coherence metrics
    print("\nSummary Coherence Metrics (higher is better):")
    print(f"  Average Unique Themes/Advice per Summary: {sum(coherence_scores) / len(coherence_scores):.2f}")
    print(f"  Minimum Unique Themes/Advice: {min(coherence_scores)} (lower indicates repetition)")
    print(f"  Maximum Unique Themes/Advice: {max(coherence_scores)} (higher indicates more variety)")

if __name__ == "__main__":
    try:
        runs = int(input("Enter the number of runs for each category: "))
        if runs <= 0:
            raise ValueError("Number of runs must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit(1)

    # Run the test for the specified number of simulations in each category
    for category in ["life", "love", "career"]:
        test_simulated_annealing(runs, category)
        print("\n" + "=" * 60 + "\n")