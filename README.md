# 🎬 NETFLIX WRAPPED AI — v2.0
### Cinematic Behavioral Intelligence Platform

> *"This is not a dashboard. It is a cinematic data experience."*

---

## WHAT'S NEW IN V2

| Feature | Status |
|---|---|
| Modular production architecture | ✅ |
| ML session clustering (KMeans + PCA) | ✅ |
| Anomaly & binge spike detection | ✅ |
| 8D behavioral feature vector | ✅ |
| Rolling binge detection (4h window) | ✅ |
| Shannon entropy / content diversity index | ✅ |
| Consistency stability metric | ✅ |
| Recency weighting (30-day bias) | ✅ |
| Year-over-year comparison | ✅ |
| Circadian viewing classification | ✅ |
| Longest streak + detox gap detection | ✅ |
| 7-day momentum curve | ✅ |
| AI narrative engine (template-based) | ✅ |
| Behavioral recommendation engine | ✅ |
| Story Mode (cinematic card flow) | ✅ |
| Deep Intelligence Mode | ✅ |
| AI Report Mode | ✅ |
| LinkedIn-ready summary generator | ✅ |
| DNA Radar Chart | ✅ |
| Genre distribution (donut) | ✅ |
| YOY bar chart | ✅ |
| Compare two profiles (similarity score) | ✅ |
| Export: JSON feature vector | ✅ |
| Export: Text intelligence report | ✅ |
| Export: Processed CSV | ✅ |
| st.cache_data performance caching | ✅ |

---

## SETUP

```bash
pip install -r requirements.txt
streamlit run app.py
```

### With ML clustering enabled:
```bash
pip install scikit-learn
```

---

## PROJECT STRUCTURE

```
Netflix-Wrapped-AI/
│
├── app.py                          ← Main orchestrator
│
├── analytics/
│   ├── metrics.py                  ← All behavioral KPIs
│   ├── clustering.py               ← KMeans + anomaly detection
│   └── feature_vector.py           ← 8D embedding builder
│
├── ai/
│   ├── narrative_engine.py         ← AI report generation
│   └── recommender.py              ← Behavioral recommendations
│
├── ui/
│   └── themes.py                   ← Master CSS injection
│
├── visualizations/
│   └── charts.py                   ← All Plotly chart builders
│
├── utils/
│   ├── data_parser.py              ← Netflix CSV parsing
│   ├── demo_data.py                ← Synthetic data generator
│   └── export.py                   ← Export utilities
│
├── requirements.txt
└── README.md
```

---

## VIEW MODES

### 📊 Dashboard Mode
The full cinematic dashboard. All original sections preserved and enhanced:
- Hero reveal with animated red glow
- 4 behavioral KPI cards
- Extended metrics strip (Consistency, Diversity, Recency, Streak)
- Monthly, Weekday, Hourly charts
- Heat Map (Day × Hour)
- 7-day momentum curve
- Top shows + Genre distribution
- DNA Radar Chart with feature vector sidebar
- Year-over-year comparison (if multi-year data)
- AI-powered recommendations
- Archetype reveal
- Export panel

### 🎬 Story Mode
Auto-scroll cinematic narrative cards — one stat per full-height card.
Dramatic, Spotify Wrapped-style sequential reveal.

### 🤖 AI Report Mode
Full AI-generated behavioral narrative report:
- Cinematic opening frame
- Statistical breakdown
- Binge behavior analysis
- Night pattern analysis
- Content identity essay
- Consistency and diversity fingerprint
- Circadian classification
- Archetype deep dive
- LinkedIn-ready summary

### 🔬 Deep Intelligence Mode
ML-powered analysis:
- KMeans cluster map (PCA visualization)
- Session cluster profiles (4 segments)
- Binge spike anomaly detection
- Digital detox gap detection
- 8D feature vector display
- Advanced behavioral metrics
- Circadian type, momentum trend

---

## BEHAVIORAL METRICS EXPLAINED

| Metric | Method | Range |
|---|---|---|
| Binge Quotient | Rolling 3+ episodes within 4h window | 0–100 |
| Weekend Dominance | % sessions on Sat/Sun | 0–100% |
| Night Owl Index | % sessions after 22:00 | 0–100% |
| Series Loyalty | % series vs total watches | 0–100% |
| Consistency Score | 100 - (weekly_std / weekly_mean × 50) | 0–100 |
| Content Diversity | Normalized Shannon entropy on show dist | 0–100% |
| Recency Score | 30-day avg vs annual baseline | 0–100 |
| Momentum Trend | 7-day rolling avg slope | Rising/Stable/Falling |
| Circadian Zone | Hour → morning/afternoon/evening/night/late | Classification |
| Longest Streak | Max consecutive viewing days | Days |
| Detox Gaps | Breaks ≥ 7 days | Day ranges |

---

## FEATURE VECTOR (8D Embedding)

```json
{
  "embedding": [
    binge_score,        // 0-1
    weekend_ratio,      // 0-1
    night_ratio,        // 0-1
    series_loyalty,     // 0-1
    avg_session_hours,  // 0-1 (normalized to 8hr max)
    consistency_score,  // 0-1
    entropy_score,      // 0-1 (Shannon normalized)
    recency_score       // 0-1
  ]
}
```

Use for: cosine similarity scoring, future ML training, profile comparison.

---

## STREAMING ARCHETYPES

| Archetype | Primary Signals |
|---|---|
| The Strategic Binger | High binge_score + high series_loyalty |
| The Night Architect | High night_ratio |
| The Weekend Ritualist | High weekend_ratio + moderate consistency |
| The Eclectic Explorer | High entropy + low series_loyalty |
| The Serial Devotee | Very high series_loyalty |
| The Cinematic Soul | Balanced/fallback archetype |

---

## COMPARE MODE

Upload two Netflix CSVs to compute:
- Cosine similarity score (0–100%)
- Side-by-side KPI comparison
- Archetype comparison
- Behavioral divergence analysis

---

*Netflix Wrapped AI — Behavioral Streaming Intelligence Platform*
*Built with Streamlit + Plotly + scikit-learn*
