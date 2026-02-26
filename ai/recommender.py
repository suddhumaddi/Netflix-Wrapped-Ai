"""
Netflix Wrapped AI — Recommendation Engine
Behavioral-embedding-based show recommendations.
"""

from typing import Dict, List, Any


# Curated show database with behavioral tags
SHOW_DATABASE = [
    {"title": "Dark",             "genre": "Sci-Fi",    "binge": 90, "series": True,  "intensity": 90, "night": 85},
    {"title": "Mindhunter",       "genre": "Crime",     "binge": 75, "series": True,  "intensity": 85, "night": 80},
    {"title": "The Leftovers",    "genre": "Drama",     "binge": 70, "series": True,  "intensity": 95, "night": 88},
    {"title": "Severance",        "genre": "Thriller",  "binge": 85, "series": True,  "intensity": 88, "night": 78},
    {"title": "The Wire",         "genre": "Crime",     "binge": 85, "series": True,  "intensity": 80, "night": 70},
    {"title": "Succession",       "genre": "Drama",     "binge": 80, "series": True,  "intensity": 75, "night": 65},
    {"title": "Beef",             "genre": "Drama",     "binge": 95, "series": True,  "intensity": 85, "night": 70},
    {"title": "Squid Game",       "genre": "Thriller",  "binge": 90, "series": True,  "intensity": 90, "night": 80},
    {"title": "Black Mirror",     "genre": "Sci-Fi",    "binge": 60, "series": True,  "intensity": 88, "night": 90},
    {"title": "Ozark",            "genre": "Crime",     "binge": 85, "series": True,  "intensity": 82, "night": 75},
    {"title": "Wednesday",        "genre": "Mystery",   "binge": 88, "series": True,  "intensity": 65, "night": 72},
    {"title": "The Bear",         "genre": "Drama",     "binge": 92, "series": True,  "intensity": 88, "night": 68},
    {"title": "Manifest",         "genre": "Sci-Fi",    "binge": 85, "series": True,  "intensity": 70, "night": 65},
    {"title": "Stranger Things",  "genre": "Sci-Fi",    "binge": 88, "series": True,  "intensity": 75, "night": 80},
    {"title": "Narcos",           "genre": "Crime",     "binge": 80, "series": True,  "intensity": 80, "night": 72},
    {"title": "The Crown",        "genre": "Drama",     "binge": 65, "series": True,  "intensity": 70, "night": 60},
    {"title": "Glass Onion",      "genre": "Mystery",   "binge": 40, "series": False, "intensity": 75, "night": 70},
    {"title": "The Irishman",     "genre": "Crime",     "binge": 30, "series": False, "intensity": 85, "night": 88},
    {"title": "Marriage Story",   "genre": "Drama",     "binge": 30, "series": False, "intensity": 90, "night": 75},
    {"title": "Parasite",         "genre": "Thriller",  "binge": 35, "series": False, "intensity": 92, "night": 82},
    {"title": "1899",             "genre": "Sci-Fi",    "binge": 82, "series": True,  "intensity": 88, "night": 85},
    {"title": "Better Call Saul", "genre": "Crime",     "binge": 75, "series": True,  "intensity": 85, "night": 72},
    {"title": "Lupin",            "genre": "Thriller",  "binge": 88, "series": True,  "intensity": 72, "night": 70},
    {"title": "The Night Agent",  "genre": "Thriller",  "binge": 85, "series": True,  "intensity": 72, "night": 68},
    {"title": "From",             "genre": "Sci-Fi",    "binge": 80, "series": True,  "intensity": 85, "night": 82},
]


def generate_recommendations(metrics: Dict, watched_titles: List[str], n: int = 6) -> List[Dict[str, Any]]:
    """
    Score and rank shows by behavioral compatibility with user's feature vector.
    Excludes already-watched titles.
    """
    bq = metrics.get('binge_quotient', 50)
    no = metrics.get('night_owl_index', 30)
    sl = metrics.get('series_loyalty', 60)
    en = metrics.get('content_diversity_pct', 50)

    watched_lower = {t.lower() for t in watched_titles}
    candidates = [s for s in SHOW_DATABASE if s['title'].lower() not in watched_lower]

    scored = []
    for show in candidates:
        # Weighted behavioral compatibility score
        score = (
            _proximity(bq, show['binge'])     * 0.35 +
            _proximity(no, show['night'])      * 0.25 +
            _series_match(sl, show['series'])  * 0.25 +
            show['intensity'] / 100            * 0.15
        )

        # Add diversity bonus if high entropy
        if en > 60 and show.get('genre') not in ['Crime', 'Thriller']:
            score += 0.05

        reason = _build_reason(show, bq, no, sl)
        scored.append({**show, 'score': score, 'reason': reason})

    scored.sort(key=lambda x: -x['score'])
    return scored[:n]


def _proximity(user_val: float, show_val: float) -> float:
    """Inverse distance score — closer = higher (0–1)."""
    return max(0, 1 - abs(user_val - show_val) / 100)


def _series_match(series_loyalty: float, is_series: bool) -> float:
    if is_series:
        return series_loyalty / 100
    return (100 - series_loyalty) / 100


def _build_reason(show: Dict, bq: float, no: float, sl: float) -> str:
    reasons = []
    if abs(bq - show['binge']) < 20:
        reasons.append("matches your binge depth")
    if abs(no - show['night']) < 20:
        reasons.append("fits your viewing window")
    if show['intensity'] > 80:
        reasons.append("high narrative intensity")
    if not reasons:
        reasons = ["aligns with your behavioral profile"]
    return "Recommended because it " + " and ".join(reasons[:2])
