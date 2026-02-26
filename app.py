"""
Netflix Wrapped AI v2
Cinematic Behavioral Intelligence Platform

Entry point — orchestrates all modules.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys, os
import streamlit.components.v1 as components
try:
    from sklearn.cluster import KMeans
    print("✅ sklearn working:", KMeans)
except Exception as e:
    print("❌ sklearn error:", e)

# ─── Path setup so sub-modules resolve correctly ───
sys.path.insert(0, os.path.dirname(__file__))

# ─────────────────────────────────────────────
# PAGE CONFIG (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Wrapped AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Internal modules ───
from ui.themes        import inject_theme
from utils.data_parser   import parse_netflix_csv
from utils.demo_data     import generate_demo_data
from utils.export        import export_feature_vector_json, export_summary_text, dataframe_to_csv_bytes
from analytics.metrics   import compute_all_metrics
from analytics.clustering import cluster_viewing_sessions, detect_anomalies
from analytics.feature_vector import build_full_feature_vector, compute_similarity, export_feature_vector_json as fv_json
from ai.narrative_engine  import generate_narrative_report, generate_linkedin_summary
from ai.recommender       import generate_recommendations
from visualizations.charts import (
    monthly_chart, hourly_chart, weekday_chart, heatmap_chart,
    top_shows_chart, radar_chart, momentum_chart,
    cluster_scatter, yoy_chart, genre_chart,
)

# ─────────────────────────────────────────────
# INJECT THEME
# ─────────────────────────────────────────────
inject_theme()

CHART_CFG = {'displayModeBar': False}


# ═══════════════════════════════════════════════════
# HELPER — CHART WRAPPER
# ═══════════════════════════════════════════════════

def chart_block(title: str, subtitle: str, chart_fn, *args, **kwargs):
    """Render a chart with cinematic header."""
    st.markdown(f"""
    <div class="nw-chart-container">
        <div class="nw-chart-title">{title}</div>
        <div class="nw-chart-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="nw-chart-inner">', unsafe_allow_html=True)
    fig = chart_fn(*args, **kwargs)
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# UPLOAD / LANDING SCREEN
# ═══════════════════════════════════════════════════

def render_upload_screen():
    import base64
    try:
        with open("background2.jpg", "rb") as f:
            bg_data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bg_data}") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
        }}
        .stApp::before {{
            background: rgba(0,0,0,0.88) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    # ── Override checkbox and uploader to not look like Streamlit
    st.markdown("""
    <style>
    [data-testid="stCheckbox"] label p {
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 0.25em !important;
        color: rgba(255,255,255,0.45) !important;
        text-transform: uppercase !important;
    }
    [data-testid="stCheckbox"] {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] p {
        font-family: 'DM Mono', monospace !important;
        color: rgba(255,255,255,0.4) !important;
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nw-upload-screen">
        <div style="margin-bottom:20px;">
    <svg width="60" height="80" viewBox="0 0 60 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0 L0 80 L18 80 L18 28 L38 80 L60 80 L60 0 L42 0 L42 52 L22 0 Z" fill="#E50914"/>
    </svg>
</div>
<div class="nw-upload-logo">NETFLIX WRAPPED AI</div>
        <div class="nw-upload-tagline">BEHAVIORAL INTELLIGENCE PLATFORM · v2.0 · By Sudarshan Maddi </div>
        <div class="nw-upload-headline">
            Your streaming data<br>tells a story you<br>haven't heard <em>yet.</em>
        </div>
        <div class="nw-upload-sub">
            Upload your Netflix viewing history and witness your behavioral patterns 
            transform into a cinematic intelligence experience — powered by ML, 
            AI narrative generation, and behavioral analytics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        uploaded = st.file_uploader(
            "DROP YOUR NETFLIX CSV HERE",
            type=['csv'],
            label_visibility='visible',
        )
        st.markdown("<br>", unsafe_allow_html=True)
        compare_mode = st.checkbox("▷  COMPARE TWO PROFILES  ( UPLOAD 2 CSVs )", value=False)

        uploaded2 = None
        if compare_mode:
            uploaded2 = st.file_uploader(
                "SECOND PROFILE CSV",
                type=['csv'],
                key='upload2',
                label_visibility='visible',
            )

        st.markdown("<br><br>", unsafe_allow_html=True)
        demo = st.button("▷  LAUNCH WITH DEMO DATA", use_container_width=True, type="primary")

    # ── Spacer to separate button from steps
    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)

    # ── Steps — big, spaced, cinematic
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:transparent; }
        .steps {
            display:grid;
            grid-template-columns:repeat(3,1fr);
            gap:32px;
            padding:0 40px;
        }
        .step {
            background:rgba(0,0,0,0.92);
            border:1px solid rgba(255,255,255,0.08);
            border-top:2px solid #E50914;
            padding:48px 40px;
        }
        .step-num {
            font-family:'Bebas Neue',sans-serif;
            font-size:80px;
            color:rgba(229,9,20,0.5);
            line-height:1;
            margin-bottom:24px;
        }
        .step-title {
            font-family:'Bebas Neue',sans-serif;
            font-size:22px;
            letter-spacing:0.06em;
            color:#fff;
            text-shadow:0 0 20px rgba(255,255,255,0.3);
            margin-bottom:16px;
        }
        .step-text {
            font-family:'DM Sans',sans-serif;
            font-size:14px;
            color:rgba(255,255,255,0.75);
            line-height:1.9;
            font-weight:300;
        }
        .step-text strong { color:#fff; }
    </style>
    <div class="steps">
        <div class="step">
            <div class="step-num">01</div>
            <div class="step-title">GET YOUR DATA</div>
            <div class="step-text">
                Go to <strong>netflix.com/account</strong><br>
                → Security & Privacy<br>
                → Get your data<br>
                → Request download
            </div>
        </div>
        <div class="step">
            <div class="step-num">02</div>
            <div class="step-title">EXTRACT THE FILE</div>
            <div class="step-text">
                Netflix emails you a link<br>
                → Download the ZIP<br>
                → Extract it<br>
                → Find <strong>ViewingActivity.csv</strong>
            </div>
        </div>
        <div class="step">
            <div class="step-num">03</div>
            <div class="step-title">UPLOAD & DISCOVER</div>
            <div class="step-text">
                Drop the CSV above<br>
                → Report generates instantly<br>
                → Or try demo data<br>
                → No account needed
            </div>
        </div>
    </div>
    """, height=340, scrolling=False)

    return uploaded, uploaded2, demo, compare_mode


# ═══════════════════════════════════════════════════
# STORY MODE
# ═══════════════════════════════════════════════════

def render_story_mode(metrics):
    h         = metrics['total_hours']
    titles    = metrics['total_titles']
    streak    = metrics.get('longest_streak', 0)
    top       = metrics.get('top_show', '—')
    arch      = metrics.get('archetype', {}).get('name', '—')
    peak      = metrics.get('peak_hour_label', '9PM')
    bq        = metrics.get('binge_quotient', 0)

    cards = [
        (f"<span class='red'>{h:,}</span> HOURS",      "That's how many hours of your life became someone else's story this year."),
        (f"<span class='red'>{titles}</span> TITLES",   "Each one a door you chose to open."),
        (f"<span class='red'>{streak}</span> DAYS",     f"Your longest unbroken viewing streak. Discipline — or devotion."),
        (f'"<span class="red">{top}</span>"',            "The show that owned you most."),
        (f"<span class='red'>{peak}</span>",             "The hour your screen consistently comes alive."),
        (f"BINGE SCORE:<br><span class='red'>{bq}</span>",  "Out of 100. The algorithm takes notes."),
        (arch,                                           "Your streaming archetype. A classification built from your behavior — not your preferences."),
    ]

    st.markdown('<div style="padding-top:60px;">', unsafe_allow_html=True)
    for i, (headline, sub) in enumerate(cards):
        st.markdown(f"""
        <div class="nw-story-card">
            <div class="nw-story-number">{str(i+1).zfill(2)}</div>
            <div class="nw-story-body">{headline}</div>
            <div style="margin-top:28px; font-size:16px; color:rgba(255,255,255,0.35);
                        font-weight:300; font-family:'DM Sans',sans-serif; max-width:600px;">
                {sub}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# COMPARE MODE
# ═══════════════════════════════════════════════════

def render_compare_section(m1, fv1, m2, fv2):
    from analytics.feature_vector import compute_similarity
    similarity = compute_similarity(fv1, fv2)
    pct        = round(similarity * 100, 1)

    st.markdown('<div class="nw-section-label">PROFILE COMPARISON</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding: 60px 0 40px; background:#0f0f0f;
                border:1px solid rgba(255,255,255,0.05); margin-bottom:2px;">
        <div style="font-family:'DM Mono',monospace; font-size:10px; letter-spacing:0.4em;
                    color:rgba(229,9,20,0.8); margin-bottom:20px;">BEHAVIORAL SIMILARITY SCORE</div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:120px; line-height:1;
                    color:#fff;">{pct}<span style="font-size:0.4em; color:#E50914;">%</span></div>
        <div style="font-size:15px; color:rgba(255,255,255,0.4); margin-top:16px; font-weight:300;">
            {"You are behavioral twins — nearly identical streaming DNA." if pct > 80 
             else "Strong similarities with distinct personal signatures." if pct > 60
             else "Divergent streaming archetypes — different worlds." if pct < 40
             else "Different approaches, some common patterns."}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Side-by-side KPIs
    keys = [
        ('binge_quotient',     'Binge Quotient',    '/100'),
        ('weekend_dominance',  'Weekend Dominance', '%'),
        ('night_owl_index',    'Night Owl Index',   '%'),
        ('series_loyalty',     'Series Loyalty',    '%'),
        ('total_hours',        'Total Hours',       ' hrs'),
        ('consistency_score',  'Consistency',       '/100'),
    ]

    c1, c2 = st.columns(2, gap="small")
    for col, (m, label) in [(c1, ('Profile A', m1)), (c2, ('Profile B', m2))]:
        with col:
            arch_name = m.get('archetype', {}).get('name', '—')
            st.markdown(f"""
            <div style="background:#111; border:1px solid rgba(255,255,255,0.05);
                        padding:40px 36px; margin-bottom:2px;">
                <div style="font-family:'DM Mono',monospace; font-size:10px;
                            letter-spacing:0.35em; color:rgba(229,9,20,0.7); margin-bottom:20px;">{label}</div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:22px;
                            letter-spacing:0.06em; color:#fff; margin-bottom:4px;">{arch_name}</div>
            </div>
            """, unsafe_allow_html=True)
            for key, display, suffix in keys:
                val = m.get(key, 0)
                st.markdown(f"""
                <div style="background:#111; border:1px solid rgba(255,255,255,0.04);
                            padding:20px 28px; margin-bottom:2px; display:flex;
                            justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Mono',monospace; font-size:10px;
                                 letter-spacing:0.2em; color:rgba(255,255,255,0.3);">{display}</span>
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:32px;
                                 color:#fff;">{val}{suffix}</span>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════════

def render_dashboard(df, metrics, cluster_result, anomalies, narrative, fv, watched_titles):
    st.markdown('<div class="nw-wrapper">', unsafe_allow_html=True)

    year = datetime.now().year
    arch = metrics.get('archetype', {})

    # ── NAV
    st.markdown(f"""
    <div class="nw-nav">
        <div class="nw-logo">NETFLIX WRAPPED AI <span>BEHAVIORAL INTELLIGENCE · V2</span></div>
        <div class="nw-nav-right">
            <div class="nw-badge-red nw-badge">{arch.get('emoji','🎬')} {arch.get('name','').split()[-1]}</div>
            <div class="nw-badge">REPORT · {year}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MODE SELECTOR
    st.markdown("<br>", unsafe_allow_html=True)
    mode = st.radio(
        "VIEW MODE",
        ["📊 Dashboard", "🎬 Story Mode", "🤖 AI Report", "🔬 Deep Intelligence"],
        horizontal=True,
        label_visibility='collapsed',
    )

    # ══════════════════════════════════
    # STORY MODE
    # ══════════════════════════════════
    if mode == "🎬 Story Mode":
        render_story_mode(metrics)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ══════════════════════════════════
    # AI REPORT MODE
    # ══════════════════════════════════
    if mode == "🤖 AI Report":
        st.markdown('<div class="nw-section-label">AI BEHAVIORAL NARRATIVE REPORT</div>', unsafe_allow_html=True)

        # Cinematic opening
        st.markdown(f"""
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">OPENING ANALYSIS</div>
            <div class="nw-narrative-body">{narrative['opening']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">THE NUMBERS</div>
            <div class="nw-narrative-body">{narrative['stats']}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="small")
        with c1:
            st.markdown(f"""
            <div class="nw-narrative-section" style="height:100%;">
                <div class="nw-narrative-title">BINGE BEHAVIOR</div>
                <div class="nw-narrative-body">{narrative['binge']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="nw-narrative-section" style="height:100%;">
                <div class="nw-narrative-title">NIGHT PATTERNS</div>
                <div class="nw-narrative-body">{narrative['night']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">CONTENT IDENTITY</div>
            <div class="nw-narrative-body">{narrative['series']}</div>
        </div>
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">CONSISTENCY ANALYSIS</div>
            <div class="nw-narrative-body">{narrative['consistency']}</div>
        </div>
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">DIVERSITY FINGERPRINT</div>
            <div class="nw-narrative-body">{narrative['diversity']}</div>
        </div>
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">CIRCADIAN CLASSIFICATION</div>
            <div class="nw-narrative-body">{narrative['circadian']}</div>
        </div>
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">ARCHETYPE ANALYSIS</div>
            <div class="nw-narrative-body">{narrative['archetype_analysis']}</div>
        </div>
        <div class="nw-narrative-section">
            <div class="nw-narrative-title">CLOSING STATEMENT</div>
            <div class="nw-narrative-body">{narrative['closing']}</div>
        </div>
        """, unsafe_allow_html=True)

        # LinkedIn summary
        st.markdown('<div class="nw-section-label">LINKEDIN-READY SUMMARY</div>', unsafe_allow_html=True)
        linkedin_txt = generate_linkedin_summary(metrics, narrative)
        st.markdown(f"""
        <div style="background:#111; border:1px solid rgba(229,9,20,0.15); border-left:2px solid #E50914;
            padding:36px 40px; margin-top:2px; font-family:'DM Sans',sans-serif;">
        <div style="font-family:'DM Mono',monospace; font-size:10px; letter-spacing:0.4em;
                color:rgba(229,9,20,0.7); margin-bottom:24px;">READY TO COPY · LINKEDIN</div>
        <pre style="font-family:'DM Sans',sans-serif; font-size:14px; color:rgba(255,255,255,0.65);
                line-height:1.9; white-space:pre-wrap; margin:0; font-weight:300;">{linkedin_txt}</pre>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ══════════════════════════════════
    # DEEP INTELLIGENCE MODE
    # ══════════════════════════════════
    if mode == "🔬 Deep Intelligence":
        _render_deep_intelligence(df, metrics, cluster_result, anomalies, fv, watched_titles)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ══════════════════════════════════════════════════════════════
    # DASHBOARD MODE (PRIMARY — preserves all original sections)
    # ══════════════════════════════════════════════════════════════

    h = metrics['total_hours']

    # ── HERO
    st.markdown(f"""
    <div class="nw-hero">
        <div class="nw-hero-eyebrow">YOUR YEAR IN STREAMING · BEHAVIORAL INTELLIGENCE</div>
        <div class="nw-hero-number">
            {h:,}<span class="unit">HRS</span>
        </div>
        <div class="nw-hero-label">
            You spent <strong>{h:,} hours</strong> streaming — 
            that's <strong>{round(h/24)} days</strong> of continuous cinema.
            <br>Across <strong>{metrics['total_titles']:,} titles</strong> and 
            <strong>{metrics['days_active']} active days</strong>.
        </div>
        <div class="nw-hero-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATS STRIP
    st.markdown('<div class="nw-section-label">VIEWING FUNDAMENTALS</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="nw-stats-strip">
        <div class="nw-stat-block">
            <div class="nw-stat-num">{metrics['total_titles']:,}</div>
            <div class="nw-stat-label">UNIQUE TITLES WATCHED</div>
        </div>
        <div class="nw-stat-block">
            <div class="nw-stat-num">{metrics['days_active']}</div>
            <div class="nw-stat-label">ACTIVE VIEWING DAYS</div>
        </div>
        <div class="nw-stat-block">
            <div class="nw-stat-num">{metrics['avg_daily_hours']}</div>
            <div class="nw-stat-label">AVG HOURS PER ACTIVE DAY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── BEHAVIORAL KPIs
    bq = metrics['binge_quotient']
    wd = metrics['weekend_dominance']
    no = metrics['night_owl_index']
    sl = metrics['series_loyalty']

    def bq_d(v): return (
        "You consume entire seasons like they're single episodes." if v > 70
        else "When a show grabs you, you don't let go." if v > 40
        else "You're a measured viewer — intentional, rarely swept into a spiral."
    )
    def wd_d(v): return (
        "The weekend is your streaming sanctuary. Two days, one screen." if v > 65
        else "Weekends see a clear uplift — your primary viewing window." if v > 45
        else "Your viewing doesn't wait for the weekend. Steady rhythm all week."
    )
    def no_d(v): return (
        "The night belongs to you. After midnight is prime time." if v > 45
        else "Evening is your sweet spot — screen alive when the city quiets." if v > 20
        else "A daylight viewer. Discipline and sleep coexist peacefully."
    )
    def sl_d(v): return (
        "Series are your native language. Characters trusted across seasons." if v > 75
        else "You lean series, but know when a film is worth it." if v > 50
        else "Films hold equal ground. You're format-agnostic, story-first."
    )

    st.markdown('<div class="nw-section-label">BEHAVIORAL INTELLIGENCE LAYER</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="nw-kpi-grid">
        <div class="nw-kpi-card">
            <div class="nw-kpi-icon">◈</div>
            <div class="nw-kpi-value {'red' if bq > 55 else ''}">{bq}</div>
            <div class="nw-kpi-name">BINGE QUOTIENT</div>
            <div class="nw-kpi-desc">{bq_d(bq)}</div>
            <div class="nw-kpi-bar"><div class="nw-kpi-bar-fill" style="width:{bq}%"></div></div>
        </div>
        <div class="nw-kpi-card">
            <div class="nw-kpi-icon">◉</div>
            <div class="nw-kpi-value {'red' if wd > 60 else ''}">{wd}%</div>
            <div class="nw-kpi-name">WEEKEND DOMINANCE</div>
            <div class="nw-kpi-desc">{wd_d(wd)}</div>
            <div class="nw-kpi-bar"><div class="nw-kpi-bar-fill" style="width:{wd}%"></div></div>
        </div>
        <div class="nw-kpi-card">
            <div class="nw-kpi-icon">◐</div>
            <div class="nw-kpi-value {'red' if no > 35 else ''}">{no}%</div>
            <div class="nw-kpi-name">NIGHT OWL INDEX</div>
            <div class="nw-kpi-desc">{no_d(no)}</div>
            <div class="nw-kpi-bar"><div class="nw-kpi-bar-fill" style="width:{no}%"></div></div>
        </div>
        <div class="nw-kpi-card">
            <div class="nw-kpi-icon">▣</div>
            <div class="nw-kpi-value {'red' if sl > 70 else ''}">{sl}%</div>
            <div class="nw-kpi-name">SERIES LOYALTY SCORE</div>
            <div class="nw-kpi-desc">{sl_d(sl)}</div>
            <div class="nw-kpi-bar"><div class="nw-kpi-bar-fill" style="width:{sl}%"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INSIGHT BAND
    st.markdown(f"""
    <div class="nw-insight-band">
        <div class="nw-insight-text">
            Peak viewing hour: <strong>{metrics['peak_hour_label']}</strong> ·
            Most active day: <strong>{metrics['peak_weekday']}</strong> ·
            Most-watched: <strong>"{metrics.get('top_show','—')}"</strong> 
            ({metrics.get('top_show_count',0):,} sessions) ·
            Longest streak: <strong>{metrics.get('longest_streak',0)} days</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── EXTENDED INTELLIGENCE STRIP
    st.markdown('<div class="nw-section-label">EXTENDED METRICS</div>', unsafe_allow_html=True)
    cs  = metrics.get('consistency_score', 0)
    rs  = metrics.get('recency_score', 0)
    cdi = metrics.get('content_diversity_pct', 0)
    ls  = metrics.get('longest_streak', 0)

    st.markdown(f"""
    <div class="nw-intel-grid">
        <div class="nw-intel-card">
            <div class="nw-intel-label">CONSISTENCY SCORE</div>
            <div class="nw-intel-value {'red' if cs > 70 else ''}">{cs}</div>
            <div class="nw-intel-sub">Regularity of weekly viewing rhythm</div>
        </div>
        <div class="nw-intel-card">
            <div class="nw-intel-label">CONTENT DIVERSITY</div>
            <div class="nw-intel-value">{cdi:.0f}%</div>
            <div class="nw-intel-sub">Shannon entropy index (normalized)</div>
        </div>
        <div class="nw-intel-card">
            <div class="nw-intel-label">RECENCY SCORE</div>
            <div class="nw-intel-value {'red' if rs > 55 else ''}">{rs}</div>
            <div class="nw-intel-sub">30-day activity vs baseline</div>
        </div>
        <div class="nw-intel-card">
            <div class="nw-intel-label">LONGEST STREAK</div>
            <div class="nw-intel-value red">{ls}</div>
            <div class="nw-intel-sub">Consecutive viewing days</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TEMPORAL CHARTS
    st.markdown('<div class="nw-section-label">TEMPORAL BEHAVIOR MAPS</div>', unsafe_allow_html=True)

    chart_block(
        "MONTHLY VIEWING INTENSITY",
        "Title count across all twelve months — red marks your peak",
        monthly_chart, metrics['monthly']
    )

    c1, c2 = st.columns(2, gap="small")
    with c1:
        chart_block("WEEKDAY RHYTHM", "Which day dominates your schedule", weekday_chart, metrics['weekday_dist'])
    with c2:
        chart_block("HOURLY SIGNATURE", "Your viewing clock, hour by hour", hourly_chart, metrics['hourly'])

    chart_block(
        "VIEWING HEAT MAP",
        "Day × Hour intensity matrix — every cell is a behavioral signal",
        heatmap_chart, metrics['heatmap']
    )

    # ── MOMENTUM CHART
    chart_block(
        "7-DAY MOMENTUM CURVE",
        "Rolling average binge trend — rising or falling engagement",
        momentum_chart, metrics['daily_counts']
    )

    # ── TOP SHOWS
    if metrics.get('top_shows') is not None:
        st.markdown('<div class="nw-section-label">TITLE FREQUENCY RANKING</div>', unsafe_allow_html=True)

        col_charts = [st.columns([3, 2])]
        with col_charts[0][0]:
            chart_block(
                "MOST WATCHED TITLES",
                "Ranked by session count — red marks the champion",
                top_shows_chart, metrics['top_shows']
            )
        with col_charts[0][1]:
            if metrics.get('genre_dist') is not None:
                chart_block(
                    "GENRE DISTRIBUTION",
                    "Content type breakdown",
                    genre_chart, metrics['genre_dist']
                )

        # ── DNA RADAR CHART
    st.markdown('<div class="nw-section-label">STREAMING BEHAVIOR DNA</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1], gap="small")

    with c1:
        chart_block(
            "BEHAVIORAL RADAR",
            "8-dimensional feature vector — your streaming DNA visualized",
            radar_chart,
            metrics['feature_vector']
        )

    with c2:
        fv = metrics['feature_vector']

        # Build rows separately to avoid nested f-string triple-quote issue
        rows_html = ""

        for k, v in fv.items():
            label = k.upper().replace('_', ' ')
            pct = v * 100
            color = '#E50914' if v > 0.6 else '#fff'

            rows_html += f"""
            <div style="margin-bottom:18px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <span style="font-family:'DM Mono',monospace; font-size:10px;
                                letter-spacing:0.15em; color:rgba(255,255,255,0.3);">
                        {label}
                    </span>
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:18px; color:{color};">
                        {pct:.0f}
                    </span>
                </div>
                <div style="height:2px; background:rgba(255,255,255,0.06);">
                    <div style="height:100%; width:{pct:.0f}%; background:#E50914;
                                transition:width 1.5s cubic-bezier(0.165,0.84,0.44,1);">
                    </div>
                </div>
            </div>
            """

        components.html(f"""
        <div style="background:#0f0f0f; padding:40px 36px; font-family:'DM Sans',sans-serif;">
            <div style="font-family:'DM Mono',monospace; font-size:10px;
                        letter-spacing:0.35em; color:rgba(229,9,20,0.7); margin-bottom:32px;">
                FEATURE VECTOR · 8D
            </div>
            {rows_html}
        </div>
        """, height=400, scrolling=False)

    # ── YOY (if available)
    if metrics.get('yoy_available'):
        st.markdown('<div class="nw-section-label">YEAR-OVER-YEAR INTELLIGENCE</div>', unsafe_allow_html=True)
        yoy = metrics['yoy_data']

        yoy_blocks = ""
        for i, row in yoy.iterrows():
            delta = ""
            if i > 0:
                prev = yoy.iloc[i-1]
                diff = int(row.get('hours', 0) - prev.get('hours', 0))
                cls  = "up" if diff > 0 else "down"
                sign = "↑" if diff > 0 else "↓"
                delta = f'<div class="nw-yoy-delta {cls}">{sign} {abs(diff):.0f} hrs vs prior year</div>'

            yoy_blocks += f"""
            <div class="nw-yoy-block">
                <div class="nw-yoy-year">YEAR · {int(row['year'])}</div>
                <div class="nw-yoy-num">{int(row.get('hours', 0)):,}</div>
                <div class="nw-yoy-label">hours streamed</div>
                <div style="margin-top:8px; font-family:'DM Mono',monospace; font-size:10px;
                            color:rgba(255,255,255,0.25);">{int(row.get('titles',0)):,} titles</div>
                {delta}
            </div>
            """

            components.html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#080808; }}
        .nw-yoy-strip {{ display:flex; gap:2px; }}
        .nw-yoy-block {{ flex:1; background:#111; border:1px solid rgba(255,255,255,0.05); padding:40px 36px; }}
        .nw-yoy-year  {{ font-family:'DM Mono',monospace; font-size:11px; letter-spacing:0.3em; color:rgba(255,255,255,0.25); margin-bottom:16px; }}
        .nw-yoy-num   {{ font-family:'Bebas Neue',sans-serif; font-size:56px; line-height:1; color:#fff; margin-bottom:8px; }}
        .nw-yoy-label {{ font-family:'DM Sans',sans-serif; font-size:12px; color:rgba(255,255,255,0.3); font-weight:300; }}
        .nw-yoy-titles {{ margin-top:8px; font-family:'DM Mono',monospace; font-size:10px; color:rgba(255,255,255,0.25); }}
        .nw-yoy-delta {{ margin-top:16px; font-family:'DM Mono',monospace; font-size:11px; letter-spacing:0.15em; }}
        .up   {{ color:#22c55e; }}
        .down {{ color:#E50914; }}
    </style>
    <div class="nw-yoy-strip">{yoy_blocks}</div>
    """, height=240, scrolling=False)
        chart_block("HOURS STREAMED BY YEAR", "Annual viewing volume comparison", yoy_chart, yoy)

    # ── RECOMMENDATIONS
    st.markdown('<div class="nw-section-label">AI RECOMMENDATIONS</div>', unsafe_allow_html=True)
    recs = generate_recommendations(metrics, watched_titles, n=6)
    if recs:
        rec_cards = ""
        for r in recs:
            score_pct = round(r['score'] * 100)
            badge     = "SERIES" if r['series'] else "FILM"
            rec_cards += f"""
            <div class="nw-rec-card">
                <div class="nw-rec-genre">{r['genre']} · {badge}</div>
                <div class="nw-rec-title">{r['title'].upper()}</div>
                <div class="nw-rec-reason">{r['reason']}</div>
                <div class="nw-rec-score-bar">
                    <div class="nw-rec-score-fill" style="width:{score_pct}%"></div>
                </div>
                <div class="nw-rec-badge">MATCH {score_pct}%</div>
            </div>
            """
        components.html(f"""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ background:#080808; }}
    .nw-rec-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:2px; }}
    .nw-rec-card {{ background:#111; border:1px solid rgba(255,255,255,0.05); padding:36px 32px; transition:all 0.5s ease; }}
    .nw-rec-genre {{ font-family:'DM Mono',monospace; font-size:9px; letter-spacing:0.3em; color:rgba(229,9,20,0.7); text-transform:uppercase; margin-bottom:12px; }}
    .nw-rec-title {{ font-family:'Bebas Neue',sans-serif; font-size:28px; letter-spacing:0.04em; color:#fff; margin-bottom:12px; line-height:1; }}
    .nw-rec-reason {{ font-family:'DM Sans',sans-serif; font-size:12px; color:rgba(255,255,255,0.3); line-height:1.6; font-weight:300; }}
    .nw-rec-score-bar {{ margin-top:24px; height:1px; background:rgba(255,255,255,0.06); }}
    .nw-rec-score-fill {{ height:100%; background:rgba(229,9,20,0.4); }}
    .nw-rec-badge {{ display:inline-block; margin-top:16px; font-family:'DM Mono',monospace; font-size:9px; letter-spacing:0.2em; color:rgba(255,255,255,0.3); border:1px solid rgba(255,255,255,0.08); padding:4px 10px; }}
</style>
<div class="nw-rec-grid">{rec_cards}</div>
""", height=420, scrolling=False)

    # ── ARCHETYPE
    arch = metrics.get('archetype', {})
    traits_html = "".join([
        f'<div class="nw-trait{"highlight" if i == arch.get("highlight",0) else ""}">{t}</div>'
        for i, t in enumerate(arch.get('traits', []))
    ])
    st.markdown('<div class="nw-section-label">YOUR STREAMING IDENTITY</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="nw-archetype">
        <div class="nw-archetype-eyebrow">AI BEHAVIORAL CLASSIFICATION · ML-POWERED ANALYSIS</div>
        <div class="nw-archetype-emoji">{arch.get('emoji', '🎬')}</div>
        <div class="nw-archetype-title">
            YOUR ARCHETYPE IS
            <span class="arch-name">{arch.get('name', '—')}</span>
        </div>
        <div class="nw-archetype-desc">{arch.get('desc', '')}</div>
        <div class="nw-traits">{traits_html}</div>
    </div>
    """, unsafe_allow_html=True)

# ── EXPORT PANEL
    _render_export_panel(metrics, fv, narrative, df)

    # ── FOOTER
    st.markdown(f"""
    <div class="nw-footer">
        <div class="nw-footer-logo">NETFLIX WRAPPED AI - by Sudarshan Maddi </div>
        <div class="nw-footer-copy">BEHAVIORAL INTELLIGENCE · {year} · {metrics['total_sessions']:,} SESSIONS ANALYZED</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# EXPORT PANEL — defined OUTSIDE render_dashboard
# ═══════════════════════════════════════════════════

def _render_export_panel(metrics, fv_dict, narrative, df):
    st.markdown('<div class="nw-section-label">EXPORT & SHARE</div>', unsafe_allow_html=True)

    try:
        fv_full     = build_full_feature_vector(metrics, df)
        fv_json_str = fv_json(fv_full)
    except Exception:
        fv_json_str = "{}"

    try:
        summary_txt = export_summary_text(metrics, narrative, metrics.get('archetype', {}))
    except Exception:
        summary_txt = "Error generating report."

    try:
        linkedin_txt = generate_linkedin_summary(metrics, narrative)
    except Exception:
        linkedin_txt = "Error generating summary."

    # Convert to bytes — required for Streamlit download buttons
    if isinstance(fv_json_str, str):
        fv_json_str = fv_json_str.encode('utf-8')
    if isinstance(summary_txt, str):
        summary_txt = summary_txt.encode('utf-8')

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        st.markdown("""
        <div style="background:#0f0f0f; border:1px solid rgba(255,255,255,0.05);
                    padding:36px 32px 16px 32px;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px;
                        letter-spacing:0.04em; color:#fff; margin-bottom:6px;">FEATURE VECTOR</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.3);
                        font-weight:300; margin-bottom:24px;">8D behavioral embedding · JSON format</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "↓ DOWNLOAD JSON",
            data=fv_json_str,
            file_name="netflix_feature_vector.json",
            mime="application/json",
            use_container_width=True,
            key="dl_json",
        )

    with c2:
        st.markdown("""
        <div style="background:#0f0f0f; border:1px solid rgba(255,255,255,0.05);
                    padding:36px 32px 16px 32px;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px;
                        letter-spacing:0.04em; color:#fff; margin-bottom:6px;">TEXT REPORT</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.3);
                        font-weight:300; margin-bottom:24px;">Full intelligence report · Plain text</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "↓ DOWNLOAD REPORT",
            data=summary_txt,
            file_name="netflix_wrapped_report.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_report",
        )

    with c3:
        st.markdown("""
        <div style="background:#0f0f0f; border:1px solid rgba(255,255,255,0.05);
                    padding:36px 32px 16px 32px;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px;
                        letter-spacing:0.04em; color:#fff; margin-bottom:6px;">RAW DATA</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.3);
                        font-weight:300; margin-bottom:24px;">Processed dataset · CSV format</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "↓ DOWNLOAD CSV",
            data=dataframe_to_csv_bytes(df),
            file_name="netflix_processed.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_csv",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋  COPY LINKEDIN SUMMARY"):
        st.markdown(f"""
        <div style="background:#111; border-left:2px solid #E50914; padding:28px 32px;
                    font-family:'DM Sans',sans-serif;">
            <pre style="font-family:'DM Sans',sans-serif; font-size:14px;
                        color:rgba(255,255,255,0.65); line-height:1.9;
                        white-space:pre-wrap; margin:0; font-weight:300;">{linkedin_txt}</pre>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# DEEP INTELLIGENCE MODE
# ═══════════════════════════════════════════════════

def _render_deep_intelligence(df, metrics, cluster_result, anomalies, fv, watched_titles):
    # Anomaly detection
    st.markdown('<div class="nw-section-label">ANOMALY DETECTION · UNUSUAL PATTERNS</div>', unsafe_allow_html=True)

    binge_days = anomalies.get('binge_days', pd.DataFrame())
    detox_gaps = metrics.get('detox_gaps', [])

    c1, c2 = st.columns(2, gap="small")
    with c1:
        st.markdown("""
        <div class="nw-chart-container">
            <div class="nw-chart-title">BINGE SPIKE DAYS</div>
            <div class="nw-chart-subtitle">Days with 2.5× your daily average</div>
        </div>
        """, unsafe_allow_html=True)
        if not binge_days.empty:
            for _, row in binge_days.iterrows():
                st.markdown(f"""
                <div style="background:#111; border:1px solid rgba(255,255,255,0.04);
                            border-top:0; padding:16px 28px; display:flex;
                            justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Mono',monospace; font-size:11px;
                                 color:rgba(255,255,255,0.45);">{row['date']}</span>
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:28px;
                                 color:#E50914;">{int(row['count'])} TITLES</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#111; border:1px solid rgba(255,255,255,0.04); border-top:0; padding:28px 28px; color:rgba(255,255,255,0.3); font-size:13px;">No extreme spike days detected.</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="nw-chart-container">
            <div class="nw-chart-title">DIGITAL DETOX GAPS</div>
            <div class="nw-chart-subtitle">Streaming breaks of 7+ days</div>
        </div>
        """, unsafe_allow_html=True)
        if detox_gaps:
            for gap in detox_gaps:
                st.markdown(f"""
                <div style="background:#111; border:1px solid rgba(255,255,255,0.04);
                            border-top:0; padding:16px 28px; display:flex;
                            justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Mono',monospace; font-size:11px;
                                 color:rgba(255,255,255,0.45);">{gap['start']} → {gap['end']}</span>
                    <span style="font-family:'Bebas Neue',sans-serif; font-size:28px;
                                 color:rgba(255,255,255,0.6);">{gap['days']}D</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#111; border:1px solid rgba(255,255,255,0.04); border-top:0; padding:28px 28px; color:rgba(255,255,255,0.3); font-size:13px;">No significant detox gaps detected. You\'re committed.</div>', unsafe_allow_html=True)

    # Feature vector display
    st.markdown('<div class="nw-section-label">BEHAVIORAL FEATURE VECTOR · 8D EMBEDDING</div>', unsafe_allow_html=True)

    fv_full = build_full_feature_vector(metrics, df)
    emb     = fv_full.get('embedding', [])
    labels  = ['Binge', 'Weekend', 'Night', 'Series', 'Session', 'Consistency', 'Entropy', 'Recency']

    cols = st.columns(8)
    for col, label, val in zip(cols, labels, emb):
        with col:
            st.markdown(f"""
            <div style="background:#111; border:1px solid rgba(255,255,255,0.04);
                        padding:24px 16px; text-align:center;">
                <div style="font-family:'DM Mono',monospace; font-size:9px;
                             letter-spacing:0.2em; color:rgba(255,255,255,0.25);
                             margin-bottom:10px; text-transform:uppercase;">{label}</div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:36px;
                             color:{'#E50914' if val > 0.6 else '#fff'}; line-height:1;">
                    {val:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="nw-section-label">ADVANCED BEHAVIORAL METRICS</div>', unsafe_allow_html=True)

    cz   = metrics.get('circadian_label', '—')
    mtrend = metrics.get('momentum_trend', 'stable').upper()
    gap_days = metrics.get('total_gap_days', 0)
    shannon  = metrics.get('shannon_entropy', 0)

    st.markdown(f"""
    <div class="nw-intel-grid">
        <div class="nw-intel-card">
            <div class="nw-intel-label">CIRCADIAN TYPE</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px; color:#fff; line-height:1.2; margin-bottom:8px;">{cz}</div>
            <div class="nw-intel-sub">{metrics.get('dominant_zone','—').title()} zone dominant</div>
        </div>
        <div class="nw-intel-card">
            <div class="nw-intel-label">MOMENTUM TREND</div>
            <div class="nw-intel-value {'red' if mtrend=='RISING' else ''}">{mtrend}</div>
            <div class="nw-intel-sub">30-day vs baseline activity</div>
        </div>
        <div class="nw-intel-card">
            <div class="nw-intel-label">SHANNON ENTROPY</div>
            <div class="nw-intel-value">{shannon}</div>
            <div class="nw-intel-sub">Content diversity index</div>
        </div>
        <div class="nw-intel-card">
            <div class="nw-intel-label">DETOX DAYS TOTAL</div>
            <div class="nw-intel-value">{gap_days}</div>
            <div class="nw-intel-sub">Days with zero streaming</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# EXPORT PANEL
# ═══════════════════════════════════════════════════

def _render_export_panel(metrics, fv_dict, narrative, df):
    st.markdown('<div class="nw-section-label">EXPORT & SHARE</div>', unsafe_allow_html=True)

    fv_full = build_full_feature_vector(metrics, df)
    fv_json_str  = fv_json(fv_full)
    summary_txt  = export_summary_text(metrics, narrative, metrics.get('archetype', {}))
    linkedin_txt = generate_linkedin_summary(metrics, narrative)

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        st.markdown("""
        <div style="background:#0f0f0f; border:1px solid rgba(255,255,255,0.05); padding:36px 32px;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px; letter-spacing:0.04em; color:#fff; margin-bottom:6px;">FEATURE VECTOR</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.3); margin-bottom:24px; font-weight:300;">8D behavioral embedding · JSON format</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "↓ DOWNLOAD JSON",
            data=fv_json_str,
            file_name="netflix_feature_vector.json",
            mime="application/json",
            use_container_width=True,
        )

    with c2:
        st.markdown("""
        <div style="background:#0f0f0f; border:1px solid rgba(255,255,255,0.05); padding:36px 32px;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px; letter-spacing:0.04em; color:#fff; margin-bottom:6px;">TEXT REPORT</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.3); margin-bottom:24px; font-weight:300;">Full intelligence report · Plain text</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "↓ DOWNLOAD REPORT",
            data=summary_txt,
            file_name="netflix_wrapped_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with c3:
        st.markdown("""
        <div style="background:#0f0f0f; border:1px solid rgba(255,255,255,0.05); padding:36px 32px;">
            <div style="font-family:'Bebas Neue',sans-serif; font-size:22px; letter-spacing:0.04em; color:#fff; margin-bottom:6px;">RAW DATA</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.3); margin-bottom:24px; font-weight:300;">Processed dataset · CSV format</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "↓ DOWNLOAD CSV",
            data=dataframe_to_csv_bytes(df),
            file_name="netflix_processed.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # LinkedIn copy box
    with st.expander("📋  COPY LINKEDIN SUMMARY"):
        st.code(linkedin_txt, language=None)


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def process_data(raw_csv_bytes):
    import io
    df  = pd.read_csv(io.BytesIO(raw_csv_bytes))
    df  = parse_netflix_csv(df)
    return df


def run_analytics(df_json: str):
    df = pd.read_json(df_json)
    df['date'] = pd.to_datetime(df['date'])
    if 'date_only' in df.columns:
        df['date_only'] = pd.to_datetime(df['date_only']).dt.date
    metrics  = compute_all_metrics(df)
    cluster_result, _ = cluster_viewing_sessions(df)
    anomalies = detect_anomalies(df)
    narrative = generate_narrative_report(metrics)
    fv        = build_full_feature_vector(metrics, df)
    return metrics, cluster_result, anomalies, narrative, fv


def main():
    for key in ['df', 'df2', 'metrics', 'metrics2', 'cluster', 'anomalies',
                'narrative', 'fv', 'fv2', 'compare_mode']:
        if key not in st.session_state:
            st.session_state[key] = None

    if st.session_state.df is None:
        uploaded, uploaded2, demo, compare_mode = render_upload_screen()
        st.session_state.compare_mode = compare_mode

        if demo:
            with st.spinner(""):
                df = generate_demo_data()
                st.session_state.df = df
            st.rerun()

        if uploaded is not None:
            with st.spinner(""):
                try:
                    raw = uploaded.read()
                    df  = process_data(raw)
                    if len(df) == 0:
                        st.error("⚠ No data found. Check your CSV format.")
                    else:
                        st.session_state.df = df
                        if compare_mode and uploaded2:
                            raw2 = uploaded2.read()
                            df2  = process_data(raw2)
                            st.session_state.df2 = df2
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠ Error: {e}")
    else:
        # Reset button
        _, _, reset_col = st.columns([10, 1, 1])
        with reset_col:
            if st.button("↩", help="Reset"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        df = st.session_state.df

        # Run analytics (cached)
        with st.spinner(""):
            metrics, cluster_result, anomalies, narrative, fv = run_analytics(df.to_json())
            st.session_state.metrics   = metrics
            st.session_state.cluster   = cluster_result
            st.session_state.anomalies = anomalies
            st.session_state.narrative = narrative
            st.session_state.fv        = fv

        watched_titles = df['show_name'].unique().tolist() if 'show_name' in df.columns else []

        # Compare mode
        if st.session_state.compare_mode and st.session_state.df2 is not None:
            metrics2, _, _, _, fv2 = run_analytics(st.session_state.df2.to_json())
            render_dashboard(df, metrics, cluster_result, anomalies, narrative, fv, watched_titles)
            render_compare_section(metrics, fv['behavioral'], metrics2, fv2['behavioral'])
        else:
            render_dashboard(df, metrics, cluster_result, anomalies, narrative, fv, watched_titles)


if __name__ == "__main__":
    main()
