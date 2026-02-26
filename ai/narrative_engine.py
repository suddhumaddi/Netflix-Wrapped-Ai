"""
Netflix Wrapped AI — Narrative Engine
Generates cinematic, AI-powered behavioral personality reports.
Supports both template-based and Claude API generation.
"""

import random
import textwrap
from typing import Dict, Any, Optional


# ─────────────────────────────────────────────
# NARRATIVE TEMPLATES (Template Engine)
# ─────────────────────────────────────────────

OPENING_FRAMES = [
    "There is a version of you that only exists after dark — restless, hungry for story, unwilling to let the night pass empty.",
    "Every tap of a remote is a small act of self-revelation. Collectively, yours paint a portrait stranger and more precise than you might expect.",
    "Your viewing history is not a log. It is a confession. A record of every moment you chose to disappear into someone else's world.",
    "The algorithm watches what you watch. But we went deeper — tracing not just the titles, but the hours, the rhythms, the behavioral DNA encoded in your choices.",
    "Somewhere between the opening credits and the final scene, your streaming data became something more interesting: a portrait of how you actually spend your most private hours.",
]

BINGE_NARRATIVES = {
    'high': [
        "When you find a show worth caring about, the concept of 'just one more episode' ceases to exist as a restraint. It becomes a formality you skip entirely.",
        "Your binge profile reads like someone who treats episode limits as a philosophical suggestion rather than a behavioral boundary.",
    ],
    'mid': [
        "You binge with intention — not compulsively, but when something earns it. You understand that commitment has a cost, and you pay it selectively.",
        "Serial consumption is in your behavioral toolkit, but you deploy it deliberately. You choose your obsessions carefully.",
    ],
    'low': [
        "You've resisted the architecture of modern streaming — the autoplay, the cliff-hangers, the engineered urgency. You watch at your own pace, on your own terms.",
        "Your viewing pattern suggests someone with genuine discipline, or a life full enough that no algorithm can fully commandeer your time.",
    ],
}

NIGHT_NARRATIVES = {
    'high': [
        "There is something almost cinematic about watching films and series in the deep hours — the world has stepped back, the light is right, and the story belongs to you entirely.",
        "You've found your theatre in the hours most people have surrendered to sleep. The late-night hours are your private screening room.",
    ],
    'mid': [
        "Evening is your natural viewing territory — after the day's demands, before the night claims you completely.",
        "You've settled into the civilized hours between dinner and sleep as your primary streaming window. Comfortable, intentional, and entirely sustainable.",
    ],
    'low': [
        "You watch while the world is still active — a daylight viewer, a morning consumer, someone who doesn't need the cover of darkness to disappear into a story.",
        "Your viewing rhythms suggest someone who has integrated streaming into the fabric of normal hours rather than treating it as a nocturnal refuge.",
    ],
}

SERIES_NARRATIVES = {
    'high': [
        "Films feel too short to you. Too contained. You want the slow accumulation of seasons — the time to know characters the way you know people.",
        "You invest in narrative universes rather than singular stories. For you, a show isn't something you finish — it's somewhere you live.",
    ],
    'mid': [
        "You navigate fluidly between series and film — knowing which format serves the story you need in a given moment.",
        "Your content portfolio is balanced: the long-game of series alongside the precision of well-crafted films.",
    ],
    'low': [
        "Films are your natural form. You prefer the contained, curated experience — two hours, a complete arc, and then the quiet after.",
        "You gravitate toward self-contained stories. The commitment architecture of multi-season series sits outside your preferred behavioral range.",
    ],
}

CLOSING_FRAMES = [
    "This is not a summary of what you watched. It is a mirror — reflecting not just your taste, but how you move through time.",
    "A year of streaming decisions, collapsed into signal. What you chose, when you chose it, and what it says about the hours you protect most.",
    "The algorithm shows you what Netflix thinks you want. This report shows you something more unsettling: who you actually are when no one is watching.",
    "Every viewing choice is a vote — for a mood, a genre, a time of day. Tallied across a year, they become something that looks uncomfortably like a self-portrait.",
]


# ─────────────────────────────────────────────
# MAIN NARRATIVE GENERATOR
# ─────────────────────────────────────────────

def generate_narrative_report(metrics: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate a complete cinematic narrative report from behavioral metrics.
    Returns dict with multiple narrative sections.
    """
    bq = metrics.get('binge_quotient', 0)
    no = metrics.get('night_owl_index', 0)
    sl = metrics.get('series_loyalty', 0)
    wd = metrics.get('weekend_dominance', 0)
    cs = metrics.get('consistency_score', 50)
    en = metrics.get('content_diversity_pct', 50)
    arch = metrics.get('archetype', {})
    hours = metrics.get('total_hours', 0)
    streak = metrics.get('longest_streak', 0)
    top_show = metrics.get('top_show', '—')
    peak_label = metrics.get('peak_hour_label', '9PM')
    circadian = metrics.get('circadian_label', 'Prime Time Viewer')

    # Select narrative pieces
    opening = random.choice(OPENING_FRAMES)

    binge_tier = 'high' if bq > 55 else ('mid' if bq > 30 else 'low')
    binge_txt  = random.choice(BINGE_NARRATIVES[binge_tier])

    night_tier = 'high' if no > 40 else ('mid' if no > 20 else 'low')
    night_txt  = random.choice(NIGHT_NARRATIVES[night_tier])

    series_tier = 'high' if sl > 70 else ('mid' if sl > 45 else 'low')
    series_txt  = random.choice(SERIES_NARRATIVES[series_tier])

    closing = random.choice(CLOSING_FRAMES)

    # Consistency paragraph
    if cs > 70:
        consistency_txt = f"With a consistency score of {cs}/100, your viewing rhythms have a almost meditative regularity. You show up for your stories with the reliability of a daily practice."
    elif cs > 45:
        consistency_txt = f"Your consistency score of {cs}/100 suggests a viewer who maintains a steady relationship with their content — neither obsessive nor casual."
    else:
        consistency_txt = f"At {cs}/100, your consistency score reflects a more fluid relationship with your schedule — streaming when life permits, stepping away when it demands."

    # Diversity paragraph
    if en > 65:
        diversity_txt = f"Your content diversity index scores in the top tier — a Shannon entropy of {metrics.get('shannon_entropy', 0):.1f} indicates someone who actively resists the gravitational pull of the recommendation engine."
    elif en > 40:
        diversity_txt = f"You maintain a healthy breadth of content without being scattered. Your diversity index of {round(en, 0):.0f}% suggests curated range rather than random sampling."
    else:
        diversity_txt = f"Your diversity index reflects deep focus rather than wide exploration. When you find what you love, you return to it with the loyalty of someone who knows exactly what they want."

    # Build headline stats paragraph
    stats_txt = (
        f"{hours:,} hours. "
        f"{metrics.get('total_titles', 0):,} unique titles. "
        f"A {streak}-day streak at peak engagement. "
        f"Your most-watched was {top_show!r}, and your primary viewing window opens at {peak_label}. "
        f"These are not just numbers — they are the coordinates of your behavioral landscape."
    )

    return {
        'opening':     opening,
        'stats':       stats_txt,
        'binge':       binge_txt,
        'night':       night_txt,
        'series':      series_txt,
        'consistency': consistency_txt,
        'diversity':   diversity_txt,
        'closing':     closing,
        'circadian':   f"Circadian classification: {circadian}. Your biological and behavioral viewing clock aligns you with the {metrics.get('dominant_zone', 'evening')} tier — one of five distinct streaming chronotypes in the Netflix behavioral spectrum.",
        'archetype_analysis': _generate_archetype_analysis(arch, metrics),
    }


def _generate_archetype_analysis(arch: Dict, m: Dict) -> str:
    name   = arch.get('name', 'The Viewer')
    traits = arch.get('traits', [])

    openers = [
        f"Our behavioral model processed {m.get('total_sessions', 0):,} individual viewing events to arrive at a single classification:",
        f"Across all the dimensions of your viewing history — time, frequency, content type, session depth — one behavioral pattern emerged with statistical clarity:",
        f"Your feature vector — binge score, consistency, entropy, temporal rhythm — converged on a single archetype:",
    ]

    return (
        f"{random.choice(openers)} **{name}**. "
        f"The three defining traits of this archetype are {', '.join(traits[:2]).lower()}, "
        f"and {traits[2].lower() if len(traits) > 2 else 'behavioral consistency'}. "
        f"This classification places you in the {_percentile_language(m)} of behavioral engagement across the streaming population."
    )


def _percentile_language(m: Dict) -> str:
    score = (
        m.get('binge_quotient', 0) +
        m.get('night_owl_index', 0) +
        m.get('series_loyalty', 0)
    ) / 3

    if score > 65:  return "top 15%"
    if score > 50:  return "top 35%"
    if score > 35:  return "middle tier"
    return "measured, balanced range"


# ─────────────────────────────────────────────
# LINKEDIN SUMMARY GENERATOR
# ─────────────────────────────────────────────

def generate_linkedin_summary(metrics: Dict, narrative: Dict) -> str:
    arch_name  = metrics.get('archetype', {}).get('name', 'Strategic Viewer')
    hours      = metrics.get('total_hours', 0)
    titles     = metrics.get('total_titles', 0)
    top_show   = metrics.get('top_show', 'N/A')
    bq         = metrics.get('binge_quotient', 0)
    streak     = metrics.get('longest_streak', 0)

    return textwrap.dedent(f"""
    🎬 My Netflix Wrapped AI Report — {pd.Timestamp.now().year if __import__('pandas', fromlist=['Timestamp']).Timestamp.now() else ''}

    This year, I streamed {hours:,} hours across {titles} unique titles.

    My streaming archetype: **{arch_name}**
    • Binge Quotient: {bq}/100
    • Longest viewing streak: {streak} days
    • Top title: {top_show}

    Powered by Netflix Wrapped AI — a behavioral intelligence platform that transforms viewing history into behavioral insight.

    #NetflixWrapped #StreamingIntelligence #BehavioralAnalytics
    """).strip()


# Allow import of pandas dynamically to avoid circular imports at module level
try:
    import pandas as pd
except ImportError:
    pass
