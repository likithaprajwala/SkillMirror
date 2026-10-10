"""
app.py  —  SkillMirror  |  Premium Career Analytics Dashboard
──────────────────────────────────────────────────────────────
Dark navy theme · Plotly charts · Inline CSS (Streamlit-safe)
Run:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import csv, io, math
from datetime import datetime

from skill_extractor  import (extract_skills_from_text, parse_user_skills,
                               get_all_predefined_skills, get_suggested_skills)
from skill_matcher    import match_skills, get_score_label
from roadmap          import (generate_roadmap, roadmap_to_report_lines,
                               get_priority_counts, SKILL_METADATA)
from sample_jobs      import get_sample_names, get_sample_description
from roadmap_page     import render_roadmap_page

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillMirror",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS  (single source of truth for every colour)
# ─────────────────────────────────────────────────────────────────────────────
C = {
    "bg":          "#0d1117",   # page background
    "surface":     "#161b27",   # card / panel background
    "surface2":    "#1e2535",   # slightly lighter card
    "border":      "#2a3348",   # subtle border
    "accent":      "#6366f1",   # indigo accent
    "accent2":     "#818cf8",   # lighter indigo
    "green":       "#22c55e",   # matched
    "green_dim":   "#14532d",
    "green_bg":    "#052e16",
    "orange":      "#f59e0b",   # partial / medium
    "orange_dim":  "#78350f",
    "orange_bg":   "#1c1008",
    "red":         "#ef4444",   # missing
    "red_dim":     "#7f1d1d",
    "red_bg":      "#1c0505",
    "blue":        "#3b82f6",   # additional
    "blue_dim":    "#1e3a8a",
    "blue_bg":     "#030d1f",
    "purple":      "#a855f7",   # neutral analytics
    "text":        "#e2e8f0",   # primary text
    "text2":       "#94a3b8",   # secondary text
    "text3":       "#64748b",   # muted text
}

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  — structural Streamlit overrides + reusable utility classes
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Reset & base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}}
.stApp {{
    background-color: {C["bg"]};
    color: {C["text"]};
}}
/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] > div:first-child {{
    background-color: {C["surface"]};
    border-right: 1px solid {C["border"]};
}}
section[data-testid="stSidebar"] * {{ color: {C["text2"]} !important; }}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{ color: {C["accent2"]} !important; }}

/* ── Sidebar inputs ── */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {{
    background-color: {C["surface2"]} !important;
    color: {C["text"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 6px !important;
}}
section[data-testid="stSidebar"] .stSelectbox > div > div {{
    background-color: {C["surface2"]} !important;
    color: {C["text"]} !important;
    border: 1px solid {C["border"]} !important;
}}

/* ── Main area inputs ── */
.stTextArea textarea, .stTextInput input {{
    background-color: {C["surface2"]} !important;
    color: {C["text"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
    border-color: {C["accent"]} !important;
    box-shadow: 0 0 0 2px {C["accent"]}33 !important;
}}

/* ── Selectbox ── */
.stSelectbox > div > div {{
    background-color: {C["surface2"]} !important;
    color: {C["text"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 8px !important;
}}

/* ── Multiselect ── */
.stMultiSelect > div > div {{
    background-color: {C["surface2"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 8px !important;
}}
.stMultiSelect span[data-baseweb="tag"] {{
    background-color: {C["accent"]}33 !important;
    color: {C["accent2"]} !important;
    border: 1px solid {C["accent"]}55 !important;
}}

/* ── Primary button (Analyse) ── */
div[data-testid="stButton"] button[kind="primary"] {{
    background: linear-gradient(135deg, {C["accent"]}, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.4rem !important;
    letter-spacing: 0.02rem !important;
    transition: opacity 0.2s !important;
}}
div[data-testid="stButton"] button[kind="primary"]:hover {{
    opacity: 0.88 !important;
}}

/* ── Secondary button ── */
div[data-testid="stButton"] button[kind="secondary"] {{
    background-color: {C["surface2"]} !important;
    color: {C["text2"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}}
div[data-testid="stButton"] button[kind="secondary"]:hover {{
    border-color: {C["accent"]} !important;
    color: {C["accent2"]} !important;
}}

/* ── Download buttons ── */
div[data-testid="stDownloadButton"] button {{
    background: linear-gradient(135deg, #059669, #047857) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}}

/* ── Tabs ── */
div[data-testid="stTabs"] button {{
    background: transparent !important;
    color: {C["text3"]} !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.88rem !important;
}}
div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {C["accent2"]} !important;
    border-bottom-color: {C["accent"]} !important;
}}
div[data-testid="stTabs"] {{
    background-color: {C["surface"]} !important;
    border-radius: 10px !important;
    border: 1px solid {C["border"]} !important;
    padding: 0 0.5rem !important;
}}

/* ── Expander ── */
details {{
    background-color: {C["surface"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 10px !important;
}}
details summary {{
    color: {C["text2"]} !important;
    font-weight: 600 !important;
    padding: 0.6rem 0.8rem !important;
}}

/* ── Metric widget (st.metric) ── */
div[data-testid="stMetric"] {{
    background: {C["surface"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 10px !important;
    padding: 0.9rem 1rem !important;
}}
div[data-testid="stMetricLabel"] {{ color: {C["text3"]} !important; font-size: 0.8rem !important; }}
div[data-testid="stMetricValue"] {{ color: {C["text"]} !important; font-size: 1.7rem !important; font-weight: 800 !important; }}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div > div > div {{
    background: linear-gradient(90deg, {C["accent"]}, {C["purple"]}) !important;
    border-radius: 4px !important;
}}
div[data-testid="stProgressBar"] > div > div {{
    background-color: {C["surface2"]} !important;
    border-radius: 4px !important;
}}

/* ── Checkbox ── */
label[data-testid="stCheckbox"] {{
    color: {C["text2"]} !important;
}}

/* ── Info / Warning / Success boxes ── */
div[data-testid="stAlert"] {{
    border-radius: 8px !important;
    border: none !important;
    font-size: 0.88rem !important;
}}

/* ── Divider ── */
hr {{ border-color: {C["border"]} !important; margin: 1rem 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {C["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {C["border"]}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "page":            "analyze",   # analyze | dashboard | roadmap | reports
    "analysis_done":   False,
    "student_name":    "",
    "degree":          "",
    "target_role":     "",
    "experience":      "Beginner",
    "student_skills":  [],
    "job_description": "",
    "required_skills": [],
    "analysis":        {},
    "roadmap":         [],
    "checklist":       {},          # {skill: bool}
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─────────────────────────────────────────────────────────────────────────────
# HTML HELPERS  (all inline-styled — never rely on injected class selectors)
# ─────────────────────────────────────────────────────────────────────────────

def _div(content: str, **style) -> str:
    css = "; ".join(f"{k.replace('_','-')}:{v}" for k, v in style.items())
    return f'<div style="{css}">{content}</div>'

def card(content: str, border_color: str = None, padding: str = "1.2rem 1.4rem") -> str:
    bc = border_color or C["border"]
    return (f'<div style="background:{C["surface"]}; border:1px solid {bc}; '
            f'border-radius:12px; padding:{padding}; '
            f'box-shadow:0 2px 12px rgba(0,0,0,0.3);">'
            f'{content}</div>')

def badge(text: str, bg: str, fg: str, border: str) -> str:
    return (f'<span style="display:inline-block; padding:3px 10px; '
            f'border-radius:20px; font-size:0.78rem; font-weight:600; '
            f'background:{bg}; color:{fg}; border:1px solid {border}; '
            f'margin:2px 2px; white-space:nowrap;">{text}</span>')

def badge_row(skills: list, kind: str) -> str:
    palettes = {
        "matched":  (C["green_bg"],  C["green"],  "#166534"),
        "missing":  (C["red_bg"],    C["red"],    "#991b1b"),
        "extra":    (C["blue_bg"],   C["blue"],   "#1e40af"),
        "required": (C["surface2"],  C["accent2"],"#4338ca"),
    }
    bg, fg, border = palettes.get(kind, (C["surface2"], C["text2"], C["border"]))
    if not skills:
        return f'<span style="color:{C["text3"]}; font-style:italic; font-size:0.85rem;">None detected</span>'
    html = f'<div style="display:flex; flex-wrap:wrap; gap:5px; padding:4px 0;">'
    for s in skills:
        html += badge(s, bg, fg, border)
    return html + "</div>"

def kpi_card(label: str, value, sub: str, color: str, icon: str) -> str:
    return f"""
    <div style="background:{C["surface"]}; border:1px solid {C["border"]};
                border-top:3px solid {color}; border-radius:12px;
                padding:1.1rem 1rem; text-align:center;
                box-shadow:0 4px 16px rgba(0,0,0,0.25);">
        <div style="font-size:1.4rem; margin-bottom:4px;">{icon}</div>
        <div style="font-size:1.9rem; font-weight:800; color:{color}; line-height:1.1;">{value}</div>
        <div style="font-size:0.78rem; color:{C["text3"]}; font-weight:600;
                    text-transform:uppercase; letter-spacing:0.05rem; margin-top:4px;">{label}</div>
        <div style="font-size:0.75rem; color:{C["text3"]}; margin-top:2px;">{sub}</div>
    </div>"""

def section_title(text: str, sub: str = "") -> str:
    s = (f'<div style="font-size:0.8rem; color:{C["text3"]}; margin-top:2px;">{sub}</div>'
         if sub else "")
    return f"""
    <div style="margin:1.6rem 0 0.8rem;">
        <div style="font-size:1.1rem; font-weight:800; color:{C["text"]};
                    border-left:3px solid {C["accent"]}; padding-left:10px;">
            {text}
        </div>{s}
    </div>"""

def pill(text: str, bg: str, fg: str) -> str:
    return (f'<span style="background:{bg}; color:{fg}; padding:2px 9px; '
            f'border-radius:20px; font-size:0.72rem; font-weight:700; '
            f'white-space:nowrap;">{text}</span>')

def priority_pill(level: str) -> str:
    m = {"HIGH": (C["red_bg"], C["red"]),
         "MEDIUM": (C["orange_bg"], C["orange"]),
         "LOW": (C["green_bg"], C["green"])}
    bg, fg = m.get(level, (C["surface2"], C["text2"]))
    return pill(level, bg, fg)

def est_hours_pill(level: str) -> str:
    m = {"HIGH": "20-40 hrs", "MEDIUM": "10-20 hrs", "LOW": "5-10 hrs"}
    return pill(m.get(level, "~"), C["surface2"], C["text3"])


# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY CHART FACTORY
# ─────────────────────────────────────────────────────────────────────────────

# Shared chart style values (used individually — NOT spread via ** to avoid
# duplicate-keyword errors when a chart needs to override margin or other keys)
_BG        = "rgba(0,0,0,0)"
_FONT      = dict(family="Inter, Segoe UI, sans-serif", color=C["text2"], size=12)
_MARGIN    = dict(t=36, b=20, l=20, r=20)


def _rgba(hex6: str, alpha: float) -> str:
    """Convert a 6-digit hex colour + alpha float → 'rgba(r,g,b,alpha)'.
    Plotly's fillcolor does not accept 8-digit hex strings."""
    h = hex6.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def chart_donut(matched: int, missing: int, additional: int) -> go.Figure:
    labels = ["Matched", "Missing", "Additional"]
    values = [matched, missing, additional]
    colors = [C["green"], C["red"], C["blue"]]
    total  = matched + missing + additional

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.68,
        marker=dict(colors=colors, line=dict(color=C["bg"], width=3)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value} skills (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=_FONT,
        margin=_MARGIN,
        height=260,
        showlegend=True,
        legend=dict(orientation="h", y=-0.12,
                    font=dict(size=11), bgcolor=_BG),
        annotations=[dict(
            text=f"<b>{matched}/{total}</b><br><span style='font-size:10px'>matched</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=15, color=C["text"]),
            align="center",
        )],
        title=dict(text="Skill Coverage",
                   font=dict(size=13, color=C["text2"]),
                   x=0, xanchor="left", pad=dict(l=4)),
    )
    return fig


def chart_missing_bar(roadmap: list) -> go.Figure:
    fig = go.Figure()
    if not roadmap:
        fig.update_layout(
            paper_bgcolor=_BG, plot_bgcolor=_BG,
            font=_FONT, margin=_MARGIN, height=100)
        return fig

    colour_map   = {"HIGH": C["red"], "MEDIUM": C["orange"], "LOW": C["green"]}
    sorted_items = sorted(roadmap,
                          key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["priority"]])
    skills   = [i["skill"]    for i in sorted_items]
    priority = [i["priority"] for i in sorted_items]
    colors   = [colour_map[p] for p in priority]

    fig.add_trace(go.Bar(
        x=[1] * len(skills),
        y=skills,
        orientation="h",
        marker_color=colors,
        customdata=list(zip(priority, [i["topic"] for i in sorted_items])),
        hovertemplate=(
            "<b>%{y}</b><br>Priority: %{customdata[0]}<br>"
            "Topic: %{customdata[1]}<extra></extra>"
        ),
        width=0.6,
    ))
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=_FONT,
        margin=_MARGIN,
        height=max(180, len(skills) * 28 + 60),
        xaxis=dict(visible=False, range=[0, 1.3]),
        yaxis=dict(showgrid=False, tickfont=dict(size=11), autorange="reversed"),
        title=dict(text="Missing Skills by Priority",
                   font=dict(size=13, color=C["text2"]),
                   x=0, xanchor="left"),
        bargap=0.35,
    )
    for label, col in [("HIGH", C["red"]), ("MEDIUM", C["orange"]), ("LOW", C["green"])]:
        fig.add_annotation(
            x=1.05, y=1.12, xref="paper", yref="paper",
            text=f'<span style="color:{col}">■</span> {label}',
            showarrow=False,
            font=dict(size=10, color=C["text2"]),
            xanchor="left",
        )
    return fig


def chart_radar(matched: list, missing: list, required: list) -> go.Figure:
    """
    Requirements Comparison radar.
    1 = student has the skill, 0 = student does not.
    Capped at 12 skills for readability.
    Labelled as 'Requirements Comparison' — not invented proficiency data.
    """
    display_skills = required[:12]
    fig = go.Figure()
    if not display_skills:
        fig.update_layout(
            paper_bgcolor=_BG, plot_bgcolor=_BG,
            font=_FONT, margin=_MARGIN, height=300)
        return fig

    matched_set = {s.lower() for s in matched}
    have = [1 if s.lower() in matched_set else 0 for s in display_skills]
    need = [1] * len(display_skills)

    # Close the polygon
    cats      = display_skills + [display_skills[0]]
    have_vals = have + [have[0]]
    need_vals = need + [need[0]]

    fig.add_trace(go.Scatterpolar(
        r=need_vals, theta=cats, fill="toself",
        name="Required",
        line=dict(color=C["accent"], width=1.5),
        fillcolor=_rgba(C["accent"], 0.09),
        hovertemplate="<b>%{theta}</b><br>Required<extra></extra>",
    ))
    fig.add_trace(go.Scatterpolar(
        r=have_vals, theta=cats, fill="toself",
        name="You Have",
        line=dict(color=C["green"], width=2),
        fillcolor=_rgba(C["green"], 0.14),
        hovertemplate="<b>%{theta}</b><br>You have this skill<extra></extra>",
    ))
    subtitle = ("<br><sup>Showing top 12 required skills</sup>"
                if len(required) > 12 else "")
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=_FONT,
        margin=_MARGIN,
        height=320,
        polar=dict(
            bgcolor=C["surface"],
            radialaxis=dict(visible=False, range=[0, 1.3]),
            angularaxis=dict(
                tickfont=dict(size=9.5, color=C["text2"]),
                linecolor=C["border"],
                gridcolor=C["border"],
            ),
        ),
        showlegend=True,
        legend=dict(orientation="h", y=-0.08,
                    font=dict(size=11), bgcolor=_BG),
        title=dict(
            text=f"Skills Requirements Comparison{subtitle}",
            font=dict(size=13, color=C["text2"]),
            x=0, xanchor="left",
        ),
    )
    return fig


def chart_score_gauge(score: float, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(suffix="%", font=dict(size=36, color=color)),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1,
                      tickcolor=C["border"],
                      tickfont=dict(color=C["text3"], size=10)),
            bar=dict(color=color, thickness=0.28),
            bgcolor=C["surface2"],
            borderwidth=0,
            steps=[
                dict(range=[0,  40], color=C["red_bg"]),
                dict(range=[40, 70], color=C["orange_bg"]),
                dict(range=[70,100], color=C["green_bg"]),
            ],
            threshold=dict(
                line=dict(color=color, width=3),
                thickness=0.75, value=score,
            ),
        ),
    ))
    # margin is specified here only — NOT via _PLOTLY_BASE spread
    fig.update_layout(
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=_FONT,
        margin=dict(t=20, b=0, l=20, r=20),   # intentionally different from _MARGIN
        height=220,
        title=dict(text="Match Score",
                   font=dict(size=13, color=C["text2"]),
                   x=0.5, xanchor="center"),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# REPORT GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def _txt_report(name, degree, role, exp, req, analysis, roadmap) -> str:
    L = ["="*62,
         "  SkillMirror  |  Job Skill Gap Analysis Report",
         f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
         "="*62, ""]
    if name:   L.append(f"Student     : {name}")
    if degree: L.append(f"Degree      : {degree}")
    if role:   L.append(f"Target Role : {role}")
    L += [f"Experience  : {exp}", "",
          f"Match Score : {analysis.get('score', 0):.1f}%  "
          f"(skill overlap — not a hiring prediction)",
          f"Required    : {analysis.get('total_required',0)}",
          f"Matched     : {len(analysis.get('matched',[]))}",
          f"Missing     : {len(analysis.get('missing',[]))}",
          f"Additional  : {len(analysis.get('additional',[]))}", ""]
    for title, key in [("Required Skills", None), ("Matched Skills","matched"),
                       ("Missing Skills","missing"), ("Additional Skills","additional")]:
        L.append(f"--- {title} ---")
        items = req if key is None else analysis.get(key, [])
        L += ([f"  • {s}" for s in items] if items else ["  (none)"])
        L.append("")
    L.extend(roadmap_to_report_lines(roadmap))
    L += ["", "="*62]
    return "\n".join(L)


def _csv_report(name, degree, role, exp, req, analysis, roadmap) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["SkillMirror Report"])
    w.writerow(["Generated", datetime.now().strftime('%Y-%m-%d %H:%M')])
    w.writerow([])
    w.writerow(["Profile"])
    for k,v in [("Name",name or "N/A"),("Degree",degree or "N/A"),
                ("Role",role or "N/A"),("Experience",exp)]: w.writerow([k,v])
    w.writerow([])
    w.writerow(["Summary"])
    w.writerow(["Match Score (%)", f"{analysis.get('score',0):.1f}"])
    for k,v in [("Required",analysis.get("total_required",0)),
                ("Matched",len(analysis.get("matched",[]))),
                ("Missing",len(analysis.get("missing",[]))),
                ("Additional",len(analysis.get("additional",[])))]: w.writerow([k,v])
    w.writerow([])
    for title, key in [("Required Skills",None),("Matched","matched"),
                       ("Missing","missing"),("Additional","additional")]:
        w.writerow([title])
        for s in (req if key is None else analysis.get(key,[])): w.writerow([s])
        w.writerow([])
    w.writerow(["Learning Roadmap"])
    w.writerow(["Skill","Priority","Est. Hours","Topic","Task","Status"])
    hrs = {"HIGH":"20-40h","MEDIUM":"10-20h","LOW":"5-10h"}
    for i in roadmap:
        w.writerow([i["skill"], i["priority"], hrs.get(i["priority"],""),
                    i["topic"], i["task"],
                    "Done" if i.get("done") else "To Do"])
    return out.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        # Logo / brand
        st.markdown(f"""
        <div style="padding:0.8rem 0 1rem;">
            <div style="font-size:1.5rem; font-weight:900;
                        color:{C['accent2']}; letter-spacing:-0.5px;">
                🪞 SkillMirror
            </div>
            <div style="font-size:0.75rem; color:{C['text3']}; margin-top:2px;">
                Career Analytics Dashboard
            </div>
        </div>""", unsafe_allow_html=True)

        # Navigation
        st.markdown(f'<div style="font-size:0.7rem; font-weight:700; '
                    f'color:{C["text3"]}; letter-spacing:0.08rem; '
                    f'text-transform:uppercase; margin-bottom:6px;">Navigation</div>',
                    unsafe_allow_html=True)

        pages = [
            ("analyze",   "🔍 Analyse Job"),
            ("dashboard", "📊 Dashboard"),
            ("roadmap",   "🗺️  Learning Roadmap"),
            ("reports",   "📥 Reports"),
        ]
        for key, label in pages:
            active = st.session_state.page == key
            bg  = f"{C['accent']}22" if active else "transparent"
            fg  = C["accent2"]       if active else C["text2"]
            lborder = f"3px solid {C['accent']}" if active else f"3px solid transparent"
            st.markdown(
                f'<div onclick="" style="background:{bg}; border-left:{lborder}; '
                f'padding:0.45rem 0.8rem; border-radius:6px; margin-bottom:3px; '
                f'cursor:pointer; font-size:0.88rem; font-weight:600; color:{fg};">'
                f'{label}</div>',
                unsafe_allow_html=True,
            )
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = key
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        # Profile
        st.markdown(f'<div style="font-size:0.7rem; font-weight:700; '
                    f'color:{C["text3"]}; letter-spacing:0.08rem; '
                    f'text-transform:uppercase; margin-bottom:8px;">Profile</div>',
                    unsafe_allow_html=True)

        st.session_state.student_name = st.text_input(
            "Name (optional)", value=st.session_state.student_name,
            placeholder="e.g. Priya Sharma")
        st.session_state.degree = st.text_input(
            "Degree / Branch", value=st.session_state.degree,
            placeholder="e.g. B.Tech CSE")
        st.session_state.target_role = st.text_input(
            "Target Role", value=st.session_state.target_role,
            placeholder="e.g. Python Developer")
        st.session_state.experience = st.selectbox(
            "Experience",
            ["Beginner", "Intermediate", "Advanced"],
            index=["Beginner","Intermediate","Advanced"].index(
                st.session_state.experience))

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.72rem; color:{C["text3"]}; '
                    f'line-height:1.5;">Rule-based matching · No API key · '
                    f'No internet required after install</div>',
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: ANALYSE JOB
# ─────────────────────────────────────────────────────────────────────────────

def page_analyze():
    # ── Page header ──
    st.markdown(f"""
    <div style="background:linear-gradient(120deg,{C['surface']} 0%,#1a1f35 100%);
                border:1px solid {C['border']}; border-radius:14px;
                padding:1.6rem 2rem; margin-bottom:1.2rem;">
        <div style="font-size:1.6rem; font-weight:900; color:{C['text']};
                    letter-spacing:-0.3px;">Analyse a Job Description</div>
        <div style="font-size:0.88rem; color:{C['text3']}; margin-top:6px;">
            Paste a job description, enter your skills, and get an instant
            skill gap analysis with a personalised learning roadmap.
        </div>
    </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1], gap="large")

    # ── Left: JD input ──
    with col_l:
        st.markdown(card(
            f'<div style="font-size:0.92rem; font-weight:700; color:{C["text"]}; '
            f'margin-bottom:10px;">📋 Job Description</div>'
            f'<div style="font-size:0.78rem; color:{C["text3"]};">'
            f'Select a sample or paste your own job description below.</div>',
            padding="1rem 1.2rem"
        ), unsafe_allow_html=True)

        samples = ["— Paste custom job description —"] + get_sample_names()
        sel = st.selectbox("Sample jobs", samples, key="sample_sel",
                           label_visibility="collapsed")
        jd_default = (get_sample_description(sel)
                      if sel != "— Paste custom job description —"
                      else st.session_state.job_description)

        job_desc = st.text_area(
            "Job description text",
            value=jd_default,
            height=300,
            placeholder="Paste the full job description here…",
            key="jd_input",
            label_visibility="collapsed",
        )

    # ── Right: Skills input ──
    with col_r:
        st.markdown(card(
            f'<div style="font-size:0.92rem; font-weight:700; color:{C["text"]}; '
            f'margin-bottom:10px;">🧑‍💻 Your Current Skills</div>'
            f'<div style="font-size:0.78rem; color:{C["text3"]};">'
            f'Enter skills separated by commas, or pick from the list below.</div>',
            padding="1rem 1.2rem"
        ), unsafe_allow_html=True)

        skills_text = st.text_area(
            "Your skills",
            value=", ".join(st.session_state.student_skills),
            height=160,
            placeholder="e.g. Python, SQL, Git, REST APIs, Communication Skills",
            key="skills_input",
            label_visibility="collapsed",
        )

        picked = st.multiselect(
            "Or pick from full skill list",
            options=get_all_predefined_skills(),
            default=[],
            key="skill_picker",
            placeholder="Search and select skills…",
        )

        # Quick suggestion chips
        st.markdown(
            f'<div style="font-size:0.75rem; color:{C["text3"]}; '
            f'margin:8px 0 4px;">Common skills:</div>',
            unsafe_allow_html=True)
        chips_html = '<div style="display:flex; flex-wrap:wrap; gap:4px;">'
        for s in get_suggested_skills()[:16]:
            chips_html += (f'<span style="background:{C["surface2"]}; color:{C["text3"]}; '
                           f'padding:2px 8px; border-radius:12px; font-size:0.73rem; '
                           f'border:1px solid {C["border"]};">{s}</span>')
        chips_html += "</div>"
        st.markdown(chips_html, unsafe_allow_html=True)

    # ── Analyse button ──
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    btn_col, reset_col, info_col = st.columns([1.2, 0.8, 4])

    with btn_col:
        run = st.button("🔍  Analyse Skills", type="primary",
                        use_container_width=True)
    with reset_col:
        if st.button("Reset", use_container_width=True):
            for k in ["analysis_done","student_skills","job_description",
                      "required_skills","analysis","roadmap","checklist"]:
                st.session_state[k] = _DEFAULTS[k]
            st.rerun()
    with info_col:
        st.markdown(
            f'<div style="font-size:0.78rem; color:{C["text3"]}; '
            f'padding-top:0.6rem;">Match Score = (matched ÷ required) × 100. '
            f'Measures skill overlap only — not actual hiring probability.</div>',
            unsafe_allow_html=True)

    if not run:
        # Show empty state only when no analysis exists yet
        if not st.session_state.analysis_done:
            st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
            st.markdown(card(
                f'<div style="text-align:center; padding:2rem 0;">'
                f'<div style="font-size:2.5rem; margin-bottom:12px;">🪞</div>'
                f'<div style="font-size:1rem; font-weight:700; color:{C["text2"]};">'
                f'Ready to analyse</div>'
                f'<div style="font-size:0.85rem; color:{C["text3"]}; margin-top:6px;">'
                f'Fill in your skills and a job description above, '
                f'then click <b style="color:{C["accent2"]};">Analyse Skills</b>.</div>'
                f'</div>'
            ), unsafe_allow_html=True)
        return

    # ── Validation ──
    combined = skills_text + (", " + ", ".join(picked) if picked else "")
    student_skills = parse_user_skills(combined)
    jd = job_desc.strip()

    if not student_skills:
        st.warning("⚠️ Enter at least one skill before analysing.")
        return
    if not jd:
        st.warning("⚠️ Paste a job description or select a sample first.")
        return

    required_skills = extract_skills_from_text(jd)

    # ── Run analysis ──
    analysis = match_skills(student_skills, required_skills)
    roadmap  = generate_roadmap(analysis.get("missing", []),
                                st.session_state.target_role)

    prev = st.session_state.checklist
    st.session_state.checklist = {
        i["skill"]: prev.get(i["skill"], False) for i in roadmap
    }
    st.session_state.student_skills   = student_skills
    st.session_state.job_description  = jd
    st.session_state.required_skills  = required_skills
    st.session_state.analysis         = analysis
    st.session_state.roadmap          = roadmap
    st.session_state.analysis_done    = True
    st.session_state.page             = "dashboard"
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def page_dashboard():
    if not st.session_state.analysis_done:
        _not_analysed_yet()
        return

    analysis   = st.session_state.analysis
    req        = st.session_state.required_skills
    matched    = analysis.get("matched", [])
    missing    = analysis.get("missing", [])
    additional = analysis.get("additional", [])
    score      = analysis.get("score", 0.0)
    info       = get_score_label(score)
    roadmap    = st.session_state.roadmap
    done_count = sum(1 for i in roadmap
                     if st.session_state.checklist.get(i["skill"], False))

    # ── Header ──
    role_text = st.session_state.target_role or "Target Role"
    st.markdown(f"""
    <div style="background:linear-gradient(120deg,{C['surface']} 0%,#1a1f35 100%);
                border:1px solid {C['border']}; border-radius:14px;
                padding:1.4rem 2rem; margin-bottom:1.2rem;
                display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div style="font-size:1.4rem; font-weight:900; color:{C['text']};">
                Skill Gap Dashboard
            </div>
            <div style="font-size:0.85rem; color:{C['text3']}; margin-top:4px;">
                Role: <b style="color:{C['accent2']};">{role_text}</b> &nbsp;·&nbsp;
                {len(req)} required skills detected
            </div>
        </div>
        <div style="background:{info['color']}18; border:1px solid {info['color']}44;
                    border-radius:8px; padding:0.5rem 1rem; text-align:center;">
            <div style="font-size:1.6rem; font-weight:900; color:{info['color']};">{score:.1f}%</div>
            <div style="font-size:0.72rem; color:{C['text3']}; font-weight:600;">{info['label']}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── 4 KPI cards ──
    k1, k2, k3, k4 = st.columns(4, gap="small")
    with k1:
        st.markdown(kpi_card("Match Score", f"{score:.1f}%",
                             "skill overlap", info["color"], "🎯"),
                    unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("Matched", len(matched),
                             f"of {len(req)} required", C["green"], "✅"),
                    unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("Missing", len(missing),
                             "skills to learn", C["red"], "📚"),
                    unsafe_allow_html=True)
    with k4:
        rd_pct = f"{int(done_count/len(roadmap)*100)}%" if roadmap else "—"
        st.markdown(kpi_card("Roadmap", rd_pct,
                             f"{done_count}/{len(roadmap)} done",
                             C["purple"], "🗺️"),
                    unsafe_allow_html=True)

    st.markdown(
        f'<div style="font-size:0.74rem; color:{C["text3"]}; '
        f'margin:6px 0 1rem;">ℹ️ Match Score measures detected skill overlap only. '
        f'It does not predict hiring probability.</div>',
        unsafe_allow_html=True)

    # ── Charts row 1: gauge + donut ──
    st.markdown(section_title("Charts"), unsafe_allow_html=True)
    gc, dc = st.columns([1, 1], gap="large")
    with gc:
        st.markdown(
            f'<div style="background:{C["surface"]}; border:1px solid {C["border"]}; '
            f'border-radius:12px; padding:0.6rem;">',
            unsafe_allow_html=True)
        st.plotly_chart(chart_score_gauge(score, info["color"]),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with dc:
        st.markdown(
            f'<div style="background:{C["surface"]}; border:1px solid {C["border"]}; '
            f'border-radius:12px; padding:0.6rem;">',
            unsafe_allow_html=True)
        st.plotly_chart(chart_donut(len(matched), len(missing), len(additional)),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Charts row 2: radar + missing bar ──
    rc, bc = st.columns([1, 1], gap="large")
    with rc:
        st.markdown(
            f'<div style="background:{C["surface"]}; border:1px solid {C["border"]}; '
            f'border-radius:12px; padding:0.6rem;">',
            unsafe_allow_html=True)
        st.plotly_chart(chart_radar(matched, missing, req),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with bc:
        st.markdown(
            f'<div style="background:{C["surface"]}; border:1px solid {C["border"]}; '
            f'border-radius:12px; padding:0.6rem;">',
            unsafe_allow_html=True)
        st.plotly_chart(chart_missing_bar(roadmap),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Skill comparison tabs ──
    st.markdown(section_title("Skill Breakdown"), unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs([
        f"✅ Matched  ({len(matched)})",
        f"❌ Missing  ({len(missing)})",
        f"➕ Additional  ({len(additional)})",
        f"🔍 All Required  ({len(req)})",
    ])
    with t1:
        st.markdown(
            f'<div style="background:{C["green_bg"]}; border:1px solid {C["green_dim"]}; '
            f'border-radius:10px; padding:1rem; min-height:60px;">'
            + badge_row(matched, "matched") +
            f'<div style="font-size:0.75rem; color:{C["text3"]}; margin-top:8px;">'
            f'{len(matched)} of your skills match the job requirements.</div>'
            f'</div>', unsafe_allow_html=True)
        if not matched:
            st.info("None of your entered skills matched the detected requirements.")

    with t2:
        st.markdown(
            f'<div style="background:{C["red_bg"]}; border:1px solid {C["red_dim"]}; '
            f'border-radius:10px; padding:1rem; min-height:60px;">'
            + badge_row(missing, "missing") +
            f'<div style="font-size:0.75rem; color:{C["text3"]}; margin-top:8px;">'
            f'These are in the job description but not in your skill list.</div>'
            f'</div>', unsafe_allow_html=True)
        if not missing:
            st.success("You have all the required skills for this role!")

    with t3:
        st.markdown(
            f'<div style="background:{C["blue_bg"]}; border:1px solid {C["blue_dim"]}; '
            f'border-radius:10px; padding:1rem; min-height:60px;">'
            + badge_row(additional, "extra") +
            f'<div style="font-size:0.75rem; color:{C["text3"]}; margin-top:8px;">'
            f'Skills you have that were not listed in this job description.</div>'
            f'</div>', unsafe_allow_html=True)

    with t4:
        st.markdown(
            f'<div style="background:{C["surface2"]}; border:1px solid {C["border"]}; '
            f'border-radius:10px; padding:1rem; min-height:60px;">'
            + badge_row(req, "required") +
            f'<div style="font-size:0.75rem; color:{C["text3"]}; margin-top:8px;">'
            f'{len(req)} skills detected in the job description.</div>'
            f'</div>', unsafe_allow_html=True)
        if not req:
            st.info("No recognisable skills were detected in the job description.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LEARNING ROADMAP  (delegated to roadmap_page.py)
# ─────────────────────────────────────────────────────────────────────────────

def page_roadmap():
    render_roadmap_page()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: REPORTS
# ─────────────────────────────────────────────────────────────────────────────

def page_reports():
    if not st.session_state.analysis_done:
        _not_analysed_yet()
        return

    analysis = st.session_state.analysis
    roadmap  = st.session_state.roadmap
    for item in roadmap:
        item["done"] = st.session_state.checklist.get(item["skill"], False)

    name = st.session_state.student_name
    deg  = st.session_state.degree
    role = st.session_state.target_role
    exp  = st.session_state.experience
    req  = st.session_state.required_skills
    ts   = datetime.now().strftime('%Y%m%d_%H%M')

    st.markdown(f"""
    <div style="background:linear-gradient(120deg,{C['surface']} 0%,#1a1f35 100%);
                border:1px solid {C['border']}; border-radius:14px;
                padding:1.4rem 2rem; margin-bottom:1.2rem;">
        <div style="font-size:1.4rem; font-weight:900; color:{C['text']};">Download Reports</div>
        <div style="font-size:0.85rem; color:{C['text3']}; margin-top:4px;">
            Export your full skill gap analysis and learning roadmap.
        </div>
    </div>""", unsafe_allow_html=True)

    # Summary card
    score = analysis.get("score", 0)
    info  = get_score_label(score)
    st.markdown(card(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:1rem; text-align:center;">
        <div>
            <div style="font-size:1.6rem; font-weight:800; color:{info['color']};">{score:.1f}%</div>
            <div style="font-size:0.75rem; color:{C['text3']};">Match Score</div>
        </div>
        <div>
            <div style="font-size:1.6rem; font-weight:800; color:{C['green']};">{len(analysis.get('matched',[]))}</div>
            <div style="font-size:0.75rem; color:{C['text3']};">Matched</div>
        </div>
        <div>
            <div style="font-size:1.6rem; font-weight:800; color:{C['red']};">{len(analysis.get('missing',[]))}</div>
            <div style="font-size:0.75rem; color:{C['text3']};">Missing</div>
        </div>
        <div>
            <div style="font-size:1.6rem; font-weight:800; color:{C['purple']};">{len(roadmap)}</div>
            <div style="font-size:0.75rem; color:{C['text3']};">Roadmap Items</div>
        </div>
    </div>"""), unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown(card(f"""
        <div style="font-size:0.92rem; font-weight:700; color:{C['text']}; margin-bottom:6px;">
            📄 TXT Report
        </div>
        <div style="font-size:0.8rem; color:{C['text3']}; margin-bottom:12px;">
            Plain text format · Full analysis + roadmap · Easy to read and share
        </div>""", padding="1rem 1.2rem"), unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download TXT",
            data=_txt_report(name, deg, role, exp, req, analysis, roadmap),
            file_name=f"skillmirror_{ts}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        st.markdown(card(f"""
        <div style="font-size:0.92rem; font-weight:700; color:{C['text']}; margin-bottom:6px;">
            📊 CSV Report
        </div>
        <div style="font-size:0.8rem; color:{C['text3']}; margin-bottom:12px;">
            Spreadsheet format · Skills table + roadmap · Open in Excel or Sheets
        </div>""", padding="1rem 1.2rem"), unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download CSV",
            data=_csv_report(name, deg, role, exp, req, analysis, roadmap),
            file_name=f"skillmirror_{ts}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Report preview
    st.markdown(section_title("Report Preview"), unsafe_allow_html=True)
    with st.expander("Click to preview the TXT report", expanded=False):
        preview = _txt_report(name, deg, role, exp, req, analysis, roadmap)
        st.code(preview, language=None)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — empty state when analysis not yet run
# ─────────────────────────────────────────────────────────────────────────────

def _not_analysed_yet():
    st.markdown(card(f"""
    <div style="text-align:center; padding:2.5rem 1rem;">
        <div style="font-size:3rem; margin-bottom:1rem;">🪞</div>
        <div style="font-size:1.1rem; font-weight:700; color:{C['text2']};">
            No analysis yet
        </div>
        <div style="font-size:0.88rem; color:{C['text3']}; margin-top:8px;">
            Go to <b style="color:{C['accent2']};">Analyse Job</b>, enter your skills
            and a job description, then click <b style="color:{C['accent2']};">Analyse Skills</b>.
        </div>
    </div>"""), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    render_sidebar()

    page = st.session_state.page
    if   page == "analyze":   page_analyze()
    elif page == "dashboard": page_dashboard()
    elif page == "roadmap":   page_roadmap()
    elif page == "reports":   page_reports()
    else:
        st.session_state.page = "analyze"
        st.rerun()

    # Footer
    st.markdown(f"""
    <div style="text-align:center; color:{C['text3']}; font-size:0.72rem;
                margin-top:3rem; padding:1rem;
                border-top:1px solid {C['border']};">
        🪞 <b>SkillMirror</b> &nbsp;·&nbsp; Built with Python &amp; Streamlit
        &nbsp;·&nbsp; Rule-based matching — no API key required
        &nbsp;·&nbsp; For educational and career exploration purposes only.
    </div>""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
