"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from src.recommender import load_songs, recommend_songs


def choose_scoring_mode() -> str:
    """Ask the user which scoring mode to use."""
    print("Choose a scoring mode:")
    print("1. genre_first")
    print("2. mood_first")
    print("3. energy_focused")

    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == "2":
        return "mood_first"
    if choice == "3":
        return "energy_focused"
    return "genre_first"


def print_table(recommendations):
    """Print recommendations as a formatted ASCII table."""
    REASON_WRAP_WIDTH = 45

    # Build rows, wrapping the reason into multiple lines if needed
    rows = []
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        reason_text = reasons.replace("Recommended because of ", "")
        reason_lines = textwrap.wrap(reason_text, REASON_WRAP_WIDTH) or [""]
        rows.append((str(rank), song["title"], song["artist"], f"{score:.2f}", reason_lines))

    headers = ("Rank", "Title", "Artist", "Score", "Reason")

    # Compute each column width from headers and row data
    col_widths = [len(h) for h in headers]
    for rank, title, artist, score, reason_lines in rows:
        for i, cell in enumerate([rank, title, artist, score]):
            col_widths[i] = max(col_widths[i], len(cell))
        col_widths[4] = max(col_widths[4], max(len(line) for line in reason_lines))

    # Helper to build a separator line
    def separator():
        return "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

    # Helper to build a data row
    def table_row(cells):
        return "|" + "|".join(f" {cell:<{w}} " for cell, w in zip(cells, col_widths)) + "|"

    print(separator())
    print(table_row(headers))
    print(separator())
    for rank, title, artist, score, reason_lines in rows:
        # First line includes all columns
        print(table_row((rank, title, artist, score, reason_lines[0])))
        # Any extra wrapped lines only fill the Reason column
        for line in reason_lines[1:]:
            print(table_row(("", "", "", "", line)))
    print(separator())


def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    scoring_mode = choose_scoring_mode()
    print(f"Using scoring mode: {scoring_mode}")

    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False
    }

    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True
    }

    metal_relaxed_paradox = {
        "favorite_genre": "metal",
        "favorite_mood": "relaxed",
        "target_energy": 0.95,
        "likes_acoustic": True
    }

    profiles = [
        ("High Energy Pop", high_energy_pop),
        ("Chill Lofi", chill_lofi),
        ("Metal Relaxed Paradox", metal_relaxed_paradox),
    ]

    for label, profile in profiles:
        print(f"\n{'=' * 40}")
        print(f" {label}")
        print(f"{'=' * 40}")

        recommendations = recommend_songs(profile, songs, k=5, scoring_mode=scoring_mode)
        print_table(recommendations)


if __name__ == "__main__":
    main()
