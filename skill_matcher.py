"""
skill_matcher.py
----------------
Handles comparison between student skills and job-required skills.
Calculates the match score and identifies matched, missing, and
additional skills.

All logic is rule-based (no ML model required for basic usage).
"""

from skill_extractor import normalize_skill


# ---------------------------------------------------------------------------
# Core Matching Functions
# ---------------------------------------------------------------------------

def match_skills(student_skills: list, required_skills: list) -> dict:
    """
    Compare student skills against job-required skills.

    Parameters
    ----------
    student_skills  : list of canonical skill names the student has
    required_skills : list of canonical skill names from the job description

    Returns
    -------
    dict with keys:
        matched    - skills present in both lists
        missing    - skills in required but NOT in student
        additional - skills in student but NOT in required
        score      - float 0-100 representing match percentage
        total_required - count of required skills
        total_student  - count of student skills
    """
    if not required_skills:
        return {
            "matched": [],
            "missing": [],
            "additional": list(student_skills),
            "score": 0.0,
            "total_required": 0,
            "total_student": len(student_skills),
            "error": "no_required_skills",
        }

    # Normalise for case-insensitive, whitespace-insensitive comparison
    student_set = {normalize_skill(s): s for s in student_skills}
    required_set = {normalize_skill(r): r for r in required_skills}

    matched_keys = set(student_set.keys()) & set(required_set.keys())
    missing_keys = set(required_set.keys()) - set(student_set.keys())
    additional_keys = set(student_set.keys()) - set(required_set.keys())

    # Retrieve original display names
    matched = sorted([required_set[k] for k in matched_keys])
    missing = sorted([required_set[k] for k in missing_keys])
    additional = sorted([student_set[k] for k in additional_keys])

    score = _calculate_score(len(matched), len(required_skills))

    return {
        "matched": matched,
        "missing": missing,
        "additional": additional,
        "score": score,
        "total_required": len(required_skills),
        "total_student": len(student_skills),
        "error": None,
    }


def _calculate_score(matched_count: int, total_required: int) -> float:
    """
    Match Score formula:
        (Matched Skills / Total Required Skills) × 100

    Returns 0.0 if total_required is 0 to avoid ZeroDivisionError.
    Score is clamped to [0, 100].
    """
    if total_required == 0:
        return 0.0
    raw = (matched_count / total_required) * 100
    return round(min(max(raw, 0.0), 100.0), 1)


def get_score_label(score: float) -> dict:
    """
    Map a numeric score to a human-readable label and colour hint
    suitable for display in the UI.
    """
    if score >= 80:
        return {"label": "Excellent Match", "color": "#2ecc71", "emoji": "🌟"}
    elif score >= 60:
        return {"label": "Good Match", "color": "#27ae60", "emoji": "✅"}
    elif score >= 40:
        return {"label": "Moderate Match", "color": "#f39c12", "emoji": "⚠️"}
    elif score >= 20:
        return {"label": "Low Match", "color": "#e67e22", "emoji": "📚"}
    else:
        return {"label": "Needs Improvement", "color": "#e74c3c", "emoji": "🔴"}


def deduplicate_skills(skills: list) -> list:
    """
    Remove duplicates from a skill list while preserving order.
    Comparison is case-insensitive.
    """
    seen = set()
    result = []
    for skill in skills:
        key = normalize_skill(skill)
        if key not in seen:
            seen.add(key)
            result.append(skill)
    return result


def summarise_results(analysis: dict, student_name: str = "",
                      target_role: str = "") -> str:
    """
    Build a plain-text summary of the analysis suitable for display
    in the UI and for inclusion in the downloadable report.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("  SkillMirror — Skill Gap Analysis Report")
    lines.append("=" * 60)

    if student_name:
        lines.append(f"Student       : {student_name}")
    if target_role:
        lines.append(f"Target Role   : {target_role}")

    lines.append(f"Match Score   : {analysis['score']}%")
    lines.append(f"Required Skills Detected : {analysis['total_required']}")
    lines.append(f"Matched Skills           : {len(analysis['matched'])}")
    lines.append(f"Missing Skills           : {len(analysis['missing'])}")
    lines.append(f"Additional Skills        : {len(analysis['additional'])}")
    lines.append("")

    lines.append("--- Matched Skills ---")
    if analysis["matched"]:
        for s in analysis["matched"]:
            lines.append(f"  ✓ {s}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("--- Missing Skills ---")
    if analysis["missing"]:
        for s in analysis["missing"]:
            lines.append(f"  ✗ {s}")
    else:
        lines.append("  (none — all required skills matched!)")

    lines.append("")
    lines.append("--- Additional Skills (Not Listed in JD) ---")
    if analysis["additional"]:
        for s in analysis["additional"]:
            lines.append(f"  + {s}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("NOTE: Match Score measures skill overlap only.")
    lines.append("It does not predict actual hiring probability.")
    lines.append("=" * 60)

    return "\n".join(lines)
