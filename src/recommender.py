import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = recommend_songs(self._prefs(user), [asdict(s) for s in self.songs], k)
        by_id = {s.id: s for s in self.songs}
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(self._prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    with open(csv_path, newline="", encoding="utf-8") as f:
        songs = []
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in numeric:
                row[key] = float(row[key])
            songs.append(row)
    return songs

PLAYS_WEIGHT = 1.0
PLAYS_CAP = 10          # plays beyond this add nothing more
SEARCH_BOOST = 1.02     # slight multiplier when a search term matches the song
GENRE_WEIGHT = 1.0      # bonus for a song in the user's favorite genre
GENRE_PLAYS_WEIGHT = 0.5  # extra bonus, scaled by the share of weekly plays in that genre
FAVORITE_GENRE_PLAYS_BOOST = 0.25  # plays of favorite-genre songs count up to 25% more, growing with plays


def plays_score(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Rewards songs the user already plays, with extra weight for favorite-genre songs as plays grow.
    user_prefs["plays"] maps song id -> play count.
    Songs in the favorite genre get a small multiplier (up to 1 + FAVORITE_GENRE_PLAYS_BOOST)
    that grows with the play count, so repeat listens count a bit more there.
    """
    plays = user_prefs.get("plays", {}).get(song["id"], 0)
    if plays <= 0:
        return 0.0, ""
    progress = min(plays, PLAYS_CAP) / PLAYS_CAP
    score = PLAYS_WEIGHT * progress
    if song["genre"] == user_prefs.get("genre"):
        score *= 1 + FAVORITE_GENRE_PLAYS_BOOST * progress
    return score, f"played {plays}x"


def similarity_score(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores how close the song's attributes are to the user's taste (max 6.0)."""
    score, reasons = 0.0, []

    energy_match = 1 - abs(song["energy"] - user_prefs.get("energy", 0.5))
    score += 2.0 * energy_match
    reasons.append(f"energy {song['energy']:.2f} vs target (+{2.0 * energy_match:.2f})")

    target_acoustic = 0.8 if user_prefs.get("likes_acoustic") else 0.2
    acoustic_match = 1 - abs(song["acousticness"] - target_acoustic)
    score += 1.0 * acoustic_match
    reasons.append(f"acousticness fit (+{acoustic_match:.2f})")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.5
        reasons.append("mood matches (+1.50)")
    if song["genre"] == user_prefs.get("genre"):
        bonus = GENRE_WEIGHT + GENRE_PLAYS_WEIGHT * user_prefs.get("genre_play_share", 0.0)
        score += bonus
        reasons.append(f"genre matches (+{bonus:.2f})")
    return score, reasons


def genre_plays_share(user_prefs: Dict, songs: List[Dict]) -> float:
    """Fraction of the user's weekly plays that were songs in their favorite genre (0 to 1)."""
    plays = user_prefs.get("plays", {})
    total = sum(plays.values())
    if total <= 0:
        return 0.0
    in_genre = sum(plays.get(s["id"], 0) for s in songs if s["genre"] == user_prefs.get("genre"))
    return in_genre / total


def search_multiplier(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Returns SEARCH_BOOST if any recent search term appears in the song's text fields."""
    text = " ".join(str(song[k]) for k in ("title", "artist", "genre", "mood")).lower()
    for term in user_prefs.get("searches", []):
        if term.lower() in text:
            return SEARCH_BOOST, f"matches search '{term}' (x{SEARCH_BOOST})"
    return 1.0, ""


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scoring Rule (one song): how well does this song fit this user?

        score = (plays_score + similarity_score) * search_multiplier

    Returns (score, reasons), where reasons explain each part of the score.
    Required by recommend_songs() and src/main.py
    """
    plays, plays_reason = plays_score(user_prefs, song)
    similarity, sim_reasons = similarity_score(user_prefs, song)
    multiplier, search_reason = search_multiplier(user_prefs, song)

    reasons = ([plays_reason] if plays_reason else []) + sim_reasons
    if search_reason:
        reasons.append(search_reason)
    return (plays + similarity) * multiplier, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranking Rule (list of songs): apply the Scoring Rule to every song,
    sort by score from highest to lowest, and keep the top k.
    Returns (song_dict, score, explanation) tuples.
    Required by src/main.py
    """
    user_prefs = {**user_prefs, "genre_play_share": genre_plays_share(user_prefs, songs)}
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons) or "no strong match"))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
