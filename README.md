# 🪞 SkillMirror — Job Skill Gap Detector

A Python + Streamlit career analytics project that helps students understand how well their current skills match a job opportunity, identifies missing skills, and generates a personalised learning roadmap — with a futuristic dark-theme dashboard.

---

## Problem Statement

Students and fresh graduates often apply for jobs without a clear picture of which skills they need to develop. Reading a job description manually and comparing it to your resume is tedious and subjective. SkillMirror automates this process with transparent, rule-based skill matching — no AI model, no API key, no internet connection needed after installation.

---

## Objectives

- Extract required technical and soft skills from any pasted job description.
- Compare them with the student's self-reported skills.
- Calculate a transparent skill match score.
- Identify matched skills, missing skills, and additional skills.
- Generate a prioritised learning roadmap with practical tasks.
- Display results in a premium dark-theme career analytics dashboard.
- Allow the student to download a full analysis report.

---

## Features

| Feature | Description |
|---|---|
| Student Profile | Name, degree, target role, experience level |
| Skill Input | Free-text entry, multiselect picker, 80+ skill suggestions |
| Job Description Analyser | Auto-extracts skills from pasted job descriptions |
| Skill Gap Analysis | Matched / Missing / Additional skill categories |
| Match Score | Transparent formula: `(Matched / Required) × 100` |
| Score Gauge | Plotly gauge chart with colour-coded zones |
| Donut Chart | Matched vs Missing vs Additional skill coverage |
| Radar Chart | Skills requirements comparison |
| Missing Skills Bar | Priority-ranked horizontal bar chart |
| Sample Job Descriptions | Python Developer, Java Developer, Data Analyst, ML Intern |
| Career Exploration Graph | Interactive SVG career-path graph with pan, zoom, and hover |
| Learning Roadmap | Prioritised checklist with topics, tasks, and estimated hours |
| Analytics Panels | Skill analysis bar, gap circles, career path timeline |
| Session Progress | Checkbox state preserved during the session |
| Downloadable Report | TXT and CSV formats with full analysis |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit 1.35 | Web interface and page routing |
| Plotly 5.22 | Interactive charts (gauge, donut, radar, bar) |
| Pandas 2.2 | Data processing |
| scikit-learn 1.5 | Dependency (future NLP features) |
| NumPy 1.26 | Numerical operations |
| HTML / CSS / JS | Career exploration graph via `st.components.v1.html` |

> Works with **no API key, no paid service, and no internet** after installation.

---

## Project Structure

```
SkillMirror/
├── app.py              ← Main Streamlit application — page routing and UI
├── roadmap_page.py     ← Futuristic Learning Roadmap page module
├── skill_extractor.py  ← Skill dictionary (80+ skills) and extraction logic
├── skill_matcher.py    ← Matching, scoring, and gap analysis
├── roadmap.py          ← Roadmap generation, priority logic, metadata
├── sample_jobs.py      ← Four built-in sample job descriptions
├── requirements.txt    ← Python dependencies with pinned versions
├── README.md           ← This file
└── .gitignore          ← Git ignore rules
```

---

## Installation — Run Locally on Windows

### Prerequisites

- Python 3.10 or newer — [Download Python](https://www.python.org/downloads/)
- Git — [Download Git](https://git-scm.com/)

### Steps

Open **PowerShell** or **VS Code Terminal**:

```powershell
# 1. Clone the repository
git clone https://github.com/likithaprajwala/SkillMirror.git
cd SkillMirror

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
.\.venv\Scripts\Activate.ps1

# If you see a permissions error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**.

---

## How to Use

1. Fill in your **profile** in the sidebar (name, degree, target role, experience).
2. Go to **🔍 Analyse Job** — enter your skills and paste a job description (or pick a sample).
3. Click **Analyse Skills**.
4. View your **📊 Dashboard** — match score, charts, and skill breakdown tabs.
5. Open **🗺️ Learning Roadmap** — explore the career graph, analytics panels, and your personalised checklist.
6. Check off skills as you complete them — progress is saved for the session.
7. Go to **📥 Reports** — download your full analysis as TXT or CSV.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: streamlit` | Activate the venv: `.\.venv\Scripts\Activate.ps1` |
| `ModuleNotFoundError: plotly` | Run `pip install -r requirements.txt` again |
| PowerShell execution policy error | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Skills not detected | The skill must match an alias in `skill_extractor.py` |
| Match score is 0% | Your skills list may be empty or not match the job description |
| Career graph is blank | Ensure the browser has JavaScript enabled |

---

## Limitations

- Skill matching is **text-based** (rule-based). It does not understand context.
- The match score measures **skill text overlap** only — not actual hiring probability.
- The skill dictionary covers ~80 common skills. Niche or new skills may not be detected.
- Priority rankings in the roadmap are general guidelines, not AI recommendations.
- No user authentication or database — all state resets when the session ends.

---

## Future Enhancements

- Add TF-IDF or spaCy NLP for smarter skill extraction from unstructured JDs.
- Allow users to upload a resume PDF and extract skills automatically.
- Add a skills gap comparison across multiple job listings.
- Persist user profiles and checklist progress in a database.
- Add a recommendation engine that suggests courses from Coursera or YouTube.
- Support multiple languages.

---

## License

This project is open-source and free to use for educational purposes.

---

*SkillMirror — built with Python & Streamlit. Rule-based matching — no API key required.*
