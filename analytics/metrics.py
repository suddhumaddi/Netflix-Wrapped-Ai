"""
Netflix Wrapped AI — Core Metrics Engine
Computes all behavioral, temporal, and statistical metrics.
"""

import pandas as pd
import numpy as np
import calendar
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def compute_all_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    m = {}

    # ── FUNDAMENTALS
    m.update(_fundamentals(df))

    # ── BEHAVIORAL KPIs
    m.update(_behavioral_kpis(df))

    # ── TEMPORAL DISTRIBUTIONS
    m.update(_temporal_distributions(df))

    # ── STREAK ANALYSIS
    m.update(_streak_analysis(df))

    # ── CONTENT DIVERSITY
    m.update(_diversity_metrics(df))

    # ── ROLLING BEHAVIOR
    m.update(_rolling_behavior(df))

    # ── YEAR-OVER-YEAR
    m.update(_yoy_comparison(df))

    # ── CIRCADIAN CLASSIFICATION
    m.update(_circadian_classification(df))

    # ── FEATURE VECTOR
    m['feature_vector'] = _build_feature_vector(m, df)

    # ── ARCHETYPE
    m['archetype'] = classify_archetype(m)

    return m


# ─────────────────────────────────────────────
# FUNDAMENTALS
# ─────────────────────────────────────────────

def _fundamentals(df: pd.DataFrame) -> dict:
    if 'duration_minutes' in df.columns and df['duration_minutes'].notna().sum() > 10:
        total_mins = df['duration_minutes'].sum()
    else:
        total_mins = len(df) * 42

    days_active  = df['date_only'].nunique() if 'date_only' in df.columns else df['date'].dt.date.nunique()
    total_hours  = round(total_mins / 60)
    years_data   = sorted(df['year'].unique().tolist())

    return {
        'total_hours':   total_hours,
        'total_minutes': total_mins,
        'total_titles':  df['title'].nunique(),
        'total_shows':   df['show_name'].nunique() if 'show_name' in df.columns else df['title'].nunique(),
        'total_sessions':len(df),
        'days_active':   days_active,
        'avg_daily_hours': round(total_hours / max(1, days_active), 1),
        'years_in_data': years_data,
        'date_range':    (df['date'].min(), df['date'].max()),
    }


# ─────────────────────────────────────────────
# BEHAVIORAL KPIs
# ─────────────────────────────────────────────

def _behavioral_kpis(df: pd.DataFrame) -> dict:
    # Binge Quotient — same show 3+ in rolling 4h window
    binge_score = _compute_binge_quotient(df)

    # Weekend Dominance
    weekend_pct = int(df['is_weekend'].mean() * 100) if 'is_weekend' in df.columns else 50

    # Night Owl Index (after 22:00)
    night_pct   = int((df['hour'] >= 22).mean() * 100)

    # Series Loyalty
    series_pct  = int(df['is_series'].mean() * 100) if 'is_series' in df.columns else 65

    # Peak metrics
    peak_hour   = int(df['hour'].mode()[0])
    peak_wday   = int(df['weekday'].mode()[0])
    peak_month  = int(df['month'].mode()[0])

    # Top show
    if 'show_name' in df.columns:
        top_s  = df['show_name'].value_counts()
        top_show       = top_s.index[0] if len(top_s) else '—'
        top_show_count = int(top_s.iloc[0]) if len(top_s) else 0
    else:
        top_show, top_show_count = '—', 0

    ph = peak_hour
    peak_hour_label = f"{ph % 12 or 12}{'AM' if ph < 12 else 'PM'}"
    peak_day_label  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][peak_wday]

    return {
        'binge_quotient':     binge_score,
        'weekend_dominance':  weekend_pct,
        'night_owl_index':    night_pct,
        'series_loyalty':     series_pct,
        'peak_hour':          peak_hour,
        'peak_hour_label':    peak_hour_label,
        'peak_weekday':       peak_day_label,
        'peak_month':         calendar.month_abbr[peak_month],
        'top_show':           top_show,
        'top_show_count':     top_show_count,
    }


def _compute_binge_quotient(df: pd.DataFrame) -> int:
    """Rolling binge detection — 3+ episodes of same show within 4h window."""
    if 'show_name' not in df.columns or len(df) < 3:
        return 0

    df_s    = df.sort_values('date').copy()
    binge_sessions = 0
    total_sessions = 0

    for show, group in df_s.groupby('show_name'):
        if len(group) < 3:
            continue
        g = group.sort_values('date')
        dates = g['date'].values
        total_sessions += 1
        # Sliding window: any 3 within 240 minutes
        for i in range(len(dates) - 2):
            delta = (pd.Timestamp(dates[i+2]) - pd.Timestamp(dates[i])).total_seconds() / 60
            if delta <= 240:
                binge_sessions += 1
                break

    if total_sessions == 0:
        return 0
    return min(99, int((binge_sessions / total_sessions) * 130))


# ─────────────────────────────────────────────
# TEMPORAL DISTRIBUTIONS
# ─────────────────────────────────────────────

def _temporal_distributions(df: pd.DataFrame) -> dict:
    # Monthly
    monthly = df.groupby('month').size().reset_index(name='count')
    monthly['month_name'] = monthly['month'].apply(lambda x: calendar.month_abbr[x])

    # Weekday
    wday_dist = df.groupby('weekday').size().reset_index(name='count')
    wday_dist['day_name'] = wday_dist['weekday'].apply(lambda x: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][x])

    # Hourly
    hourly = df.groupby('hour').size().reset_index(name='count')

    # Heatmap weekday×hour
    heatmap = df.groupby(['weekday','hour']).size().reset_index(name='count')

    # Top shows
    top_shows = None
    if 'show_name' in df.columns:
        ts = df['show_name'].value_counts().head(10).reset_index()
        ts.columns = ['show', 'count']
        top_shows = ts

    # Genre distribution (if available)
    genre_dist = None
    if 'genre' in df.columns:
        gd = df['genre'].value_counts().reset_index()
        gd.columns = ['genre', 'count']
        genre_dist = gd

    return {
        'monthly':     monthly,
        'weekday_dist':wday_dist,
        'hourly':      hourly,
        'heatmap':     heatmap,
        'top_shows':   top_shows,
        'genre_dist':  genre_dist,
    }


# ─────────────────────────────────────────────
# STREAK ANALYSIS
# ─────────────────────────────────────────────

def _streak_analysis(df: pd.DataFrame) -> dict:
    if 'date_only' in df.columns:
        dates = sorted(df['date_only'].unique())
    else:
        dates = sorted(df['date'].dt.date.unique())

    if not dates:
        return {'longest_streak': 0, 'current_streak': 0, 'streak_dates': []}

    longest  = 1
    current  = 1
    temp     = 1

    for i in range(1, len(dates)):
        delta = (pd.Timestamp(dates[i]) - pd.Timestamp(dates[i-1])).days
        if delta == 1:
            temp += 1
            longest = max(longest, temp)
        else:
            temp = 1

    # Current streak from end
    today = pd.Timestamp('today').date()
    cs = 0
    for d in reversed(dates):
        delta = (today - d).days
        if delta <= cs + 1:
            cs += 1
        else:
            break

    # Detect "detox" gaps ≥ 7 days
    gaps = []
    for i in range(1, len(dates)):
        delta = (pd.Timestamp(dates[i]) - pd.Timestamp(dates[i-1])).days
        if delta >= 7:
            gaps.append({
                'start': str(dates[i-1]),
                'end':   str(dates[i]),
                'days':  delta,
            })

    return {
        'longest_streak': longest,
        'current_streak': cs,
        'detox_gaps':     sorted(gaps, key=lambda x: -x['days'])[:3],
        'total_gap_days': sum(g['days'] for g in gaps),
    }


# ─────────────────────────────────────────────
# DIVERSITY METRICS
# ─────────────────────────────────────────────

def _diversity_metrics(df: pd.DataFrame) -> dict:
    # Shannon Entropy on show distribution
    show_counts = df['show_name'].value_counts() if 'show_name' in df.columns else df['title'].value_counts()
    probs = show_counts / show_counts.sum()
    shannon = float(-np.sum(probs * np.log2(probs + 1e-10)))
    max_entropy = np.log2(len(probs))
    normalized_entropy = float(shannon / max_entropy) if max_entropy > 0 else 0

    # Consistency score — inverse of weekly std dev
    weekly = df.groupby('week').size()
    weekly_std = float(weekly.std()) if len(weekly) > 1 else 0
    weekly_mean = float(weekly.mean()) if len(weekly) > 0 else 1
    consistency = max(0, min(100, int(100 - (weekly_std / max(1, weekly_mean)) * 50)))

    return {
        'shannon_entropy':       round(shannon, 2),
        'normalized_entropy':    round(normalized_entropy, 3),
        'content_diversity_pct': round(normalized_entropy * 100, 1),
        'consistency_score':     consistency,
        'weekly_std':            round(weekly_std, 1),
        'weekly_mean':           round(weekly_mean, 1),
    }


# ─────────────────────────────────────────────
# ROLLING BEHAVIOR
# ─────────────────────────────────────────────

def _rolling_behavior(df: pd.DataFrame) -> dict:
    # 7-day rolling average momentum
    daily = df.groupby(df['date'].dt.date).size().reset_index()
    daily.columns = ['date', 'count']
    daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.sort_values('date')
    daily['rolling_7d'] = daily['count'].rolling(7, min_periods=1).mean()

    # 30-day recency score — how active in last 30 days vs baseline
    if len(daily) >= 30:
        recent_30  = daily.tail(30)['count'].mean()
        baseline   = daily['count'].mean()
        recency_score = min(100, max(0, int((recent_30 / max(0.1, baseline)) * 50)))
    else:
        recency_score = 50

    return {
        'daily_counts':    daily,
        'recency_score':   recency_score,
        'momentum_trend':  'rising' if recency_score > 55 else ('falling' if recency_score < 45 else 'stable'),
    }


# ─────────────────────────────────────────────
# YEAR OVER YEAR
# ─────────────────────────────────────────────

def _yoy_comparison(df: pd.DataFrame) -> dict:
    years = sorted(df['year'].unique())
    if len(years) < 2:
        return {'yoy_available': False, 'yoy_data': None}

    yoy = df.groupby('year').agg(
        sessions=('title', 'count'),
        titles=('title', 'nunique'),
    ).reset_index()

    if 'duration_minutes' in df.columns:
        yoy_hrs = df.groupby('year')['duration_minutes'].sum() / 60
        yoy = yoy.merge(yoy_hrs.rename('hours').reset_index(), on='year', how='left')
    else:
        yoy['hours'] = yoy['sessions'] * 42 / 60

    return {
        'yoy_available': True,
        'yoy_data':      yoy,
        'years':         years,
    }


# ─────────────────────────────────────────────
# CIRCADIAN CLASSIFICATION
# ─────────────────────────────────────────────

def _circadian_classification(df: pd.DataFrame) -> dict:
    if 'circadian_zone' not in df.columns:
        df['circadian_zone'] = 'evening'

    zone_dist = df['circadian_zone'].value_counts(normalize=True).to_dict()
    dominant  = df['circadian_zone'].mode()[0]

    labels = {
        'morning':    'The Early Bird',
        'afternoon':  'The Afternoon Drifter',
        'evening':    'The Prime Time Viewer',
        'night':      'The Night Curator',
        'late_night': 'The Midnight Wanderer',
    }

    return {
        'circadian_dist':  zone_dist,
        'dominant_zone':   dominant,
        'circadian_label': labels.get(dominant, 'The Balanced Viewer'),
    }


# ─────────────────────────────────────────────
# FEATURE VECTOR
# ─────────────────────────────────────────────

def _build_feature_vector(m: dict, df: pd.DataFrame) -> dict:
    return {
        'binge_score':         m.get('binge_quotient', 0) / 100,
        'weekend_ratio':       m.get('weekend_dominance', 0) / 100,
        'night_ratio':         m.get('night_owl_index', 0) / 100,
        'series_loyalty':      m.get('series_loyalty', 0) / 100,
        'avg_session_hours':   min(1.0, m.get('avg_daily_hours', 0) / 8),
        'consistency_score':   m.get('consistency_score', 0) / 100,
        'entropy_score':       m.get('normalized_entropy', 0),
        'recency_score':       m.get('recency_score', 50) / 100,
    }


# ─────────────────────────────────────────────
# ARCHETYPE CLASSIFIER
# ─────────────────────────────────────────────

def classify_archetype(m: dict) -> dict:
    bq = m.get('binge_quotient', 0)
    wd = m.get('weekend_dominance', 0)
    no = m.get('night_owl_index', 0)
    sl = m.get('series_loyalty', 0)
    en = m.get('content_diversity_pct', 50)
    cs = m.get('consistency_score', 50)

    ARCHETYPES = [
        {
            "name":  "THE STRATEGIC BINGER",
            "score": bq * 0.5 + sl * 0.3 + (100 - wd) * 0.2,
            "desc":  "You don't just watch — you commit. When a series captures you, everything else dissolves. You've turned the act of binging into an art form: calculated, immersive, and utterly consuming.",
            "traits":    ["BINGE MASTERY", "SERIES DEVOTED", "FULL COMMITMENT"],
            "highlight": 0,
            "emoji":     "🎯",
        },
        {
            "name":  "THE NIGHT ARCHITECT",
            "score": no * 0.6 + (100 - wd) * 0.2 + bq * 0.2,
            "desc":  "The world quiets and your screen ignites. You've constructed an entire parallel life in the hours between midnight and dawn — curated, intentional, and entirely your own.",
            "traits":    ["LATE NIGHT ELITE", "SOLITUDE CURATOR", "DARK HOURS"],
            "highlight": 1,
            "emoji":     "🌙",
        },
        {
            "name":  "THE WEEKEND RITUALIST",
            "score": wd * 0.6 + cs * 0.3 + (100 - no) * 0.1,
            "desc":  "Your weekends are sacred ground. You protect your viewing window with the precision of someone who understands that great content deserves proper ceremony — unhurried, immersive, and entirely intentional.",
            "traits":    ["WEEKEND SOVEREIGN", "RITUAL BEHAVIOR", "FOCUSED DEPTH"],
            "highlight": 2,
            "emoji":     "📅",
        },
        {
            "name":  "THE ECLECTIC EXPLORER",
            "score": en * 0.6 + (100 - sl) * 0.3 + (100 - bq) * 0.1,
            "desc":  "Genres, formats, languages — none of it constrains you. Your viewing history is a passport to everywhere. You follow curiosity like a compass and no algorithm has ever truly predicted your next move.",
            "traits":    ["FORMAT AGNOSTIC", "CURIOSITY ENGINE", "GENRE FLUID"],
            "highlight": 0,
            "emoji":     "🌐",
        },
        {
            "name":  "THE SERIAL DEVOTEE",
            "score": sl * 0.5 + bq * 0.3 + cs * 0.2,
            "desc":  "Series are your mother tongue. You track characters across seasons, remember plot threads from years prior, and feel genuine grief when a show ends. You're not watching — you're inhabiting.",
            "traits":    ["SERIES PURIST", "DEEP LORE KEEPER", "CHARACTER BONDED"],
            "highlight": 1,
            "emoji":     "📺",
        },
        {
            "name":  "THE CINEMATIC SOUL",
            "score": 40,  # base fallback
            "desc":  "Your viewing life reads like a curated film festival. Every choice is intentional. Every hour spent watching carries the quiet weight of someone who takes storytelling seriously.",
            "traits":    ["REFINED TASTE", "STORY SEEKER", "INTENTIONAL VIEWER"],
            "highlight": 0,
            "emoji":     "🎬",
        },
    ]

    best = max(ARCHETYPES, key=lambda a: a['score'])
    return {k: v for k, v in best.items() if k != 'score'}
