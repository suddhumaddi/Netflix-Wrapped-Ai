"""
Netflix Wrapped AI — Demo Data Generator
Creates a rich, realistic synthetic viewing dataset.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


SHOWS = [
    ("Stranger Things",   True,  42, "Sci-Fi"),
    ("The Crown",         True,  56, "Drama"),
    ("Squid Game",        True,  38, "Thriller"),
    ("Ozark",             True,  58, "Crime"),
    ("Wednesday",         True,  46, "Mystery"),
    ("Black Mirror",      True,  60, "Sci-Fi"),
    ("Bridgerton",        True,  55, "Romance"),
    ("Money Heist",       True,  48, "Crime"),
    ("Dark",              True,  53, "Sci-Fi"),
    ("The Witcher",       True,  62, "Fantasy"),
    ("Breaking Bad",      True,  47, "Crime"),
    ("Better Call Saul",  True,  49, "Crime"),
    ("The Night Agent",   True,  44, "Thriller"),
    ("Narcos",            True,  50, "Crime"),
    ("Mindhunter",        True,  54, "Crime"),
    ("Succession",        True,  60, "Drama"),
    ("The Last of Us",    True,  60, "Drama"),
    ("Glass Onion",       False, 139, "Mystery"),
    ("The Irishman",      False, 209, "Crime"),
    ("Marriage Story",    False, 137, "Drama"),
    ("Roma",              False, 135, "Drama"),
    ("Extraction",        False, 116, "Action"),
    ("The Gray Man",      False, 122, "Action"),
    ("Knives Out",        False, 130, "Mystery"),
    ("Bird Box",          False, 124, "Thriller"),
    ("Mudbound",          False, 134, "Drama"),
    ("The Power of Dog",  False, 126, "Drama"),
    ("Don't Look Up",     False, 138, "Comedy"),
]


def generate_demo_data(n: int = 900, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    end_date   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=730)  # 2 years of data

    rows = []
    for _ in range(n):
        # Temporal bias: weekends + evenings
        days_offset = np.random.randint(0, 730)
        base_date   = start_date + timedelta(days=days_offset)

        # Weekend probability boost
        if base_date.weekday() < 5 and np.random.random() < 0.25:
            days_offset = np.random.randint(0, 730)
            base_date   = start_date + timedelta(days=days_offset)

        # Hour: bimodal — evening peak (20-23) + late night (0-2)
        r = np.random.random()
        if r < 0.50:
            hour = int(np.clip(np.random.normal(21.5, 1.5), 18, 23))
        elif r < 0.70:
            hour = int(np.clip(np.random.normal(0.5,  1.0),  0,  3))
        elif r < 0.85:
            hour = int(np.clip(np.random.normal(15.0, 2.0), 12, 17))
        else:
            hour = int(np.clip(np.random.normal(10.0, 2.0),  6, 12))

        show_idx              = np.random.randint(0, len(SHOWS))
        name, series, base_d, genre = SHOWS[show_idx]

        if series:
            s     = np.random.randint(1, 5)
            e     = np.random.randint(1, 11)
            title = f"{name}: Season {s}: Episode {e}"
        else:
            title = name

        dur = max(15, int(np.random.normal(base_d, base_d * 0.08)))

        rows.append({
            'title':            title,
            'date':             base_date + timedelta(hours=hour),
            'duration_minutes': dur,
            'is_series':        series,
            'genre':            genre,
        })

    df = pd.DataFrame(rows)

    # Temporal columns
    df['year']       = df['date'].dt.year
    df['month']      = df['date'].dt.month
    df['day']        = df['date'].dt.day
    df['weekday']    = df['date'].dt.weekday
    df['hour']       = df['date'].dt.hour
    df['week']       = df['date'].dt.isocalendar().week.astype(int)
    df['date_only']  = df['date'].dt.date
    df['is_weekend'] = df['weekday'].isin([5, 6])
    df['show_name']  = df['title'].str.replace(
        r':\s*(Season|Episode|Part|Chapter|Volume|Vol).*', '',
        regex=True, flags=__import__('re').IGNORECASE
    ).str.strip()

    ZONES = {(5,12):'morning',(12,17):'afternoon',(17,21):'evening',(21,24):'night'}
    def zone(h):
        for (s,e),z in ZONES.items():
            if s <= h < e: return z
        return 'late_night'
    df['circadian_zone'] = df['hour'].apply(zone)

    return df.sort_values('date').reset_index(drop=True)
