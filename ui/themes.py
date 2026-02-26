"""
Netflix Wrapped AI — Master Theme System
All CSS injected into Streamlit. Cinematic immersion engine.
"""

MASTER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════════════
   ROOT RESET & FOUNDATIONS
   ═══════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --red:      #E50914;
    --red-glow: rgba(229,9,20,0.5);
    --red-soft: rgba(229,9,20,0.08);
    --bg:       #080808;
    --bg2:      #0f0f0f;
    --bg3:      #141414;
    --card:     #111111;
    --border:   rgba(255,255,255,0.05);
    --border2:  rgba(255,255,255,0.09);
    --text:     #E6E6E6;
    --text2:    rgba(255,255,255,0.5);
    --text3:    rgba(255,255,255,0.25);
    --font-display: 'Bebas Neue', sans-serif;
    --font-body:    'DM Sans', sans-serif;
    --font-mono:    'DM Mono', monospace;
    --ease:     cubic-bezier(0.165, 0.84, 0.44, 1);
    --ease2:    cubic-bezier(0.4, 0, 0.2, 1);
}

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    overflow-x: hidden;
    scroll-behavior: smooth;
}

/* ── Deep Kill Streamlit Header & Toolbar ── */
header[data-testid="stHeader"] {
    display: none !important;
}

/* This kills the 'Return' / 'Explorer' button on the top right */
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* This targets the main container padding specifically */
.stMainBlockContainer {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* Force the app to the absolute top */
.stAppViewMain {
    margin-top: -60px !important; /* Adjust if needed to pull content up */
}

/* Ensure the wrapper doesn't have its own top padding */
.nw-nav {
    padding-top: 20px !important; /* Reduced from 36px */
}

/* ── Kill Streamlit chrome ── */
#MainMenu, footer, header               { visibility: hidden !important; height: 0 !important; }
.stDeployButton                         { display: none !important; }
[data-testid="stToolbar"]              { display: none !important; }
[data-testid="stDecoration"]           { display: none !important; }
[data-testid="stSidebar"]              { display: none !important; }
section[data-testid="stSidebar"]       { display: none !important; }
.block-container                        { padding: 0 !important; max-width: 100% !important; margin-top: 0 !important; }
[data-testid="stVerticalBlock"]        { gap: 0 !important; }

/* ── Kill ALL top gap sources ── */
.main .block-container                 { padding-top: 0 !important; }
[data-testid="stAppViewContainer"]     { padding-top: 0 !important; }
[data-testid="stAppViewBlockContainer"]{ padding-top: 0 !important; }
section.main > div                     { padding-top: 0 !important; }
.stApp > header                        { display: none !important; height: 0 !important; min-height: 0 !important; }
[data-testid="stHeader"]               { display: none !important; height: 0 !important; }
[data-testid="stStatusWidget"]         { display: none !important; }

/* Kill Streamlit top spacer */
section.main {
    padding-top: 0px !important;
}

section.main > div:first-child {
    padding-top: 0px !important;
    margin-top: 0px !important;
}

.stApp {
    padding-top: 0px !important;
}

header {
    height: 0px !important;
    min-height: 0px !important;
}

.stApp > header {
    display: none !important;
}

/* ── Ambient Light System ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 50% 0%, rgba(229,9,20,0.09) 0%, transparent 65%),
        radial-gradient(ellipse 40% 40% at 85% 85%, rgba(229,9,20,0.05) 0%, transparent 55%),
        radial-gradient(ellipse 50% 50% at -10% 50%, rgba(229,9,20,0.04) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
    animation: ambientPulse 12s ease-in-out infinite;
}

/* ── Film Grain Overlay ── */
.stApp::after {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 1;
    opacity: 0.35;
}

/* ═══════════════════════════════════════════════════
   LAYOUT WRAPPERS
   ═══════════════════════════════════════════════════ */
.nw-wrapper {
    position: relative; z-index: 2;
    max-width: 1440px;
    margin: -130px auto 0;
    padding: 0 56px 140px;
}

/* ═══════════════════════════════════════════════════
   NAV BAR
   ═══════════════════════════════════════════════════ */
.nw-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 0 20px;
    border-bottom: 1px solid var(--border);
    animation: fadeSlideDown 0.7s var(--ease) both;
}
.nw-logo {
    font-family: var(--font-display);
    font-size: 26px; letter-spacing: 0.14em;
    color: var(--red);
    text-shadow: 0 0 40px var(--red-glow);
}
.nw-logo span {
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.22em;
    color: var(--text3); margin-left: 18px; vertical-align: middle;
}
.nw-nav-right { display: flex; align-items: center; gap: 16px; }
.nw-badge {
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.3em;
    color: var(--text3); border: 1px solid var(--border2);
    padding: 7px 14px; border-radius: 1px;
}
.nw-badge-red {
    border-color: rgba(229,9,20,0.25);
    color: rgba(229,9,20,0.7);
    background: var(--red-soft);
}

/* ── Progress Bar (top of page) ── */
.nw-progress-bar {
    position: fixed; top: 0; left: 0; right: 0; height: 2px; z-index: 9999;
    background: rgba(255,255,255,0.05);
}
.nw-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #E50914, #ff4d4d);
    box-shadow: 0 0 12px var(--red-glow);
    transition: width 0.4s var(--ease);
}

/* ═══════════════════════════════════════════════════
   HERO SECTION
   ═══════════════════════════════════════════════════ */
.nw-hero {
    padding: 60px 0 70px;
    text-align: center; position: relative;
}
.nw-hero-eyebrow {
    font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.45em;
    color: var(--red); text-transform: uppercase;
    margin-bottom: 40px;
    animation: fadeSlideDown 0.9s var(--ease) 0.1s both;
}
.nw-hero-number {
    font-family: var(--font-display);
    font-size: clamp(110px, 18vw, 230px);
    line-height: 0.85; letter-spacing: -0.02em;
    color: #fff; position: relative; display: inline-block;
    animation: heroReveal 1.2s var(--ease) 0.25s both;
}
.nw-hero-number .unit {
    font-size: 0.3em; color: var(--red);
    vertical-align: super; margin-left: 6px;
    text-shadow: 0 0 60px var(--red-glow), 0 0 120px rgba(229,9,20,0.3);
    animation: redGlow 3.5s ease-in-out 1.5s infinite;
}
.nw-hero-label {
    font-size: clamp(15px, 2.2vw, 24px);
    font-weight: 300; letter-spacing: 0.04em;
    color: var(--text2); margin-top: 28px;
    animation: fadeSlideUp 1s var(--ease) 0.5s both;
}
.nw-hero-label strong { color: var(--text); font-weight: 600; }

.nw-hero-divider {
    width: 1px; height: 80px;
    background: linear-gradient(to bottom, transparent, rgba(229,9,20,0.5), transparent);
    margin: 64px auto 0;
    animation: fadeIn 1.2s ease 1s both;
}

/* ═══════════════════════════════════════════════════
   SECTION LABELS (Cinematic Upgrade)
   ═══════════════════════════════════════════════════ */
.nw-section-label {
    font-family: var(--font-display);
    font-size: 34px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--red);
    padding-top: 90px;
    margin-bottom: 48px;
    display: flex;
    align-items: center;
    gap: 26px;
    text-shadow: 0 0 30px rgba(229,9,20,0.25);
}

.nw-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(229,9,20,0.25);
}

/* ═══════════════════════════════════════════════════
   STATS STRIP
   ═══════════════════════════════════════════════════ */
.nw-stats-strip {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 2px; margin-bottom: 2px;
}
.nw-stat-block {
    background: var(--card); border: 1px solid var(--border);
    padding: 44px 40px; text-align: center;
    transition: all 0.5s var(--ease);
    position: relative; overflow: hidden;
}
.nw-stat-block::before {
    content: ''; position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(229,9,20,0.06), transparent 70%);
    opacity: 0; transition: opacity 0.5s var(--ease);
}
.nw-stat-block:hover { border-color: rgba(229,9,20,0.12); transform: translateY(-2px); }
.nw-stat-block:hover::before { opacity: 1; }
.nw-stat-num {
    font-family: var(--font-display); font-size: 60px;
    color: #fff; line-height: 1; margin-bottom: 10px;
}
.nw-stat-label {
    font-family: var(--font-mono); font-size: 10px;
    letter-spacing: 0.3em; color: var(--text3); text-transform: uppercase;
}

/* ═══════════════════════════════════════════════════
   KPI CARDS — BEHAVIORAL INTELLIGENCE
   ═══════════════════════════════════════════════════ */
.nw-kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 2px; margin-bottom: 2px;
}
.nw-kpi-card {
    background: var(--card); border: 1px solid var(--border);
    padding: 44px 38px;
    position: relative; overflow: hidden; cursor: default;
    transition: all 0.5s var(--ease);
}
.nw-kpi-card::before {
    content: ''; position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: var(--red);
    transform: scaleX(0); transform-origin: left;
    transition: transform 0.5s var(--ease);
}
.nw-kpi-card::after {
    content: ''; position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 100%, rgba(229,9,20,0.06), transparent 70%);
    opacity: 0; transition: opacity 0.5s var(--ease);
}
.nw-kpi-card:hover { border-color: rgba(229,9,20,0.2); transform: translateY(-4px); }
.nw-kpi-card:hover::before { transform: scaleX(1); }
.nw-kpi-card:hover::after { opacity: 1; }
.nw-kpi-icon { font-size: 16px; margin-bottom: 36px; opacity: 0.5; }
.nw-kpi-value {
    font-family: var(--font-display); font-size: 72px; line-height: 1;
    color: #fff; letter-spacing: 0.02em; margin-bottom: 8px;
}
.nw-kpi-value.red {
    color: var(--red);
    text-shadow: 0 0 40px rgba(229,9,20,0.35);
}
.nw-kpi-name {
    font-family: var(--font-mono); 
    font-size: 10px; 
    letter-spacing: 0.22em;
    text-transform: uppercase; 
    color: var(--text3); 
    margin-bottom: 22px;
}
.nw-kpi-desc {
    font-size: 13px; color: var(--text2); line-height: 1.65; font-weight: 300;
}
.nw-kpi-bar {
    margin-top: 28px; height: 2px;
    background: rgba(255,255,255,0.06); border-radius: 1px; overflow: hidden;
}
.nw-kpi-bar-fill {
    height: 100%; background: var(--red); border-radius: 1px;
    transition: width 2s var(--ease);
}

/* ═══════════════════════════════════════════════════
   INSIGHT BAND — Upgraded Layout Separation
   ═══════════════════════════════════════════════════ */

.nw-insight-band {
    background: linear-gradient(
        90deg,
        rgba(229,9,20,0.08) 0%,
        rgba(229,9,20,0.04) 30%,
        transparent 85%
    );
    
    border-left: 3px solid var(--red);
    
    padding: 28px 40px;
    
    /* THIS fixes the clash */
    margin: 24px 0 80px 0;
    
    position: relative;
}

/* Optional subtle bottom divider to visually close band */
.nw-insight-band::after {
    content: "";
    position: absolute;
    bottom: -40px;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

.nw-insight-text {
    font-size: 17px;
    color: var(--text2);
    line-height: 1.85;
    font-weight: 300;
    max-width: 1100px;
}

.nw-insight-text strong {
    color: var(--text);
    font-weight: 600;
}

/* ═══════════════════════════════════════════════════
   CHART CONTAINERS
   ═══════════════════════════════════════════════════ */
.nw-chart-container {
    background: var(--bg2);
    border: 1px solid var(--border);
    padding: 48px 44px 40px;
    position: relative;
}
.nw-chart-inner {
    background: var(--bg2);
    border: 1px solid var(--border); border-top: 0;
    padding: 0 36px 36px;
}
.nw-chart-title {
    font-family: var(--font-display); font-size: 30px; letter-spacing: 0.06em;
    color: #fff; margin-bottom: 6px;
}
.nw-chart-subtitle {
    font-size: 13px; color: var(--text3); font-weight: 300;
}

/* ═══════════════════════════════════════════════════
   ARCHETYPE REVEAL
   ═══════════════════════════════════════════════════ */
.nw-archetype {
    background: var(--bg2);
    border: 1px solid rgba(229,9,20,0.15);
    padding: 100px 80px; text-align: center;
    position: relative; overflow: hidden;
    margin-top: 2px;
}
.nw-archetype::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 60% at 50% 50%, rgba(229,9,20,0.06), transparent 65%);
    pointer-events: none;
}
.nw-archetype-eyebrow {
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.5em;
    color: var(--red); margin-bottom: 28px; opacity: 0.85;
}
.nw-archetype-emoji { font-size: 48px; margin-bottom: 24px; display: block; }
.nw-archetype-title {
    font-family: var(--font-display);
    font-size: clamp(52px, 8vw, 100px);
    line-height: 0.9; letter-spacing: 0.03em;
    color: #fff; margin-bottom: 12px;
    position: relative; z-index: 1;
}
.nw-archetype-title .arch-name {
    color: var(--red); display: block;
    text-shadow: 0 0 80px rgba(229,9,20,0.45);
}
.nw-archetype-desc {
    font-size: 17px; color: var(--text2); line-height: 1.85;
    max-width: 620px; margin: 32px auto 56px; font-weight: 300;
    position: relative; z-index: 1;
}
.nw-traits {
    display: flex; justify-content: center; gap: 4px; flex-wrap: wrap;
    position: relative; z-index: 1;
}
.nw-trait {
    padding: 10px 22px; border: 1px solid var(--border2);
    font-family: var(--font-mono); font-size: 10px;
    letter-spacing: 0.22em; color: var(--text2); text-transform: uppercase;
    background: rgba(255,255,255,0.02);
    transition: all 0.4s var(--ease);
}
.nw-trait:hover { border-color: rgba(255,255,255,0.2); color: var(--text); }
.nw-trait.highlight {
    border-color: rgba(229,9,20,0.35);
    color: var(--red);
    background: rgba(229,9,20,0.06);
}

/* ═══════════════════════════════════════════════════
   NARRATIVE REPORT — Executive AI Report Upgrade
   ═══════════════════════════════════════════════════ */

.nw-narrative-section {
    background: linear-gradient(180deg, var(--bg2), #0c0c0c);
    border: 1px solid rgba(229,9,20,0.12);
    padding: 90px 100px;
    margin-bottom: 2px;
    position: relative;
    transition: all 0.4s var(--ease);
}

.nw-narrative-section::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(to bottom, var(--red), transparent);
}

/* Section Headers (OPENING ANALYSIS, THE NUMBERS, etc.) */
.nw-narrative-title {
    font-family: var(--font-display);
    font-size: 22px;
    letter-spacing: 0.18em;
    color: var(--red);
    text-transform: uppercase;
    margin-bottom: 34px;
    text-shadow: 0 0 20px rgba(229,9,20,0.3);
}

/* Main Body Text */
.nw-narrative-body {
    font-size: 21px;
    line-height: 1.95;
    color: rgba(255,255,255,0.9);
    font-weight: 400;
    font-style: normal;
    max-width: 900px;
}

/* Strong Highlights */
.nw-narrative-body strong {
    color: #ffffff;
    font-weight: 600;
}

/* ═══════════════════════════════════════════════════
   RECOMMENDATION CARDS
   ═══════════════════════════════════════════════════ */
.nw-rec-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 2px; margin-bottom: 2px;
}
.nw-rec-card {
    background: var(--card); border: 1px solid var(--border);
    padding: 36px 32px;
    position: relative; overflow: hidden;
    transition: all 0.5s var(--ease);
}
.nw-rec-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(229,9,20,0.4), transparent);
    transform: scaleX(0); transform-origin: center;
    transition: transform 0.5s var(--ease);
}
.nw-rec-card:hover { border-color: rgba(229,9,20,0.15); transform: translateY(-3px); }
.nw-rec-card:hover::before { transform: scaleX(1); }
.nw-rec-genre {
    font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.3em;
    color: rgba(229,9,20,0.7); text-transform: uppercase; margin-bottom: 12px;
}
.nw-rec-title {
    font-family: var(--font-display); font-size: 28px; letter-spacing: 0.04em;
    color: #fff; margin-bottom: 12px; line-height: 1;
}
.nw-rec-reason {
    font-size: 12px; color: var(--text3); line-height: 1.6; font-weight: 300;
}
.nw-rec-score-bar {
    margin-top: 24px; height: 1px;
    background: rgba(255,255,255,0.06);
}
.nw-rec-score-fill {
    height: 100%; background: rgba(229,9,20,0.4);
    transition: width 1.5s var(--ease);
}
.nw-rec-badge {
    display: inline-block; margin-top: 16px;
    font-family: var(--font-mono); font-size: 9px;
    letter-spacing: 0.2em; color: var(--text3);
    border: 1px solid var(--border); padding: 4px 10px;
}

/* ═══════════════════════════════════════════════════
   CLUSTER VISUALIZATION
   ═══════════════════════════════════════════════════ */
.nw-cluster-profiles {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 2px; margin-top: 2px;
}
.nw-cluster-profile {
    background: var(--card); border: 1px solid var(--border);
    padding: 36px 32px;
    transition: all 0.4s var(--ease);
}
.nw-cluster-profile:hover { border-color: rgba(229,9,20,0.12); }
.nw-cluster-num {
    font-family: var(--font-display); font-size: 52px;
    line-height: 1;
    color: rgba(229,9,20,0.3); margin-bottom: 12px;
}
.nw-cluster-name {
    font-family: var(--font-display); font-size: 22px;
    letter-spacing: 0.05em; color: #fff; margin-bottom: 8px;
}
.nw-cluster-desc {
    font-size: 13px; color: var(--text2); line-height: 1.6; font-weight: 300;
    margin-bottom: 20px;
}
.nw-cluster-meta {
    font-family: var(--font-mono); font-size: 10px;
    letter-spacing: 0.15em; color: var(--text3);
}

/* ═══════════════════════════════════════════════════
   STREAK / INTELLIGENCE CARDS
   ═══════════════════════════════════════════════════ */
.nw-intel-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 2px; margin-bottom: 2px;
}
.nw-intel-card {
    background: var(--card); border: 1px solid var(--border);
    padding: 36px 30px;
    transition: all 0.4s var(--ease);
}
.nw-intel-card:hover { border-color: var(--border2); transform: translateY(-2px); }
.nw-intel-label {
    font-family: var(--font-mono); font-size: 9px;
    letter-spacing: 0.3em; color: var(--text3);
    text-transform: uppercase; margin-bottom: 16px;
}
.nw-intel-value {
    font-family: var(--font-display); font-size: 44px;
    line-height: 1; color: #fff; margin-bottom: 8px;
}
.nw-intel-value.red { color: var(--red); }
.nw-intel-sub { font-size: 12px; color: var(--text3); font-weight: 300; }

/* ═══════════════════════════════════════════════════
   EXPORT / SHARE PANEL — Stable Grid Layout
   ═══════════════════════════════════════════════════ */

.nw-export-panel {
    background: var(--bg2);
    border: 1px solid var(--border);

    padding: 64px 56px;
    margin: 60px 0 80px 0;

    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2px;
}

.nw-export-panel > div {
    background: var(--card);
    border: 1px solid var(--border);

    padding: 48px 40px;
    min-height: 230px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    transition: all 0.4s var(--ease);
}

.nw-export-panel > div:hover {
    border-color: rgba(229,9,20,0.2);
    transform: translateY(-3px);
}

.nw-export-title {
    font-family: var(--font-display);
    font-size: 26px;
    letter-spacing: 0.04em;
    color: #fff;
    margin-bottom: 12px;
}

.nw-export-desc {
    font-size: 14px;
    color: var(--text3);
    font-weight: 300;
    line-height: 1.6;
}

/* ═══════════════════════════════════════════════════
   YOY COMPARISON
   ═══════════════════════════════════════════════════ */
.nw-yoy-strip {
    display: flex; gap: 2px; margin-bottom: 2px;
}
.nw-yoy-block {
    flex: 1; background: var(--card);
    border: 1px solid var(--border); padding: 40px 36px;
}
.nw-yoy-year {
    font-family: var(--font-mono); font-size: 11px;
    letter-spacing: 0.3em; color: var(--text3); margin-bottom: 16px;
}
.nw-yoy-num {
    font-family: var(--font-display); font-size: 56px;
    line-height: 1; color: #fff; margin-bottom: 8px;
}
.nw-yoy-label { font-size: 12px; color: var(--text3); font-weight: 300; }
.nw-yoy-delta {
    margin-top: 16px; font-family: var(--font-mono); font-size: 11px;
    letter-spacing: 0.15em;
}
.nw-yoy-delta.up   { color: #22c55e; }
.nw-yoy-delta.down { color: var(--red); }

/* ═══════════════════════════════════════════════════
   UPLOAD SCREEN
   ═══════════════════════════════════════════════════ */
.nw-upload-screen {
    min-height: 100vh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 60px 40px;
    position: relative; z-index: 2;
}
.nw-upload-logo {
    font-family: var(--font-display); font-size: 46px;
    letter-spacing: 0.15em; color: var(--red);
    text-shadow: 0 0 60px var(--red-glow);
    margin-bottom: 16px;
    animation: fadeSlideDown 0.8s var(--ease) both;
}
.nw-upload-tagline {
    font-family: var(--font-mono); font-size: 11px;
    letter-spacing: 0.35em; color: var(--text3);
    margin-bottom: 80px;
    animation: fadeSlideDown 0.8s var(--ease) 0.1s both;
}
.nw-upload-headline {
    font-family: var(--font-display);
    font-size: clamp(54px, 9vw, 100px); line-height: 0.92;
    letter-spacing: 0.02em; color: #fff;
    margin-bottom: 28px; max-width: 820px;
    animation: fadeSlideUp 1s var(--ease) 0.2s both;
}
.nw-upload-headline em { color: var(--red); font-style: normal; }
.nw-upload-sub {
    font-size: 16px; color: var(--text2); line-height: 1.75;
    max-width: 520px; margin: 0 auto 64px; font-weight: 300;
    animation: fadeSlideUp 1s var(--ease) 0.3s both;
}
.nw-steps {
    display: flex; gap: 2px; max-width: 700px;
    animation: fadeSlideUp 1s var(--ease) 0.5s both;
}
.nw-step {
    flex: 1; background: var(--card);
    border: 1px solid var(--border); padding: 28px 24px; text-align: left;
    transition: all 0.4s var(--ease);
}
.nw-step:hover { border-color: var(--border2); }
.nw-step-num {
    font-family: var(--font-display); font-size: 44px;
    color: rgba(229,9,20,0.25); line-height: 1; margin-bottom: 12px;
}
.nw-step-text { font-size: 12px; color: var(--text3); line-height: 1.6; font-weight: 300; }
.nw-step-text strong { color: rgba(255,255,255,0.55); }

/* ── File uploader overrides ── */
[data-testid="stFileUploader"] { animation: fadeSlideUp 1s var(--ease) 0.4s both; }
[data-testid="stFileUploaderDropzone"] {
    background: rgba(229,9,20,0.03) !important;
    border: 1px solid rgba(229,9,20,0.18) !important;
    border-radius: 0 !important; padding: 44px !important;
    transition: all 0.4s var(--ease) !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    background: rgba(229,9,20,0.06) !important;
    border-color: rgba(229,9,20,0.35) !important;
}

/* ── Button styling ── */
.stButton > button {
    border-radius: 0 !important;
    font-family: var(--font-mono) !important;
    letter-spacing: 0.2em !important;
    font-size: 11px !important;
    transition: all 0.4s var(--ease) !important;
}
.stButton > button[kind="primary"] {
    background: var(--red) !important;
    border: none !important; color: #fff !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--text2) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    background: var(--card) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 0.2em !important;
    color: var(--text3) !important;
    border-radius: 0 !important;
    padding: 16px 24px !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    border-bottom: 2px solid var(--red) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 0 !important;
    background: transparent !important;
}

/* ── Selectbox / slider ── */
[data-testid="stSelectbox"] > div { border-radius: 0 !important; }

/* ═══════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════ */
.nw-footer {
    padding: 56px 0 36px; border-top: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 80px;
}
.nw-footer-logo {
    font-family: var(--font-display); font-size: 22px;
    letter-spacing: 0.12em; color: rgba(229,9,20,0.5);
}
.nw-footer-copy {
    font-family: var(--font-mono); font-size: 10px;
    letter-spacing: 0.2em; color: var(--text3);
}

/* ═══════════════════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: rgba(229,9,20,0.3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(229,9,20,0.55); }

/* ═══════════════════════════════════════════════════
   PLOTLY OVERRIDE
   ═══════════════════════════════════════════════════ */
[data-testid="stPlotlyChart"] { border: none !important; background: transparent !important; }

/* ═══════════════════════════════════════════════════
   KEYFRAMES
   ═══════════════════════════════════════════════════ */
@keyframes fadeSlideDown {
    from { opacity:0; transform:translateY(-24px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity:0; transform:translateY(36px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeIn {
    from { opacity:0; } to { opacity:1; }
}
@keyframes heroReveal {
    from { opacity:0; transform:translateY(50px) scale(0.95); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes redGlow {
    0%,100% { text-shadow: 0 0 60px rgba(229,9,20,0.8),0 0 120px rgba(229,9,20,0.35); }
    50%      { text-shadow: 0 0 90px rgba(229,9,20,1),0 0 180px rgba(229,9,20,0.5); }
}
@keyframes ambientPulse {
    0%,100% { opacity:1; }
    50%      { opacity:0.75; }
}
@keyframes shimmer {
    0%   { transform:translateX(-100%); }
    100% { transform:translateX(400%); }
}

/* ═══════════════════════════════════════════════════
   STORY MODE OVERLAY
   ═══════════════════════════════════════════════════ */
.nw-story-card {
    background: var(--bg2);
    border: 1px solid rgba(229,9,20,0.12);
    padding: 80px 72px; text-align: center;
    margin-bottom: 2px; position: relative;
    min-height: 400px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.nw-story-number {
    font-family: var(--font-display); font-size: 140px;
    line-height: 1; color: rgba(229,9,20,0.12);
    position: absolute; right: 48px; top: 40px; letter-spacing: -0.04em;
}
.nw-story-body {
    font-family: var(--font-display); font-size: clamp(32px, 4vw, 52px);
    line-height: 1.15; color: #fff; letter-spacing: 0.02em;
    max-width: 800px; position: relative; z-index: 1;
}
.nw-story-body .red { color: var(--red); }

/* ═══════════════════════════════════════════════════
   GLOBAL DESCRIPTION SIZE UPGRADE
   Makes all helper/subtext bigger across entire app
   ═══════════════════════════════════════════════════ */

.nw-kpi-desc,
.nw-intel-sub,
.nw-yoy-label,
.nw-rec-reason,
.nw-stat-label,
.nw-archetype-desc,
.nw-export-desc,
.nw-cluster-desc,
.nw-step-text,
.nw-narrative-body,
.nw-chart-subtitle {
    font-size: 16px !important;
    line-height: 1.8 !important;
    font-weight: 400 !important;
    color: var(--text2) !important;
}

/* ═══════════════════════════════════════════════════
   GLOBAL METRIC TITLE UPGRADE
   Makes uppercase labels bigger + red-accented
   ═══════════════════════════════════════════════════ */

.nw-kpi-name,
.nw-intel-label,
.nw-yoy-year,
.nw-rec-genre,
.nw-stat-label {
    font-family: var(--font-display) !important;
    font-size: 16px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: rgba(229,9,20,0.85) !important;
    margin-bottom: 18px !important;
}

/* ═══════════════════════════════════════════════════
   GLASSMORPHISM PANEL
   ═══════════════════════════════════════════════════ */
.nw-glass {
    background: rgba(17,17,17,0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.07);
}


/* ═══════════════════════════════════════════════════
   MODE NAV (Dashboard / Story / AI / Deep)
   Cinematic Top Navigation Upgrade
   ═══════════════════════════════════════════════════ */

/* Kill default radio circle */
div[role="radiogroup"] > label > div:first-child {
    display: none;
}

/* Navigation container */
div[role="radiogroup"] {
    display: flex;
    align-items: center;
    gap: 42px;
    margin-top: 28px;
    margin-bottom: 22px;
    padding-left: 2px;
}

/* Base tab style */
div[role="radiogroup"] label {
    font-family: var(--font-display) !important;
    font-size: 21px !important;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.32) !important;
    padding-bottom: 12px;
    border-bottom: 2px solid transparent;
    transition: all 0.35s var(--ease);
    cursor: pointer;
    position: relative;
}

/* Subtle glow on hover */
div[role="radiogroup"] label:hover {
    color: #ffffff !important;
    text-shadow: 0 0 14px rgba(255,255,255,0.2);
}

/* Active tab (bulletproof selector) */
div[role="radiogroup"] label:has(input:checked) {
    color: var(--red) !important;
    text-shadow: 0 0 30px var(--red-glow);
    border-bottom: 2px solid var(--red);
}

/* Smooth cinematic underline animation */
div[role="radiogroup"] label::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -2px;
    height: 2px;
    width: 100%;
    background: var(--red);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.35s var(--ease);
}

div[role="radiogroup"] label:has(input:checked)::after {
    transform: scaleX(1);
}
</style>
"""


def inject_theme():
    """Inject master CSS into Streamlit."""
    import streamlit as st
    st.markdown(MASTER_CSS, unsafe_allow_html=True)
