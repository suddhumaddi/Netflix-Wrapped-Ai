"""
Netflix Wrapped AI — Data Parser
Handles Netflix CSV parsing with robust column detection and cleaning.
"""

import pandas as pd
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)


def parse_netflix_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse a raw Netflix viewing history DataFrame into a clean,
    analytics-ready format with all derived temporal columns.
    """
    df.columns = [c.strip() for c in df.columns]

    date_col  = _find_col(df.columns, ['date', 'watch date', 'start time'])
    title_col = _find_col(df.columns, ['title', 'show title', 'name'])
    dur_col   = _find_col(df.columns, ['duration', 'watch time', 'elapsed'])

    if title_col is None: title_col = df.columns[0]
    if date_col  is None: date_col  = df.columns[1] if len(df.columns) > 1 else df.columns[0]

    result = pd.DataFrame()
    result['title'] = df[title_col].astype(str).str.strip()
    result['date']  = pd.to_datetime(df[date_col], infer_datetime_format=True, errors='coerce')
    result          = result.dropna(subset=['date'])

    if dur_col is not None:
        result['duration_raw'] = df[dur_col]
        result['duration_minutes'] = result['duration_raw'].apply(_parse_duration)
    else:
        result['duration_minutes'] = np.nan

    _add_temporal_columns(result)
    _add_content_flags(result)

    return result.reset_index(drop=True)


def _find_col(columns, keywords):
    for c in columns:
        cl = c.lower()
        if any(k in cl for k in keywords):
            return c
    return None


def _parse_duration(val):
    """Parse duration string (HH:MM:SS or minutes int) → float minutes"""
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    # HH:MM:SS
    m = re.match(r'(\d+):(\d{2}):(\d{2})', s)
    if m:
        h, mn, sec = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return h * 60 + mn + sec / 60
    # MM:SS
    m = re.match(r'(\d+):(\d{2})$', s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / 60
    # Plain integer (assume minutes)
    try:
        return float(s)
    except Exception:
        return np.nan


def _add_temporal_columns(df: pd.DataFrame):
    df['year']       = df['date'].dt.year
    df['month']      = df['date'].dt.month
    df['day']        = df['date'].dt.day
    df['weekday']    = df['date'].dt.weekday     # 0=Mon
    df['hour']       = df['date'].dt.hour
    df['week']       = df['date'].dt.isocalendar().week.astype(int)
    df['date_only']  = df['date'].dt.date
    df['is_weekend'] = df['weekday'].isin([5, 6])


def _add_content_flags(df: pd.DataFrame):
    SERIES_PATTERN = re.compile(
        r'season|episode|part|vol\.|chapter|: s\d|series|ep\s*\d',
        re.IGNORECASE
    )
    df['is_series'] = df['title'].str.contains(SERIES_PATTERN, na=False)

    df['show_name'] = df['title'].str.replace(
        r':\s*(Season|Episode|Part|Chapter|Volume|Series|Vol).*',
        '', regex=True, flags=re.IGNORECASE
    ).str.strip()

    df['circadian_zone'] = df['hour'].apply(_circadian_zone)


def _circadian_zone(hour: int) -> str:
    if 5  <= hour < 12: return 'morning'
    if 12 <= hour < 17: return 'afternoon'
    if 17 <= hour < 21: return 'evening'
    if 21 <= hour < 24: return 'night'
    return 'late_night'
