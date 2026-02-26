"""
Netflix Wrapped AI — Session Clustering Engine
KMeans behavioral segmentation on viewing sessions.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)


def cluster_viewing_sessions(df: pd.DataFrame, n_clusters: int = 4) -> Tuple[pd.DataFrame, Dict]:
    """
    KMeans clustering on session-level behavioral features.
    Returns annotated DataFrame + cluster summary dict.
    Falls back gracefully if sklearn not available.
    """
    try:
        from sklearn.cluster      import KMeans
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
    except Exception as e:
        logger.warning(f"Clustering error: {e}")
        print(f"CLUSTERING FAILED: {e}")
        return df, _empty_cluster_result()

    if len(df) < n_clusters * 3:
        return df, _empty_cluster_result()

    # ── Build feature matrix
    features = _build_session_features(df)
    if features is None or len(features) < n_clusters:
        return df, _empty_cluster_result()

    feat_cols = ['hour_sin', 'hour_cos', 'weekday_norm', 'is_series_f', 'is_weekend_f']
    if 'duration_norm' in features.columns:
        feat_cols.append('duration_norm')

    X = features[feat_cols].fillna(0).values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ── KMeans
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    features['cluster'] = labels

    # ── PCA for 2D visualization
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    features['pca_x'] = coords[:, 0]
    features['pca_y'] = coords[:, 1]

    # ── Merge back
    df_out = df.copy()
    df_out['cluster'] = -1
    df_out.loc[features.index, 'cluster'] = features['cluster']

    # ── Cluster profiles
    summary = _build_cluster_profiles(features, df_out, n_clusters)

    return df_out, summary


def _build_session_features(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Construct numeric features per viewing session."""
    f = pd.DataFrame(index=df.index)

    # Cyclical encoding of hour
    f['hour_sin']    = np.sin(2 * np.pi * df['hour'] / 24)
    f['hour_cos']    = np.cos(2 * np.pi * df['hour'] / 24)

    # Weekday normalized 0-1
    f['weekday_norm'] = df['weekday'] / 6.0

    # Boolean flags as float
    f['is_series_f']  = df['is_series'].astype(float) if 'is_series'  in df.columns else 0.5
    f['is_weekend_f'] = df['is_weekend'].astype(float) if 'is_weekend' in df.columns else 0.5

    # Duration (if available)
    if 'duration_minutes' in df.columns and df['duration_minutes'].notna().sum() > len(df) * 0.3:
        dmax = df['duration_minutes'].quantile(0.95)
        f['duration_norm'] = (df['duration_minutes'].clip(upper=dmax) / dmax).fillna(0.5)

    return f


def _build_cluster_profiles(features: pd.DataFrame, df: pd.DataFrame, n_clusters: int) -> Dict:
    profiles = {}

    CLUSTER_NAMES = [
        ("Prime Time Bingers",  "Heavy evening series consumers — the core Netflix audience"),
        ("Late Night Wanderers","Irregular, late-hour explorers driven by impulse"),
        ("Weekend Warriors",    "Concentrated weekend viewers with high session depth"),
        ("Casual Drifters",     "Low-intensity, irregular daytime and afternoon watchers"),
    ]

    for i in range(n_clusters):
        mask     = features['cluster'] == i
        cluster_features = features[mask]
        cluster_df_idx = df[df['cluster'] == i] if 'cluster' in df.columns else pd.DataFrame()

        if len(cluster_features) == 0:
            continue

        avg_hour    = float(((np.arctan2(cluster_features['hour_sin'].mean(),
                                          cluster_features['hour_cos'].mean())
                              / (2*np.pi)) * 24) % 24)
        avg_weekday = float(cluster_features['weekday_norm'].mean() * 6)
        series_pct  = float(cluster_features['is_series_f'].mean() * 100)
        weekend_pct = float(cluster_features['is_weekend_f'].mean() * 100)
        size        = int(mask.sum())

        name, desc = CLUSTER_NAMES[i % len(CLUSTER_NAMES)]

        profiles[i] = {
            'id':          i,
            'name':        name,
            'description': desc,
            'size':        size,
            'pct':         round(size / len(features) * 100, 1),
            'avg_hour':    round(avg_hour, 1),
            'avg_weekday': round(avg_weekday, 1),
            'series_pct':  round(series_pct, 1),
            'weekend_pct': round(weekend_pct, 1),
            'pca_x_mean':  float(cluster_features['pca_x'].mean()),
            'pca_y_mean':  float(cluster_features['pca_y'].mean()),
        }

    # Scatter data for visualization
    scatter_data = features[['pca_x', 'pca_y', 'cluster']].copy()
    scatter_data['cluster_str'] = scatter_data['cluster'].astype(str)

    return {
        'available':   True,
        'n_clusters':  n_clusters,
        'profiles':    profiles,
        'scatter_data': scatter_data,
        'features':    features,
    }


def _empty_cluster_result() -> Dict:
    return {'available': False, 'profiles': {}, 'scatter_data': None}


# ─────────────────────────────────────────────
# ANOMALY DETECTION
# ─────────────────────────────────────────────

def detect_anomalies(df: pd.DataFrame) -> Dict:
    """
    Identify statistically unusual weeks/months and binge spikes.
    Uses IQR-based outlier detection — no external deps required.
    """
    weekly = df.groupby('week').size().reset_index(name='count')
    monthly = df.groupby('month').size().reset_index(name='count')

    weekly_anomalies  = _iqr_outliers(weekly, 'count', 'week')
    monthly_anomalies = _iqr_outliers(monthly, 'count', 'month')

    # Binge spike days — days with 3x the average watches
    daily = df.groupby(df['date'].dt.date).size().reset_index(name='count')
    daily.columns = ['date', 'count']
    mean_daily = daily['count'].mean()
    binge_days = daily[daily['count'] >= mean_daily * 2.5].copy()
    binge_days['excess'] = (binge_days['count'] - mean_daily).round(1)

    return {
        'weekly_anomalies':  weekly_anomalies,
        'monthly_anomalies': monthly_anomalies,
        'binge_days':        binge_days.sort_values('count', ascending=False).head(5),
        'mean_daily':        round(mean_daily, 1),
    }


def _iqr_outliers(df: pd.DataFrame, value_col: str, label_col: str) -> pd.DataFrame:
    q1, q3 = df[value_col].quantile([0.25, 0.75])
    iqr    = q3 - q1
    high   = q3 + 1.5 * iqr
    low    = q1 - 1.5 * iqr
    return df[(df[value_col] > high) | (df[value_col] < low)].copy()
