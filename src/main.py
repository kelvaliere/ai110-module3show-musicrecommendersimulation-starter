"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main (project root)
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs      # python main.py (from src/)

SONGS_CSV = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


def main() -> None:
    """Prints a ranked list of songs with scores and bulleted reasons, runnable from the project root or src/."""
    songs = load_songs(str(SONGS_CSV))

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
        "plays": {10: 4},         # song id -> play count
        "searches": ["neon"],     # recent search terms
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print("\n" + "=" * width)
    print("TOP RECOMMENDATIONS".center(width))
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']}".ljust(width - 12) + f"Score: {score:5.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print("\n" + "=" * width + "\n")


if __name__ == "__main__":
    main()
