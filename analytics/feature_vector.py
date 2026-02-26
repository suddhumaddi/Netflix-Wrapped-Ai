"""
Netflix Wrapped AI — Feature Vector Engine
Builds exportable behavioral embeddings.
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, Any


def build_full_feature_vector(metrics: Dict, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Construct a complete, normalized behavioral feature vector
    from all computed metrics. Exportable as JSON.
    """
    fv = {
        "schema_version": "2.0",
        "generated_at": pd.Timestamp.now().isoformat(),

        # Core behavioral signals
        "behavioral": {
            "binge_score":         round(metrics.get('binge_quotient', 0) / 100, 4),
            "weekend_ratio":       round(metrics.get('weekend_dominance', 0) / 100, 4),
            "night_owl_ratio":     round(metrics.get('night_owl_index', 0) / 100, 4),
            "series_loyalty":      round(metrics.get('series_loyalty', 0) / 100, 4),
            "consistency_score":   round(metrics.get('consistency_score', 0) / 100, 4),
            "content_entropy":     round(metrics.get('normalized_entropy', 0), 4),
            "recency_score":       round(metrics.get('recency_score', 0.5), 4),
        },

        # Temporal fingerprint
        "temporal": {
            "peak_hour":           metrics.get('peak_hour', 21),
            "peak_weekday":        metrics.get('peak_weekday', 'Sat'),
            "dominant_zone":       metrics.get('dominant_zone', 'evening'),
            "circadian_label":     metrics.get('circadian_label', 'Prime Time Viewer'),
        },

        # Volume metrics (normalized)
        "volume": {
            "total_hours":         metrics.get('total_hours', 0),
            "total_titles":        metrics.get('total_titles', 0),
            "avg_daily_hours":     metrics.get('avg_daily_hours', 0),
            "longest_streak_days": metrics.get('longest_streak', 0),
        },

        # Identity
        "archetype": {
            "name":   metrics.get('archetype', {}).get('name', 'Unknown'),
            "traits": metrics.get('archetype', {}).get('traits', []),
        },

        # Raw feature array for ML use
        "embedding": _build_embedding_array(metrics),
    }

    return fv


def _build_embedding_array(metrics: Dict) -> list:
    """
    8-dimensional normalized embedding vector.
    Useful for similarity scoring, clustering, and comparison.
    """
    return [
        round(metrics.get('binge_quotient', 0) / 100, 4),
        round(metrics.get('weekend_dominance', 0) / 100, 4),
        round(metrics.get('night_owl_index', 0) / 100, 4),
        round(metrics.get('series_loyalty', 0) / 100, 4),
        round(min(1.0, metrics.get('avg_daily_hours', 0) / 8), 4),
        round(metrics.get('consistency_score', 0) / 100, 4),
        round(metrics.get('normalized_entropy', 0), 4),
        round(metrics.get('recency_score', 50) / 100, 4),
    ]


def compute_similarity(fv1: Dict, fv2: Dict) -> float:
    """
    Cosine similarity between two feature vectors (0→1, 1=identical).
    """
    v1 = np.array(fv1.get('embedding', []))
    v2 = np.array(fv2.get('embedding', []))

    if len(v1) == 0 or len(v2) == 0 or len(v1) != len(v2):
        return 0.0

    dot = np.dot(v1, v2)
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return round(float(dot / max(1e-10, norm)), 4)


def export_feature_vector_json(fv: Dict) -> str:
    return json.dumps(fv, indent=2, default=str)
