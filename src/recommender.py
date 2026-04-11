from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv


MODE_WEIGHTS = {
    # Genre-first: prioritize genre matching more than mood or energy.
    "genre_first": {"genre": 3.0, "mood": 1.5, "energy": 2.0},
    # Mood-first: prioritize mood matching more than genre or energy.
    "mood_first": {"genre": 1.5, "mood": 3.0, "energy": 2.0},
    # Energy-focused: prioritize energy similarity more than genre or mood.
    "energy_focused": {"genre": 1.5, "mood": 1.5, "energy": 3.0},
}


def get_mode_weights(scoring_mode: str) -> Dict[str, float]:
    """Return the weight settings for a scoring mode."""
    return MODE_WEIGHTS.get(scoring_mode, MODE_WEIGHTS["genre_first"])

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

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            score = 0.0

            if song.mood.lower() == user.favorite_mood.lower():
                score += 5

            energy_diff = abs(song.energy - user.target_energy)
            score += max(0, 3 - energy_diff * 3)

            if song.genre.lower() == user.favorite_genre.lower():
                score += 2

            if user.likes_acoustic and song.acousticness >= 0.5:
                score += 1

            scored.append((score, song))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []

        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("matching mood")
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("matching genre")
        if abs(song.energy - user.target_energy) <= 0.2:
            reasons.append("similar energy")
        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("acoustic style")

        if not reasons:
            return "Recommended based on overall similarity."
        return "Recommended because of " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": int(row["popularity"]),
                "release_decade": row["release_decade"],
                "mood_tag": row["mood_tag"],
                "instrumentalness": float(row["instrumentalness"]),
                "explicit": row["explicit"].strip().lower() == "true",
            })

    return songs

def score_song(user_prefs: Dict, song: Dict, scoring_mode: str = "genre_first") -> Tuple[float, List[str]]:
    """Score one song against user preferences and return score with reasons."""
    weights = get_mode_weights(scoring_mode)
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    # Energy is always used, but the selected mode changes how strongly it matters.
    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0.0, weights["energy"] * (1.0 - energy_diff))
    score += energy_score
    if energy_score > 0:
        reasons.append(f"energy similarity (+{energy_score:.1f})")

    if user_prefs["likes_acoustic"] and song["acousticness"] >= 0.5:
        score += 1.0
        reasons.append("acoustic preference match (+1.0)")

    # --- Advanced features (Challenge 1) ---

    if user_prefs.get("preferred_decade") and song["release_decade"] == user_prefs["preferred_decade"]:
        score += 1.5
        reasons.append(f"release decade match ({song['release_decade']}) (+1.5)")

    if user_prefs.get("preferred_mood_tag") and song["mood_tag"] == user_prefs["preferred_mood_tag"]:
        score += 1.5
        reasons.append(f"mood tag match ({song['mood_tag']}) (+1.5)")

    if user_prefs.get("target_popularity") is not None:
        pop_diff = abs(song["popularity"] - user_prefs["target_popularity"])
        pop_score = max(0.0, 1.5 * (1.0 - pop_diff / 100))
        score += pop_score
        if pop_score > 0:
            reasons.append(f"popularity similarity (+{pop_score:.1f})")

    if user_prefs.get("likes_instrumental") and song["instrumentalness"] >= 0.5:
        score += 1.0
        reasons.append("instrumental preference match (+1.0)")

    if user_prefs.get("allows_explicit") is not None:
        if user_prefs["allows_explicit"] == song["explicit"]:
            score += 0.5
            reasons.append("explicit preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, scoring_mode: str = "genre_first") -> List[Tuple[Dict, float, str]]:
    """Return the top k songs sorted by highest recommendation score."""
    scored_songs = [
        (
            song,
            score,
            "Recommended because of " + ", ".join(reasons)
            if reasons
            else "Recommended based on overall similarity.",
        )
        for song in songs
        for score, reasons in [score_song(user_prefs, song, scoring_mode)]
    ]

    scored_songs.sort(key=lambda item: item[1], reverse=True)

    # Diversity penalty: lightly reduce scores when we keep repeating the same artist or genre.
    # This helps the top recommendations feel less repetitive without changing the overall scoring model.
    selected_songs = []
    selected_artists = set()
    selected_genre_counts = {}

    for song, score, reasons in scored_songs:
        adjusted_score = score
        penalty_notes = []

        if song["artist"] in selected_artists:
            adjusted_score -= 1.0
            penalty_notes.append("artist diversity penalty (-1.0)")

        current_genre_count = selected_genre_counts.get(song["genre"], 0)
        if current_genre_count > 1:
            adjusted_score -= 0.5
            penalty_notes.append("genre diversity penalty (-0.5)")

        final_reasons = reasons
        if penalty_notes:
            final_reasons = reasons + "; " + ", ".join(penalty_notes)

        selected_songs.append((song, adjusted_score, final_reasons))
        selected_artists.add(song["artist"])
        selected_genre_counts[song["genre"]] = current_genre_count + 1

        if len(selected_songs) == k:
            break

    return selected_songs