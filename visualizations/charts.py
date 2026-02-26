"""
Netflix Wrapped AI — Chart Library
All Plotly visualizations with cinematic dark theming.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import calendar
from typing import Dict, List, Optional


# ─────────────────────────────────────────────
# SHARED PLOTLY LAYOUT
# ─────────────────────────────────────────────

def _base_layout(**overrides) -> dict:
    layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#E6E6E6', size=12),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.07)',
            tickfont=dict(color='rgba(255,255,255,0.38)', size=11),
            title_font=dict(color='rgba(255,255,255,0.3)', size=11),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.07)',
            tickfont=dict(color='rgba(255,255,255,0.38)', size=11),
            title_font=dict(color='rgba(255,255,255,0.3)', size=11),
            zeroline=False,
        ),
        margin=dict(l=12, r=12, t=20, b=12),
        showlegend=False,
        hoverlabel=dict(
            bgcolor='#1a1a1a',
            bordercolor='rgba(229,9,20,0.35)',
            font=dict(family='DM Mono', color='#E6E6E6', size=12),
        ),
        transition=dict(duration=600, easing='cubic-in-out'),
    )
    layout.update(overrides)
    return layout


RED       = 'rgba(229,9,20,0.92)'
RED_SOFT  = 'rgba(229,9,20,0.25)'
GRAY_BAR  = 'rgba(255,255,255,0.10)'
GRAY_MED  = 'rgba(255,255,255,0.16)'


# ─────────────────────────────────────────────
# MONTHLY INTENSITY
# ─────────────────────────────────────────────

def monthly_chart(monthly_df: pd.DataFrame) -> go.Figure:
    all_months = list(range(1, 13))
    labels     = [calendar.month_abbr[m] for m in all_months]

    merged = pd.DataFrame({'month': all_months}).merge(monthly_df, on='month', how='left').fillna(0)
    vals   = merged['count'].tolist()
    max_i  = int(np.argmax(vals))
    colors = [RED if i == max_i else GRAY_BAR for i in range(12)]

    fig = go.Figure()
    # Ghost area fill
    fig.add_trace(go.Scatter(
        x=labels, y=vals, fill='tozeroy',
        fillcolor='rgba(229,9,20,0.04)',
        line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip',
    ))
    # Bars
    fig.add_trace(go.Bar(
        x=labels, y=vals, marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>%{y} titles<extra></extra>',
    ))

    fig.update_layout(**_base_layout(height=300, bargap=0.28))
    return fig


# ─────────────────────────────────────────────
# HOURLY SIGNATURE
# ─────────────────────────────────────────────

def hourly_chart(hourly_df: pd.DataFrame) -> go.Figure:
    all_hours = list(range(24))
    merged    = pd.DataFrame({'hour': all_hours}).merge(hourly_df, on='hour', how='left').fillna(0)
    vals      = merged['count'].tolist()
    max_i     = int(np.argmax(vals))

    colors = []
    for i, v in enumerate(vals):
        if i == max_i:              colors.append(RED)
        elif i >= 22 or i <= 2:     colors.append('rgba(229,9,20,0.30)')
        elif 17 <= i < 22:          colors.append(GRAY_MED)
        else:                       colors.append(GRAY_BAR)

    labels = [f"{h:02d}:00" for h in all_hours]

    fig = go.Figure(go.Bar(
        x=labels, y=vals,
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>%{y} titles<extra></extra>',
    ))
    fig.update_layout(**_base_layout(height=280, bargap=0.14))
    return fig


# ─────────────────────────────────────────────
# WEEKDAY RHYTHM
# ─────────────────────────────────────────────

def weekday_chart(weekday_df: pd.DataFrame) -> go.Figure:
    days   = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    merged = (pd.DataFrame({'weekday': range(7), 'day_name': days})
               .merge(weekday_df, on='weekday', how='left').fillna(0))
    vals   = merged['count'].tolist()
    max_i  = int(np.argmax(vals))

    colors = []
    for i in range(7):
        if i == max_i:      colors.append(RED)
        elif i in [5, 6]:   colors.append(GRAY_MED)
        else:               colors.append(GRAY_BAR)

    fig = go.Figure(go.Bar(
        x=days, y=vals,
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>%{y} titles<extra></extra>',
    ))
    fig.update_layout(**_base_layout(height=280, bargap=0.35))
    return fig


# ─────────────────────────────────────────────
# HEAT MAP (weekday × hour)
# ─────────────────────────────────────────────

def heatmap_chart(heatmap_df: pd.DataFrame) -> go.Figure:
    days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    mat  = np.zeros((7, 24))
    for _, row in heatmap_df.iterrows():
        mat[int(row['weekday'])][int(row['hour'])] = row['count']

    colorscale = [
        [0.00, 'rgba(10,10,10,1)'],
        [0.20, 'rgba(55,5,5,1)'],
        [0.50, 'rgba(140,7,10,1)'],
        [0.80, 'rgba(200,8,15,1)'],
        [1.00, 'rgba(229,9,20,1)'],
    ]

    fig = go.Figure(go.Heatmap(
        z=mat, x=[f"{h:02d}" for h in range(24)], y=days,
        colorscale=colorscale, showscale=False,
        hovertemplate='<b>%{y} %{x}:00</b><br>%{z:.0f} titles<extra></extra>',
        xgap=2, ygap=2,
    ))
    fig.update_layout(**_base_layout(height=240, xaxis=dict(
        gridcolor='rgba(0,0,0,0)', linecolor='rgba(0,0,0,0)',
        tickfont=dict(color='rgba(255,255,255,0.3)', size=10),
        title=dict(text='Hour of Day', font=dict(color='rgba(255,255,255,0.25)', size=10)),
        zeroline=False,
    )))
    return fig


# ─────────────────────────────────────────────
# TOP SHOWS (horizontal bar)
# ─────────────────────────────────────────────

def top_shows_chart(df: pd.DataFrame) -> go.Figure:
    d    = df.sort_values('count').copy()
    max_ = d['count'].max()
    colors = [RED if v == max_ else GRAY_BAR for v in d['count']]

    fig = go.Figure(go.Bar(
        y=d['show'], x=d['count'], orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='<b>%{y}</b><br>%{x} sessions<extra></extra>',
    ))
    layout = _base_layout(height=320, bargap=0.38, margin=dict(l=8, r=20, t=16, b=16))
    layout['yaxis']['tickfont'] = dict(color='rgba(255,255,255,0.55)', size=12)
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# DNA RADAR CHART
# ─────────────────────────────────────────────

def radar_chart(feature_vector: Dict) -> go.Figure:
    labels = [
        'Binge Power', 'Weekend Focus', 'Night Activity',
        'Series Loyalty', 'Consistency', 'Content Diversity',
        'Recency', 'Avg Intensity'
    ]
    fv = feature_vector
    values = [
        fv.get('binge_score', 0) * 100,
        fv.get('weekend_ratio', 0) * 100,
        fv.get('night_ratio', 0) * 100,
        fv.get('series_loyalty', 0) * 100,
        fv.get('consistency_score', 0) * 100,
        fv.get('entropy_score', 0) * 100,
        fv.get('recency_score', 0) * 100,
        fv.get('avg_session_hours', 0) * 100,
    ]
    values_closed = values + [values[0]]
    labels_closed  = labels + [labels[0]]

    fig = go.Figure()

    # Background ring
    fig.add_trace(go.Scatterpolar(
        r=[100] * (len(labels) + 1), theta=labels_closed,
        fill='toself', fillcolor='rgba(255,255,255,0.02)',
        line=dict(color='rgba(255,255,255,0.06)', width=1),
        showlegend=False, hoverinfo='skip',
    ))

    # Inner rings
    for level in [25, 50, 75]:
        fig.add_trace(go.Scatterpolar(
            r=[level] * (len(labels) + 1), theta=labels_closed,
            fill=None,
            line=dict(color='rgba(255,255,255,0.04)', width=1),
            showlegend=False, hoverinfo='skip',
        ))

    # User's vector
    fig.add_trace(go.Scatterpolar(
        r=values_closed, theta=labels_closed,
        fill='toself',
        fillcolor='rgba(229,9,20,0.12)',
        line=dict(color='rgba(229,9,20,0.8)', width=2),
        marker=dict(size=6, color='rgba(229,9,20,0.9)', line=dict(width=1, color='rgba(229,9,20,0.5)')),
        hovertemplate='<b>%{theta}</b><br>%{r:.0f}/100<extra></extra>',
        showlegend=False,
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.05)',
                tickfont=dict(color='rgba(255,255,255,0.2)', size=9),
                tickvals=[25, 50, 75, 100],
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.08)',
                tickfont=dict(color='rgba(255,255,255,0.55)', size=11),
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#E6E6E6'),
        margin=dict(l=60, r=60, t=40, b=40),
        height=440,
        showlegend=False,
        hoverlabel=dict(
            bgcolor='#1a1a1a',
            bordercolor='rgba(229,9,20,0.35)',
            font=dict(family='DM Mono', color='#E6E6E6', size=12),
        ),
    )
    return fig


# ─────────────────────────────────────────────
# DAILY MOMENTUM (rolling 7d)
# ─────────────────────────────────────────────

def momentum_chart(daily_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    # Raw bars
    fig.add_trace(go.Bar(
        x=daily_df['date'], y=daily_df['count'],
        marker=dict(color='rgba(255,255,255,0.07)', line=dict(width=0)),
        showlegend=False, hoverinfo='skip',
    ))

    # 7-day rolling line
    fig.add_trace(go.Scatter(
        x=daily_df['date'], y=daily_df['rolling_7d'],
        line=dict(color='rgba(229,9,20,0.85)', width=2.5),
        fill='tozeroy', fillcolor='rgba(229,9,20,0.05)',
        hovertemplate='<b>%{x|%b %d}</b><br>7-day avg: %{y:.1f}<extra></extra>',
        showlegend=False,
    ))

    layout = _base_layout(height=240)
    layout['xaxis']['tickformat'] = '%b %Y'
    layout['xaxis']['dtick'] = 'M1'
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# CLUSTER SCATTER
# ─────────────────────────────────────────────

def cluster_scatter(scatter_df: pd.DataFrame, profiles: Dict) -> go.Figure:
    fig = go.Figure()

    colors_map = [
        'rgba(229,9,20,0.7)',
        'rgba(255,255,255,0.55)',
        'rgba(229,9,20,0.4)',
        'rgba(255,255,255,0.35)',
    ]

    for i, profile in profiles.items():
        mask = scatter_df['cluster'] == i
        subset = scatter_df[mask]
        color  = colors_map[i % len(colors_map)]

        fig.add_trace(go.Scatter(
            x=subset['pca_x'], y=subset['pca_y'],
            mode='markers',
            marker=dict(size=4, color=color, opacity=0.7, line=dict(width=0)),
            name=profile['name'],
            hovertemplate=f'<b>{profile["name"]}</b><br>({profile["pct"]}% of sessions)<extra></extra>',
        ))

        # Centroid label
        fig.add_trace(go.Scatter(
            x=[profile['pca_x_mean']], y=[profile['pca_y_mean']],
            mode='text',
            text=[profile['name'].split()[0]],
            textfont=dict(color='rgba(255,255,255,0.4)', size=10, family='DM Mono'),
            showlegend=False, hoverinfo='skip',
        ))

    layout = _base_layout(height=380, showlegend=False)
    layout['xaxis']['showticklabels'] = False
    layout['yaxis']['showticklabels'] = False
    layout['xaxis']['gridcolor'] = 'rgba(0,0,0,0)'
    layout['yaxis']['gridcolor'] = 'rgba(0,0,0,0)'
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
# YOY COMPARISON BAR
# ─────────────────────────────────────────────

def yoy_chart(yoy_df: pd.DataFrame) -> go.Figure:
    max_h = yoy_df['hours'].max()
    colors = [RED if h == max_h else GRAY_BAR for h in yoy_df['hours']]

    fig = go.Figure(go.Bar(
        x=yoy_df['year'].astype(str), y=yoy_df['hours'].round(0),
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>%{y:.0f} hours<extra></extra>',
        text=yoy_df['hours'].round(0).astype(int),
        textfont=dict(color='rgba(255,255,255,0.5)', family='Bebas Neue', size=20),
        textposition='outside',
    ))
    fig.update_layout(**_base_layout(height=280, bargap=0.45))
    return fig


# ─────────────────────────────────────────────
# GENRE PIE (donut)
# ─────────────────────────────────────────────

def genre_chart(genre_df: pd.DataFrame) -> go.Figure:
    n = len(genre_df)
    reds   = [f'rgba(229,9,20,{0.9 - i*(0.7/max(1,n-1)):.2f})' for i in range(n)]
    whites = [f'rgba(255,255,255,{0.15 + i*(0.3/max(1,n-1)):.2f})' for i in range(n)]
    colors = [reds[i] if i == 0 else whites[i] for i in range(n)]

    fig = go.Figure(go.Pie(
        labels=genre_df['genre'], values=genre_df['count'],
        hole=0.65,
        marker=dict(colors=colors, line=dict(width=2, color='rgba(8,8,8,1)')),
        textinfo='label+percent',
        textfont=dict(size=11, color='rgba(255,255,255,0.6)', family='DM Mono'),
        hovertemplate='<b>%{label}</b><br>%{value} titles<br>%{percent}<extra></extra>',
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#E6E6E6'),
        margin=dict(l=16, r=16, t=16, b=16),
        height=340, showlegend=False,
        hoverlabel=dict(bgcolor='#1a1a1a', bordercolor='rgba(229,9,20,0.3)',
                        font=dict(family='DM Mono', color='#E6E6E6', size=12)),
    )
    return fig
