"""
roadmap_page.py  —  SkillMirror
────────────────────────────────────────────────────────────────────────────
Futuristic Career Exploration & Learning Roadmap page.

Rendered inside app.py when the user navigates to "Learning Roadmap".
Uses:
  • st.components.v1.html  — interactive D3-style SVG career graph (pure JS)
  • Plotly                 — skill analysis bar chart
  • Inline CSS             — glassmorphism panels, neon theme
  • Streamlit session state — checklist persistence

All data is derived from the actual analysis stored in session state.
No fake or hard-coded analytics are shown to the user.
"""

import json
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from roadmap import get_priority_counts

# ── Neon colour palette (mirrors C dict in app.py for consistency) ──────────
NC = {
    "bg":       "#080c14",
    "surface":  "#0d1520",
    "glass":    "rgba(13,21,32,0.82)",
    "border":   "#1a2a3f",
    "cyan":     "#00d4ff",
    "blue":     "#3b82f6",
    "violet":   "#8b5cf6",
    "magenta":  "#e879f9",
    "amber":    "#f59e0b",
    "green":    "#10b981",
    "red":      "#f43f5e",
    "text":     "#e2e8f0",
    "text2":    "#7090b0",
    "text3":    "#3a5070",
}


# ────────────────────────────────────────────────────────────────────────────
# CAREER GRAPH  —  pure HTML/CSS/JS embedded via st.components
# ────────────────────────────────────────────────────────────────────────────

def _build_career_graph_html(matched: list, missing: list,
                              target_role: str) -> str:
    """
    Builds a self-contained HTML page with an SVG career-path graph.
    Nodes are colour-coded by career branch and by skill status.
    Supports pan, zoom, hover tooltips, and click-to-highlight.
    """

    # Career tree data — three branches with skill tags
    career_tree = [
        {
            "id": "root",
            "label": target_role or "Your Profile",
            "icon": "◈",
            "branch": "root",
            "color": NC["cyan"],
            "glow": NC["cyan"],
            "skills": matched[:6],
            "x": 500, "y": 300,
            "desc": "Your current starting point",
        },
        # ── Software Engineering branch ──────────────────────────────────
        {
            "id": "se",
            "label": "Software\nEngineering",
            "icon": "⬡",
            "branch": "se",
            "color": NC["cyan"],
            "glow": NC["cyan"],
            "parent": "root",
            "skills": ["Python", "JavaScript", "Git", "REST APIs", "Docker"],
            "x": 220, "y": 160,
            "desc": "Core software development path",
        },
        {
            "id": "fe",
            "label": "Frontend\nDeveloper",
            "icon": "◇",
            "branch": "se",
            "color": NC["blue"],
            "glow": NC["blue"],
            "parent": "se",
            "skills": ["React", "HTML", "CSS", "TypeScript", "Vue.js"],
            "x": 80,  "y": 60,
            "desc": "Build user interfaces and web apps",
        },
        {
            "id": "be",
            "label": "Backend\nDeveloper",
            "icon": "◇",
            "branch": "se",
            "color": NC["blue"],
            "glow": NC["blue"],
            "parent": "se",
            "skills": ["Python", "Django", "Flask", "SQL", "PostgreSQL"],
            "x": 200, "y": 50,
            "desc": "APIs, databases, and server logic",
        },
        {
            "id": "fs",
            "label": "Full Stack\nDeveloper",
            "icon": "◇",
            "branch": "se",
            "color": NC["blue"],
            "glow": NC["blue"],
            "parent": "se",
            "skills": ["React", "Node.js", "SQL", "Docker", "AWS"],
            "x": 320, "y": 60,
            "desc": "End-to-end web application development",
        },
        {
            "id": "devops",
            "label": "DevOps\nEngineer",
            "icon": "◇",
            "branch": "se",
            "color": NC["blue"],
            "glow": NC["blue"],
            "parent": "se",
            "skills": ["Docker", "Kubernetes", "CI/CD", "AWS", "Linux"],
            "x": 100, "y": 260,
            "desc": "Infrastructure, automation, and deployment",
        },
        # ── AI / Data Science branch ─────────────────────────────────────
        {
            "id": "ai",
            "label": "AI &\nData Science",
            "icon": "⬡",
            "branch": "ai",
            "color": NC["violet"],
            "glow": NC["violet"],
            "parent": "root",
            "skills": ["Python", "Machine Learning", "Pandas", "NumPy", "Statistics"],
            "x": 780, "y": 160,
            "desc": "Artificial intelligence and data science path",
        },
        {
            "id": "mle",
            "label": "ML\nEngineer",
            "icon": "◇",
            "branch": "ai",
            "color": NC["magenta"],
            "glow": NC["magenta"],
            "parent": "ai",
            "skills": ["Scikit-learn", "TensorFlow", "PyTorch", "MLOps", "Docker"],
            "x": 680, "y": 50,
            "desc": "Build and deploy machine learning systems",
        },
        {
            "id": "ds",
            "label": "Data\nScientist",
            "icon": "◇",
            "branch": "ai",
            "color": NC["magenta"],
            "glow": NC["magenta"],
            "parent": "ai",
            "skills": ["Statistics", "Pandas", "Matplotlib", "Jupyter Notebook", "SQL"],
            "x": 820, "y": 50,
            "desc": "Analyse data and derive business insights",
        },
        {
            "id": "nlp",
            "label": "NLP\nSpecialist",
            "icon": "◇",
            "branch": "ai",
            "color": NC["magenta"],
            "glow": NC["magenta"],
            "parent": "ai",
            "skills": ["Natural Language Processing", "PyTorch", "TensorFlow", "Python"],
            "x": 940, "y": 60,
            "desc": "Language models and text intelligence",
        },
        {
            "id": "cv",
            "label": "Computer\nVision",
            "icon": "◇",
            "branch": "ai",
            "color": NC["magenta"],
            "glow": NC["magenta"],
            "parent": "ai",
            "skills": ["Computer Vision", "PyTorch", "TensorFlow", "Python"],
            "x": 900, "y": 260,
            "desc": "Image recognition and visual AI systems",
        },
        # ── Product Management branch ─────────────────────────────────────
        {
            "id": "pm",
            "label": "Product\nManagement",
            "icon": "⬡",
            "branch": "pm",
            "color": NC["amber"],
            "glow": NC["amber"],
            "parent": "root",
            "skills": ["Communication Skills", "Agile", "Problem Solving", "Leadership"],
            "x": 500, "y": 490,
            "desc": "Product strategy and delivery path",
        },
        {
            "id": "apm",
            "label": "Associate\nPM",
            "icon": "◇",
            "branch": "pm",
            "color": "#fb923c",
            "glow": "#fb923c",
            "parent": "pm",
            "skills": ["Agile", "Communication Skills", "Problem Solving"],
            "x": 320, "y": 560,
            "desc": "Entry-level product management",
        },
        {
            "id": "tpm",
            "label": "Technical\nPM",
            "icon": "◇",
            "branch": "pm",
            "color": "#fb923c",
            "glow": "#fb923c",
            "parent": "pm",
            "skills": ["System Design", "Agile", "REST APIs", "Problem Solving"],
            "x": 470, "y": 590,
            "desc": "PM with strong technical background",
        },
        {
            "id": "spm",
            "label": "Senior\nPM",
            "icon": "◇",
            "branch": "pm",
            "color": "#fb923c",
            "glow": "#fb923c",
            "parent": "pm",
            "skills": ["Leadership", "Agile", "Communication Skills", "Project Management"],
            "x": 630, "y": 560,
            "desc": "Lead product vision and cross-functional teams",
        },
    ]

    # Compute match status for each node
    matched_lower = {s.lower() for s in matched}
    missing_lower = {s.lower() for s in missing}

    for node in career_tree:
        node_skills = node.get("skills", [])
        m = sum(1 for s in node_skills if s.lower() in matched_lower)
        total = len(node_skills) if node_skills else 1
        node["match_pct"] = int((m / total) * 100)
        node["match_count"] = m
        node["total_skills"] = total

    nodes_json = json.dumps(career_tree)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: {NC['bg']};
    font-family: 'Segoe UI', system-ui, sans-serif;
    overflow: hidden;
    width: 100%; height: 600px;
    position: relative;
  }}

  /* Grid background */
  body::before {{
    content: '';
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }}

  #canvas-wrap {{
    width: 100%; height: 600px;
    cursor: grab;
    position: relative;
  }}
  #canvas-wrap:active {{ cursor: grabbing; }}

  svg {{
    width: 100%; height: 100%;
  }}

  /* Tooltip */
  #tooltip {{
    position: absolute;
    background: rgba(13,21,32,0.96);
    border: 1px solid {NC['cyan']};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 12px;
    color: {NC['text']};
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s;
    max-width: 220px;
    box-shadow: 0 0 20px rgba(0,212,255,0.2);
    z-index: 100;
  }}
  #tooltip.show {{ opacity: 1; }}
  #tooltip .tt-title {{
    font-size: 13px; font-weight: 700; color: {NC['cyan']};
    margin-bottom: 5px;
  }}
  #tooltip .tt-row {{
    display: flex; justify-content: space-between;
    margin-bottom: 3px; color: {NC['text2']};
  }}
  #tooltip .tt-row span {{ color: {NC['text']}; font-weight: 600; }}
  #tooltip .tt-skills {{
    margin-top: 6px; display: flex; flex-wrap: wrap; gap: 3px;
  }}
  #tooltip .tt-skill {{
    background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.25);
    border-radius: 10px; padding: 1px 7px; font-size: 10px; color: {NC['cyan']};
  }}
  #tooltip .tt-skill.has {{
    background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.3);
    color: {NC['green']};
  }}

  /* Controls */
  #controls {{
    position: absolute; bottom: 14px; right: 14px;
    display: flex; gap: 6px;
  }}
  #controls button {{
    background: rgba(13,21,32,0.9);
    border: 1px solid {NC['border']};
    color: {NC['text2']};
    border-radius: 6px; padding: 5px 10px;
    font-size: 11px; cursor: pointer;
    transition: all 0.2s;
  }}
  #controls button:hover {{
    border-color: {NC['cyan']}; color: {NC['cyan']};
    box-shadow: 0 0 8px rgba(0,212,255,0.3);
  }}

  /* Legend */
  #legend {{
    position: absolute; top: 12px; left: 12px;
    background: rgba(13,21,32,0.88);
    border: 1px solid {NC['border']};
    border-radius: 8px; padding: 8px 12px;
    font-size: 10.5px;
  }}
  #legend .leg-row {{
    display: flex; align-items: center; gap: 7px;
    margin-bottom: 4px; color: {NC['text2']};
  }}
  #legend .leg-dot {{
    width: 8px; height: 8px; border-radius: 50%;
  }}
</style>
</head>
<body>
<div id="canvas-wrap">
  <svg id="graph-svg" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- Glow filters -->
      <filter id="glow-cyan" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="glow-violet" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="glow-amber" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="glow-strong" x="-80%" y="-80%" width="260%" height="260%">
        <feGaussianBlur stdDeviation="8" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <!-- Gradients for edges -->
      <linearGradient id="grad-se" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{NC['cyan']}" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="{NC['blue']}" stop-opacity="0.4"/>
      </linearGradient>
      <linearGradient id="grad-ai" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{NC['violet']}" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="{NC['magenta']}" stop-opacity="0.4"/>
      </linearGradient>
      <linearGradient id="grad-pm" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{NC['amber']}" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="#fb923c" stop-opacity="0.4"/>
      </linearGradient>
    </defs>
    <g id="graph-group" transform="translate(0,0) scale(1)">
      <g id="edges-layer"></g>
      <g id="nodes-layer"></g>
    </g>
  </svg>

  <!-- Tooltip -->
  <div id="tooltip">
    <div class="tt-title" id="tt-title"></div>
    <div class="tt-row">Match <span id="tt-pct"></span></div>
    <div class="tt-row">Skills <span id="tt-skills-count"></span></div>
    <div style="font-size:10px;color:{NC['text2']};margin-top:2px;" id="tt-desc"></div>
    <div class="tt-skills" id="tt-skill-tags"></div>
  </div>

  <!-- Legend -->
  <div id="legend">
    <div class="leg-row"><div class="leg-dot" style="background:{NC['cyan']};box-shadow:0 0 5px {NC['cyan']};"></div>Software Engineering</div>
    <div class="leg-row"><div class="leg-dot" style="background:{NC['violet']};box-shadow:0 0 5px {NC['violet']};"></div>AI & Data Science</div>
    <div class="leg-row"><div class="leg-dot" style="background:{NC['amber']};box-shadow:0 0 5px {NC['amber']};"></div>Product Management</div>
    <div class="leg-row" style="margin-top:4px; border-top:1px solid {NC['border']}; padding-top:4px;">
      <div class="leg-dot" style="background:{NC['green']};"></div>Skills matched
    </div>
    <div class="leg-row">
      <div class="leg-dot" style="background:{NC['red']};"></div>Skills needed
    </div>
  </div>

  <!-- Controls -->
  <div id="controls">
    <button onclick="resetView()">⟳ Reset View</button>
    <button onclick="zoomIn()">＋ Zoom</button>
    <button onclick="zoomOut()">－ Zoom</button>
  </div>
</div>

<script>
const NODES = {nodes_json};
const matchedSkills = new Set({json.dumps(list(matched_lower))});

// Build lookup
const nodeMap = {{}};
NODES.forEach(n => nodeMap[n.id] = n);

const svg    = document.getElementById('graph-svg');
const group  = document.getElementById('graph-group');
const edgesL = document.getElementById('edges-layer');
const nodesL = document.getElementById('nodes-layer');
const tooltip= document.getElementById('tooltip');

// ── Viewport / pan / zoom ────────────────────────────────────────────────
let vx=0, vy=0, scale=1;
let dragging=false, lastX=0, lastY=0;
let selectedId = null;

function applyTransform() {{
  group.setAttribute('transform', `translate(${{vx}},${{vy}}) scale(${{scale}})`);
}}

svg.addEventListener('mousedown', e => {{
  if (e.target.closest('.node-group')) return;
  dragging=true; lastX=e.clientX; lastY=e.clientY;
}});
window.addEventListener('mousemove', e => {{
  if (!dragging) return;
  vx += e.clientX - lastX; vy += e.clientY - lastY;
  lastX=e.clientX; lastY=e.clientY;
  applyTransform();
}});
window.addEventListener('mouseup', () => dragging=false);
svg.addEventListener('wheel', e => {{
  e.preventDefault();
  const delta = e.deltaY > 0 ? 0.9 : 1.1;
  scale = Math.min(Math.max(scale * delta, 0.4), 2.5);
  applyTransform();
}}, {{passive:false}});

function resetView() {{ vx=0; vy=0; scale=1; applyTransform(); selectedId=null; renderGraph(); }}
function zoomIn()    {{ scale = Math.min(scale*1.2, 2.5); applyTransform(); }}
function zoomOut()   {{ scale = Math.max(scale*0.8, 0.4); applyTransform(); }}

// ── Determine node colour based on match status ──────────────────────────
function nodeColor(node) {{
  if (node.id === 'root') return '#00d4ff';
  const pct = node.match_pct || 0;
  if (pct >= 60) return '#10b981';
  if (pct >= 30) return '#f59e0b';
  return node.color;
}}

// ── Draw curved edge ─────────────────────────────────────────────────────
function drawEdge(n1, n2) {{
  const x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y;
  const mx=(x1+x2)/2, my=(y1+y2)/2;
  const cx = mx + (y2-y1)*0.25, cy = my - (x2-x1)*0.25;

  const gradMap = {{ se:'grad-se', ai:'grad-ai', pm:'grad-pm', root:'grad-se' }};
  const grad = gradMap[n2.branch] || 'grad-se';
  const isSelected = selectedId && (n1.id===selectedId || n2.id===selectedId ||
    n1.parent===selectedId || n2.parent===selectedId);
  const opacity = isSelected ? 0.9 : 0.35;
  const width   = isSelected ? 2.5 : 1.5;
  const color   = isSelected ? nodeColor(n2) : n2.color;

  const path = document.createElementNS('http://www.w3.org/2000/svg','path');
  path.setAttribute('d', `M${{x1}},${{y1}} Q${{cx}},${{cy}} ${{x2}},${{y2}}`);
  path.setAttribute('fill','none');
  path.setAttribute('stroke', color);
  path.setAttribute('stroke-width', width);
  path.setAttribute('stroke-opacity', opacity);
  if (isSelected) path.setAttribute('filter','url(#glow-cyan)');

  // Animated dash for selected
  if (isSelected) {{
    const len = path.getTotalLength ? 200 : 200;
    path.setAttribute('stroke-dasharray','8 5');
    const anim = document.createElementNS('http://www.w3.org/2000/svg','animateTransform');
    anim.setAttribute('attributeName','stroke-dashoffset');
    // Use animate instead
    const a2 = document.createElementNS('http://www.w3.org/2000/svg','animate');
    a2.setAttribute('attributeName','stroke-dashoffset');
    a2.setAttribute('from','0'); a2.setAttribute('to','-26');
    a2.setAttribute('dur','1s'); a2.setAttribute('repeatCount','indefinite');
    path.appendChild(a2);
  }}
  edgesL.appendChild(path);
}}

// ── Draw node ─────────────────────────────────────────────────────────────
function drawNode(node) {{
  const isRoot   = node.id === 'root';
  const isHub    = ['se','ai','pm'].includes(node.id);
  const isSelected = node.id === selectedId;
  const color    = nodeColor(node);
  const r        = isRoot ? 44 : isHub ? 36 : 28;

  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class','node-group');
  g.setAttribute('transform',`translate(${{node.x}},${{node.y}})`);
  g.style.cursor = 'pointer';

  // Outer glow ring (selected)
  if (isSelected || isRoot) {{
    const outerRing = document.createElementNS('http://www.w3.org/2000/svg','circle');
    outerRing.setAttribute('r', r+10);
    outerRing.setAttribute('fill','none');
    outerRing.setAttribute('stroke', color);
    outerRing.setAttribute('stroke-width','1');
    outerRing.setAttribute('stroke-opacity','0.25');
    outerRing.setAttribute('filter','url(#glow-strong)');
    g.appendChild(outerRing);
  }}

  // Pulse ring on root
  if (isRoot) {{
    const pulse = document.createElementNS('http://www.w3.org/2000/svg','circle');
    pulse.setAttribute('r', r+6);
    pulse.setAttribute('fill','none');
    pulse.setAttribute('stroke', color);
    pulse.setAttribute('stroke-width','1.5');
    pulse.setAttribute('stroke-opacity','0.5');
    const anim = document.createElementNS('http://www.w3.org/2000/svg','animate');
    anim.setAttribute('attributeName','r');
    anim.setAttribute('values',`${{r+6}};${{r+16}};${{r+6}}`);
    anim.setAttribute('dur','3s'); anim.setAttribute('repeatCount','indefinite');
    const anim2 = document.createElementNS('http://www.w3.org/2000/svg','animate');
    anim2.setAttribute('attributeName','stroke-opacity');
    anim2.setAttribute('values','0.5;0;0.5'); anim2.setAttribute('dur','3s');
    anim2.setAttribute('repeatCount','indefinite');
    pulse.appendChild(anim); pulse.appendChild(anim2);
    g.appendChild(pulse);
  }}

  // Background circle
  const bg = document.createElementNS('http://www.w3.org/2000/svg','circle');
  bg.setAttribute('r', r);
  bg.setAttribute('fill', isRoot ? `rgba(0,212,255,0.12)` :
                          isHub  ? `rgba(${{hexToRgb(color)}},0.1)` :
                                   `rgba(${{hexToRgb(color)}},0.08)`);
  bg.setAttribute('stroke', color);
  bg.setAttribute('stroke-width', isRoot ? '2.5' : isHub ? '2' : '1.5');
  bg.setAttribute('filter', isRoot || isSelected ? 'url(#glow-strong)' :
                             isHub ? 'url(#glow-cyan)' : 'none');
  g.appendChild(bg);

  // Icon
  const iconEl = document.createElementNS('http://www.w3.org/2000/svg','text');
  iconEl.setAttribute('text-anchor','middle');
  iconEl.setAttribute('dominant-baseline','middle');
  iconEl.setAttribute('y', isHub || isRoot ? -6 : -5);
  iconEl.setAttribute('font-size', isRoot ? '18' : isHub ? '15' : '12');
  iconEl.setAttribute('fill', color);
  iconEl.textContent = node.icon;
  g.appendChild(iconEl);

  // Match % badge (non-root)
  if (!isRoot && node.match_pct !== undefined) {{
    const badgeText = document.createElementNS('http://www.w3.org/2000/svg','text');
    badgeText.setAttribute('text-anchor','middle');
    badgeText.setAttribute('dominant-baseline','middle');
    badgeText.setAttribute('y', isHub ? 6 : 4);
    badgeText.setAttribute('font-size', isHub ? '9' : '8');
    badgeText.setAttribute('fill', node.match_pct >= 50 ? '#10b981' : '#f59e0b');
    badgeText.setAttribute('font-weight','700');
    badgeText.textContent = node.match_pct + '%';
    g.appendChild(badgeText);
  }}

  // Label lines
  const lines = node.label.split('\\n');
  lines.forEach((line, i) => {{
    const labelEl = document.createElementNS('http://www.w3.org/2000/svg','text');
    labelEl.setAttribute('text-anchor','middle');
    labelEl.setAttribute('dominant-baseline','middle');
    const yOff = r + 12 + i * 13;
    labelEl.setAttribute('y', yOff);
    labelEl.setAttribute('font-size', isRoot ? '11' : isHub ? '10' : '9');
    labelEl.setAttribute('fill', isSelected ? color : '#94a3b8');
    labelEl.setAttribute('font-weight', isRoot || isHub ? '700' : '500');
    labelEl.textContent = line;
    g.appendChild(labelEl);
  }});

  // Hover + click events
  g.addEventListener('mouseenter', e => showTooltip(node, e));
  g.addEventListener('mousemove',  e => moveTooltip(e));
  g.addEventListener('mouseleave', hideTooltip);
  g.addEventListener('click', () => {{
    selectedId = (selectedId === node.id) ? null : node.id;
    renderGraph();
  }});

  nodesL.appendChild(g);
}}

function hexToRgb(hex) {{
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `${{r}},${{g}},${{b}}`;
}}

// ── Tooltip ──────────────────────────────────────────────────────────────
function showTooltip(node, e) {{
  document.getElementById('tt-title').textContent = node.label.replace('\\n',' ');
  document.getElementById('tt-pct').textContent   = node.match_pct + '%';
  document.getElementById('tt-skills-count').textContent =
    node.match_count + ' / ' + node.total_skills + ' matched';
  document.getElementById('tt-desc').textContent  = node.desc || '';

  const tagsEl = document.getElementById('tt-skill-tags');
  tagsEl.innerHTML = '';
  (node.skills||[]).slice(0,6).forEach(s => {{
    const sp = document.createElement('span');
    sp.className = 'tt-skill' + (matchedSkills.has(s.toLowerCase()) ? ' has' : '');
    sp.textContent = s;
    tagsEl.appendChild(sp);
  }});

  tooltip.classList.add('show');
  moveTooltip(e);
}}
function moveTooltip(e) {{
  const wrap = document.getElementById('canvas-wrap');
  const rect = wrap.getBoundingClientRect();
  let x = e.clientX - rect.left + 14;
  let y = e.clientY - rect.top  - 10;
  if (x + 230 > rect.width)  x = e.clientX - rect.left - 240;
  if (y + 160 > rect.height) y = e.clientY - rect.top  - 160;
  tooltip.style.left = x + 'px';
  tooltip.style.top  = y + 'px';
}}
function hideTooltip() {{ tooltip.classList.remove('show'); }}

// ── Render ────────────────────────────────────────────────────────────────
function renderGraph() {{
  edgesL.innerHTML = '';
  nodesL.innerHTML = '';

  // Draw edges first
  NODES.forEach(node => {{
    if (node.parent) {{
      const parent = nodeMap[node.parent];
      if (parent) drawEdge(parent, node);
    }}
  }});

  // Draw nodes on top
  NODES.forEach(node => drawNode(node));
}}

renderGraph();
</script>
</body>
</html>"""


# ────────────────────────────────────────────────────────────────────────────
# SKILL ANALYSIS BAR CHART  (Plotly)
# ────────────────────────────────────────────────────────────────────────────

def _skill_analysis_chart(matched: list, missing: list) -> go.Figure:
    """
    Horizontal bar chart — top skills from matched + missing.
    Matched = green bars, Missing = red bars.
    """
    m_items = [(s, 1, NC["green"])  for s in matched[:5]]
    x_items = [(s, 1, NC["red"])    for s in missing[:5]]
    all_items = m_items + x_items

    if not all_items:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=160, margin=dict(t=8,b=8,l=8,r=8))
        return fig

    labels = [i[0] for i in all_items]
    colors = [i[2] for i in all_items]

    fig = go.Figure(go.Bar(
        y=labels, x=[1]*len(labels),
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=["✓ Matched" if c == NC["green"] else "✗ Missing"
              for c in colors],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=10, color="white"),
        hovertemplate="<b>%{y}</b><extra></extra>",
        width=0.55,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI", color="#7090b0", size=10),
        margin=dict(t=4, b=4, l=4, r=4),
        height=max(160, len(all_items) * 22 + 20),
        xaxis=dict(visible=False, range=[0, 1.4]),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10, color="#94a3b8"),
            autorange="reversed",
        ),
        bargap=0.3,
    )
    return fig


# ────────────────────────────────────────────────────────────────────────────
# CIRCULAR PROGRESS  (SVG inline)
# ────────────────────────────────────────────────────────────────────────────

def _circle_progress(label: str, pct: int, color: str,
                     assessed: bool = True) -> str:
    if not assessed:
        return f"""
        <div style="text-align:center; padding:6px;">
            <svg width="64" height="64" viewBox="0 0 64 64">
                <circle cx="32" cy="32" r="26" fill="none"
                    stroke="{NC['border']}" stroke-width="4"/>
                <text x="32" y="36" text-anchor="middle"
                    font-size="9" fill="{NC['text2']}" font-family="Segoe UI">N/A</text>
            </svg>
            <div style="font-size:10px; color:{NC['text2']}; margin-top:2px;">{label}</div>
        </div>"""

    r = 26
    circumference = 2 * 3.14159 * r
    dash = circumference * pct / 100
    gap  = circumference - dash
    return f"""
    <div style="text-align:center; padding:6px;">
        <svg width="64" height="64" viewBox="0 0 64 64">
            <circle cx="32" cy="32" r="{r}" fill="none"
                stroke="{NC['border']}" stroke-width="4"/>
            <circle cx="32" cy="32" r="{r}" fill="none"
                stroke="{color}" stroke-width="4"
                stroke-dasharray="{dash:.1f} {gap:.1f}"
                stroke-linecap="round"
                transform="rotate(-90 32 32)"
                style="filter:drop-shadow(0 0 4px {color})"/>
            <text x="32" y="36" text-anchor="middle"
                font-size="11" font-weight="700"
                fill="{color}" font-family="Segoe UI">{pct}%</text>
        </svg>
        <div style="font-size:10px; color:{NC['text2']}; margin-top:2px;
                    white-space:nowrap;">{label}</div>
    </div>"""


# ────────────────────────────────────────────────────────────────────────────
# CAREER PATH TIMELINE
# ────────────────────────────────────────────────────────────────────────────

def _career_timeline(score: float, roadmap: list, checklist: dict) -> str:
    done = sum(1 for i in roadmap if checklist.get(i["skill"], False))
    total = len(roadmap)
    pct = int(done / total * 100) if total else 0

    milestones = [
        ("Current Skills",       score >= 1,    score >= 1,  NC["cyan"]),
        ("Core Foundations",     score >= 20,   score >= 20, NC["blue"]),
        ("Intermediate Skills",  score >= 40,   score >= 40, NC["violet"]),
        ("Advanced Skills",      pct >= 50,     pct >= 50,   NC["magenta"]),
        ("Target Role Ready",    pct >= 90,     score >= 80, NC["amber"]),
    ]

    html = '<div style="display:flex; align-items:center; gap:0; width:100%;">'
    for i, (label, active, done_m, color) in enumerate(milestones):
        dot_col  = color if active else NC["border"]
        dot_glow = f"box-shadow:0 0 10px {color};" if active else ""
        txt_col  = color if active else NC["text3"]
        check    = "✓" if done_m else ("●" if active else "○")

        html += f"""
        <div style="display:flex; flex-direction:column; align-items:center;
                    flex:1; position:relative;">
            <div style="width:28px; height:28px; border-radius:50%;
                        background:{'rgba('+','.join(str(int(dot_col[j:j+2],16)) for j in (1,3,5))+',0.15)' if active else NC['surface']};
                        border:2px solid {dot_col}; {dot_glow}
                        display:flex; align-items:center; justify-content:center;
                        font-size:11px; color:{dot_col}; font-weight:700;
                        position:relative; z-index:2;">
                {check}
            </div>
            <div style="font-size:9px; color:{txt_col}; margin-top:5px;
                        text-align:center; line-height:1.3;">{label}</div>
        </div>"""

        # connector line (not after last)
        if i < len(milestones) - 1:
            next_active = milestones[i+1][1]
            line_col = color if (active and next_active) else NC["border"]
            html += f"""<div style="height:2px; flex:0.5; background:{line_col};
                            margin-bottom:22px; opacity:0.6;"></div>"""

    html += "</div>"
    return html


# ────────────────────────────────────────────────────────────────────────────
# ROADMAP CHECKLIST  (skill cards)
# ────────────────────────────────────────────────────────────────────────────

def _render_roadmap_checklist(roadmap: list):
    """Render the interactive checklist cards with futuristic styling."""
    if not roadmap:
        st.markdown(f"""
        <div style="background:rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.2);
                    border-radius:12px; padding:2rem; text-align:center;">
            <div style="font-size:2rem; margin-bottom:8px;">🎯</div>
            <div style="color:{NC['cyan']}; font-weight:700;">All skills matched!</div>
            <div style="color:{NC['text2']}; font-size:0.85rem; margin-top:4px;">
                You already have all required skills for this role.
            </div>
        </div>""", unsafe_allow_html=True)
        return

    border_map = {"HIGH": NC["red"], "MEDIUM": NC["amber"], "LOW": NC["green"]}
    hrs_map    = {"HIGH": "20–40 hrs", "MEDIUM": "10–20 hrs", "LOW": "5–10 hrs"}
    p_bg_map   = {
        "HIGH":   "rgba(244,63,94,0.12)",
        "MEDIUM": "rgba(245,158,11,0.12)",
        "LOW":    "rgba(16,185,129,0.12)",
    }
    current_p = None

    for item in roadmap:
        skill = item["skill"]
        p     = item["priority"]
        bc    = border_map.get(p, NC["cyan"])
        hrs   = hrs_map.get(p, "")
        p_bg  = p_bg_map.get(p, "rgba(0,212,255,0.1)")

        # ── Priority group header ────────────────────────────────────────
        if p != current_p:
            current_p = p
            g_labels = {
                "HIGH":   "High Priority — Start Here",
                "MEDIUM": "Medium Priority",
                "LOW":    "Low Priority — Optional",
            }
            st.markdown(
                f'<div style="font-size:0.7rem; font-weight:800; color:{bc}; '
                f'letter-spacing:0.08rem; text-transform:uppercase; '
                f'margin:1.2rem 0 0.5rem; padding-left:2px; '
                f'border-left:3px solid {bc}; padding-left:8px;">'
                f'{g_labels.get(p, p)}</div>',
                unsafe_allow_html=True,
            )

        # ── Checkbox — Streamlit widget, standalone ──────────────────────
        done = st.session_state.checklist.get(skill, False)
        new_done = st.checkbox(
            f"Mark **{skill}** as completed",
            value=done,
            key=f"fut_rm_{skill}",
        )
        st.session_state.checklist[skill] = new_done

        # ── Card — complete, self-contained HTML block ───────────────────
        op   = "0.42" if new_done else "1"
        td   = "line-through" if new_done else "none"
        glow = f"box-shadow:0 0 14px {bc}18;" if not new_done else ""
        done_html = (
            f'<span style="margin-left:auto; font-size:0.7rem; '
            f'color:{NC["green"]}; font-weight:700; white-space:nowrap;">✓ Completed</span>'
            if new_done else ""
        )

        st.markdown(
            f'<div style="background:rgba(13,21,32,0.85); '
            f'border:1px solid {bc}55; border-left:4px solid {bc}; '
            f'border-radius:10px; padding:0.8rem 1.1rem; '
            f'margin-bottom:10px; margin-top:-8px; '
            f'opacity:{op}; {glow}">'

            f'<div style="display:flex; align-items:center; gap:8px; '
            f'margin-bottom:6px; flex-wrap:wrap;">'
            f'<span style="font-size:0.92rem; font-weight:700; '
            f'color:{NC["text"]}; text-decoration:{td};">{skill}</span>'
            f'<span style="background:{p_bg}; color:{bc}; '
            f'padding:1px 9px; border-radius:4px; '
            f'font-size:0.68rem; font-weight:800;">{p}</span>'
            f'<span style="font-size:0.7rem; color:{NC["text3"]};">⏱ {hrs}</span>'
            f'{done_html}'
            f'</div>'

            f'<div style="font-size:0.79rem; color:{NC["text2"]}; margin-bottom:4px;">'
            f'<span style="color:{NC["cyan"]}; font-weight:600;">Topic</span>'
            f'&nbsp;&nbsp;{item["topic"]}'
            f'</div>'

            f'<div style="font-size:0.79rem; color:{NC["text3"]};">'
            f'<span style="color:{NC["text2"]}; font-weight:600;">Task</span>'
            f'&nbsp;&nbsp;{item["task"]}'
            f'</div>'

            f'</div>',
            unsafe_allow_html=True,
        )


# ────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT  — called from app.py
# ────────────────────────────────────────────────────────────────────────────

def render_roadmap_page():
    """
    Full futuristic Learning Roadmap page.
    Reads all data from st.session_state set by the analysis page.
    """
    if not st.session_state.get("analysis_done", False):
        # ── Not yet analysed ─────────────────────────────────────────────
        st.markdown(f"""
        <div style="background:rgba(0,212,255,0.04); border:1px solid {NC['cyan']}33;
                    border-radius:16px; padding:3rem 2rem; text-align:center;
                    margin-top:2rem;">
            <div style="font-size:3rem; margin-bottom:1rem; filter:drop-shadow(0 0 20px {NC['cyan']});">🪞</div>
            <div style="font-size:1.2rem; font-weight:800; color:{NC['cyan']};">
                No analysis yet
            </div>
            <div style="font-size:0.88rem; color:{NC['text2']}; margin-top:8px;">
                Go to <b style="color:{NC['cyan']};">Analyse Job</b>, enter your skills
                and a job description, then click <b>Analyse Skills</b>.
            </div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Pull data from session state ─────────────────────────────────────
    analysis  = st.session_state.analysis
    matched   = analysis.get("matched",   [])
    missing   = analysis.get("missing",   [])
    additional= analysis.get("additional",[])
    required  = st.session_state.required_skills
    score     = analysis.get("score",     0.0)
    roadmap   = st.session_state.roadmap
    checklist = st.session_state.checklist
    role      = st.session_state.target_role or "Software Engineer"
    name      = st.session_state.student_name or "You"
    total_rm  = len(roadmap)
    done_count= sum(1 for i in roadmap if checklist.get(i["skill"], False))
    rm_pct    = int(done_count / total_rm * 100) if total_rm else 0
    counts    = get_priority_counts(roadmap)

    # ── Page CSS (scoped to this page render) ────────────────────────────
    st.markdown(f"""
    <style>
    .stApp {{ background-color:{NC['bg']} !important; }}
    .rm-glass {{
        background: {NC['glass']};
        border: 1px solid {NC['border']};
        border-radius: 14px;
        backdrop-filter: blur(12px);
        padding: 1rem 1.2rem;
    }}
    .rm-panel-title {{
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08rem;
        color: {NC['text2']};
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .rm-panel-title::before {{
        content: '';
        display: inline-block;
        width: 3px; height: 12px;
        background: {NC['cyan']};
        border-radius: 2px;
        box-shadow: 0 0 6px {NC['cyan']};
    }}
    </style>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # TOP BAR
    # ─────────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:rgba(13,21,32,0.9); border:1px solid {NC['border']};
                border-radius:14px; padding:0.9rem 1.4rem; margin-bottom:1rem;
                display:flex; align-items:center; justify-content:space-between;
                flex-wrap:wrap; gap:10px; backdrop-filter:blur(12px);">
        <div>
            <div style="font-size:0.65rem; color:{NC['cyan']}; font-weight:800;
                        letter-spacing:0.12rem; text-transform:uppercase;">
                Career Exploration &amp; Learning Roadmap
            </div>
            <div style="font-size:1.2rem; font-weight:900; color:{NC['text']};
                        letter-spacing:-0.3px; margin-top:1px;">
                {role}
                <span style="font-size:0.75rem; font-weight:400; color:{NC['text2']};
                             margin-left:10px;">· {name}</span>
            </div>
        </div>
        <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
            <div style="text-align:center;">
                <div style="font-size:1.3rem; font-weight:800;
                            color:{'#10b981' if score>=60 else '#f59e0b' if score>=30 else NC['red']};">
                    {score:.1f}%
                </div>
                <div style="font-size:0.68rem; color:{NC['text3']};">Job Match</div>
            </div>
            <div style="width:1px; height:30px; background:{NC['border']};"></div>
            <div style="text-align:center;">
                <div style="font-size:1.3rem; font-weight:800; color:{NC['cyan']};">
                    {rm_pct}%
                </div>
                <div style="font-size:0.68rem; color:{NC['text3']};">Roadmap Done</div>
            </div>
            <div style="width:1px; height:30px; background:{NC['border']};"></div>
            <div style="text-align:center;">
                <div style="font-size:1.3rem; font-weight:800; color:{NC['violet']};">
                    {len(required)}
                </div>
                <div style="font-size:0.68rem; color:{NC['text3']};">Skills Required</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # MAIN LAYOUT  — career graph (large) + right panel
    # ─────────────────────────────────────────────────────────────────────
    graph_col, panel_col = st.columns([2.6, 1], gap="medium")

    with graph_col:
        st.markdown(f"""
        <div class="rm-panel-title">Exploration Graph</div>
        <div style="font-size:0.75rem; color:{NC['text3']}; margin-bottom:6px;">
            Hover nodes for details · Click to highlight path · Scroll to zoom · Drag to pan
        </div>""", unsafe_allow_html=True)

        graph_html = _build_career_graph_html(matched, missing, role)
        components.html(graph_html, height=615, scrolling=False)

    with panel_col:
        # ── Skill summary pills ──────────────────────────────────────────
        st.markdown(f'<div class="rm-panel-title">Skill Status</div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:1rem;">
            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25);
                        border-radius:8px; padding:0.6rem 0.9rem;
                        display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8rem; color:{NC['green']}; font-weight:600;">
                    ✓ Matched
                </span>
                <span style="font-size:1.1rem; font-weight:800; color:{NC['green']};">
                    {len(matched)}
                </span>
            </div>
            <div style="background:rgba(244,63,94,0.08); border:1px solid rgba(244,63,94,0.25);
                        border-radius:8px; padding:0.6rem 0.9rem;
                        display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8rem; color:{NC['red']}; font-weight:600;">
                    ✗ Missing
                </span>
                <span style="font-size:1.1rem; font-weight:800; color:{NC['red']};">
                    {len(missing)}
                </span>
            </div>
            <div style="background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.25);
                        border-radius:8px; padding:0.6rem 0.9rem;
                        display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.8rem; color:{NC['blue']}; font-weight:600;">
                    + Additional
                </span>
                <span style="font-size:1.1rem; font-weight:800; color:{NC['blue']};">
                    {len(additional)}
                </span>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Roadmap progress ring ────────────────────────────────────────
        st.markdown(f'<div class="rm-panel-title">Roadmap Progress</div>',
                    unsafe_allow_html=True)

        prog_color = NC["green"] if rm_pct >= 70 else NC["amber"] if rm_pct >= 30 else NC["cyan"]
        st.markdown(f"""
        <div style="background:rgba(13,21,32,0.8); border:1px solid {NC['border']};
                    border-radius:12px; padding:1rem; text-align:center; margin-bottom:1rem;">
            {_circle_progress("Roadmap", rm_pct, prog_color)}
            <div style="font-size:0.78rem; color:{NC['text3']}; margin-top:4px;">
                {done_count} of {total_rm} skills completed
            </div>
            <div style="margin-top:8px; display:flex; justify-content:center; gap:10px;">
                <span style="font-size:0.72rem; color:{NC['red']};">
                    {counts.get('HIGH',0)} HIGH
                </span>
                <span style="font-size:0.72rem; color:{NC['amber']};">
                    {counts.get('MEDIUM',0)} MED
                </span>
                <span style="font-size:0.72rem; color:{NC['green']};">
                    {counts.get('LOW',0)} LOW
                </span>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Matched skill badges ─────────────────────────────────────────
        if matched:
            st.markdown(f'<div class="rm-panel-title">Matched Skills</div>',
                        unsafe_allow_html=True)
            badges = ""
            for s in matched[:12]:
                badges += (f'<span style="display:inline-block; '
                           f'background:rgba(16,185,129,0.1); '
                           f'border:1px solid rgba(16,185,129,0.3); '
                           f'color:{NC["green"]}; padding:2px 8px; '
                           f'border-radius:12px; font-size:0.71rem; '
                           f'margin:2px;">{s}</span>')
            st.markdown(
                f'<div style="display:flex; flex-wrap:wrap; gap:3px; '
                f'margin-bottom:1rem;">{badges}</div>',
                unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # BOTTOM ANALYTICS  — 3 panels
    # ─────────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="font-size:0.65rem; font-weight:800; color:{NC['text3']};
                letter-spacing:0.1rem; text-transform:uppercase;
                margin:1rem 0 0.6rem;">
        Analytics Panels
    </div>""", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3, gap="medium")

    # ── Panel 1: Skill Analysis ──────────────────────────────────────────
    with p1:
        st.markdown(f"""
        <div style="background:{NC['glass']}; border:1px solid {NC['border']};
                    border-radius:12px; padding:0.9rem 1rem;
                    border-top:2px solid {NC['cyan']};">
            <div class="rm-panel-title">Skill Analysis</div>""",
                    unsafe_allow_html=True)

        if matched or missing:
            fig = _skill_analysis_chart(matched, missing)
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar": False})
        else:
            st.markdown(
                f'<div style="color:{NC["text3"]}; font-size:0.82rem; '
                f'padding:1rem 0;">No skills to display.</div>',
                unsafe_allow_html=True)

        st.markdown(
            f'<div style="font-size:0.7rem; color:{NC["text3"]}; margin-top:4px;">'
            f'Top {min(5,len(matched))} matched · Top {min(5,len(missing))} missing</div>',
            unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Panel 2: Skill Development Gaps ─────────────────────────────────
    with p2:
        st.markdown(f"""
        <div style="background:{NC['glass']}; border:1px solid {NC['border']};
                    border-radius:12px; padding:0.9rem 1rem;
                    border-top:2px solid {NC['violet']};">
            <div class="rm-panel-title">Skill Development Gaps</div>""",
                    unsafe_allow_html=True)

        # Calculate actual gap percentages from the analysis
        total_req = analysis.get("total_required", 0) or 1
        tech_missing = [s for s in missing
                        if s not in {"Communication Skills","Teamwork",
                                     "Leadership","Problem Solving",
                                     "Time Management","Presentation Skills"}]
        soft_missing = [s for s in missing
                        if s in {"Communication Skills","Teamwork",
                                 "Leadership","Problem Solving"}]

        tech_have  = len([s for s in matched if s not in
                          {"Communication Skills","Teamwork","Leadership",
                           "Problem Solving","Time Management"}])
        soft_have  = len([s for s in matched if s in
                          {"Communication Skills","Teamwork","Leadership",
                           "Problem Solving"}])

        tech_total = len(tech_missing) + tech_have
        soft_total = len(soft_missing) + soft_have
        tech_pct   = int(tech_have / tech_total * 100) if tech_total else 0
        soft_pct   = int(soft_have / soft_total * 100) if soft_total else 0
        rm_hi_pct  = int(done_count / max(counts.get("HIGH",1),1) * 100) \
                     if counts.get("HIGH",0) else 0
        overall    = int(score)

        circles_html = '<div style="display:flex; justify-content:space-around; flex-wrap:wrap;">'
        circles_html += _circle_progress("Technical",    tech_pct, NC["cyan"])
        circles_html += _circle_progress("Soft Skills",  soft_pct, NC["violet"])
        circles_html += _circle_progress("High Prio.",   rm_hi_pct,NC["red"])
        circles_html += _circle_progress("Overall",      overall,  NC["amber"])
        circles_html += '</div>'
        st.markdown(circles_html, unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.7rem; color:{NC["text3"]}; margin-top:6px;">'
            f'Based on detected skill overlap · Not assessed = no data provided</div>',
            unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Panel 3: Career Path Progress ───────────────────────────────────
    with p3:
        st.markdown(f"""
        <div style="background:{NC['glass']}; border:1px solid {NC['border']};
                    border-radius:12px; padding:0.9rem 1rem;
                    border-top:2px solid {NC['amber']};">
            <div class="rm-panel-title">Career Path Progress</div>""",
                    unsafe_allow_html=True)

        st.markdown(_career_timeline(score, roadmap, checklist),
                    unsafe_allow_html=True)

        # Mini progress bar
        st.markdown(f"""
        <div style="margin-top:12px;">
            <div style="display:flex; justify-content:space-between;
                        font-size:0.72rem; color:{NC['text3']}; margin-bottom:4px;">
                <span>Roadmap completion</span>
                <span style="color:{NC['amber']}; font-weight:700;">{rm_pct}%</span>
            </div>
            <div style="background:{NC['border']}; border-radius:4px; height:5px; overflow:hidden;">
                <div style="background:linear-gradient(90deg,{NC['cyan']},{NC['violet']},{NC['amber']});
                            height:100%; width:{rm_pct}%; border-radius:4px;
                            box-shadow:0 0 8px {NC['cyan']};
                            transition:width 0.5s ease;">
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # LEARNING ROADMAP CHECKLIST
    # ─────────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:{NC['glass']}; border:1px solid {NC['border']};
                border-radius:14px; padding:1.2rem 1.4rem; margin-top:1rem;
                border-top:2px solid {NC['magenta']};">
        <div style="display:flex; align-items:center; justify-content:space-between;
                    margin-bottom:0.8rem; flex-wrap:wrap; gap:8px;">
            <div>
                <div class="rm-panel-title" style="margin-bottom:2px;">
                    My Learning Roadmap
                </div>
                <div style="font-size:0.78rem; color:{NC['text3']};">
                    {total_rm} skills · Check off as you complete each one
                </div>
            </div>
            <div style="display:flex; gap:10px;">
                <span style="font-size:0.78rem; color:{NC['red']}; font-weight:700;">
                    {counts.get('HIGH',0)} High
                </span>
                <span style="font-size:0.78rem; color:{NC['amber']}; font-weight:700;">
                    {counts.get('MEDIUM',0)} Medium
                </span>
                <span style="font-size:0.78rem; color:{NC['green']}; font-weight:700;">
                    {counts.get('LOW',0)} Low
                </span>
            </div>
        </div>""", unsafe_allow_html=True)

    # Filter
    col_f, _ = st.columns([1, 3])
    with col_f:
        filter_p = st.selectbox(
            "Filter", ["All", "HIGH", "MEDIUM", "LOW"],
            key="fut_rm_filter",
            label_visibility="collapsed",
        )

    filtered = [i for i in roadmap
                if filter_p == "All" or i["priority"] == filter_p]

    _render_roadmap_checklist(filtered)

    # Overall progress bar — read after all checkboxes rendered
    final_done = sum(1 for i in roadmap
                     if st.session_state.checklist.get(i["skill"], False))
    final_pct  = int(final_done / total_rm * 100) if total_rm else 0

    st.markdown(f"""
    <div style="margin-top:1rem; padding-top:1rem; border-top:1px solid {NC['border']};">
        <div style="display:flex; justify-content:space-between; align-items:center;
                    margin-bottom:6px; flex-wrap:wrap; gap:4px;">
            <span style="font-size:0.82rem; font-weight:700; color:{NC['text2']};">
                Overall Progress
            </span>
            <span style="font-size:0.82rem; font-weight:800; color:{NC['cyan']};">
                {final_done} / {total_rm} &nbsp;({final_pct}%)
            </span>
        </div>
        <div style="background:{NC['border']}; border-radius:6px; height:8px; overflow:hidden;">
            <div style="background:linear-gradient(90deg,{NC['cyan']},{NC['violet']},{NC['magenta']});
                        height:100%; width:{final_pct}%; border-radius:6px;
                        box-shadow:0 0 10px {NC['cyan']}66;
                        transition:width 0.4s ease;">
            </div>
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

    if final_done == total_rm and total_rm > 0:
        st.success("🎉 All roadmap skills completed — outstanding work!")
