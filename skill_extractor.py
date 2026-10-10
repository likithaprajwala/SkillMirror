"""
skill_extractor.py
------------------
Contains the master skill dictionary and functions for extracting
skills from a job description text.

To add new skills: simply add an entry to SKILL_DICTIONARY below.
Each key is the canonical skill name; the value is a list of aliases
(variations, abbreviations, or common misspellings).
"""

import re

# ---------------------------------------------------------------------------
# Master Skill Dictionary
# Key   -> canonical display name
# Value -> list of text aliases to look for (case-insensitive)
# ---------------------------------------------------------------------------
SKILL_DICTIONARY = {
    # Programming Languages
    "Python": ["python", "python3", "python 3"],
    "Java": ["java", "java se", "java ee", "core java"],
    "C++": ["c++", "cpp", "c plus plus"],
    "C": ["c language", " c ", "c programming"],
    "C#": ["c#", "csharp", "c sharp", "dotnet c#"],
    "JavaScript": ["javascript", "js", "es6", "es2015", "ecmascript"],
    "TypeScript": ["typescript", "ts"],
    "Go": ["golang", "go language", " go "],
    "Rust": ["rust", "rust lang"],
    "Swift": ["swift", "swift language"],
    "Kotlin": ["kotlin"],
    "R": [" r language", "r programming", "r studio", "rstudio"],
    "PHP": ["php", "php7", "php8"],
    "Ruby": ["ruby", "ruby on rails", "rails"],
    "Scala": ["scala"],
    "MATLAB": ["matlab"],
    "Bash": ["bash", "shell scripting", "bash scripting", "shell script"],
    "PowerShell": ["powershell"],

    # Web Frontend
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "reactjs", "react.js"],
    "Angular": ["angular", "angularjs", "angular.js"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Next.js": ["next.js", "nextjs"],
    "Bootstrap": ["bootstrap"],
    "Tailwind CSS": ["tailwind", "tailwindcss", "tailwind css"],
    "jQuery": ["jquery"],

    # Web Backend
    "Node.js": ["node", "nodejs", "node.js"],
    "Express.js": ["express", "expressjs", "express.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Spring Boot": ["spring boot", "springboot", "spring framework", "spring"],
    "Laravel": ["laravel"],
    "ASP.NET": ["asp.net", "aspnet", ".net core", "dotnet"],

    # Databases
    "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "SQLite": ["sqlite"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "Cassandra": ["cassandra"],
    "Oracle DB": ["oracle", "oracle db", "oracle database"],
    "MS SQL Server": ["sql server", "mssql", "microsoft sql"],
    "Firebase": ["firebase", "firestore"],

    # Data Science & ML
    "Machine Learning": ["machine learning", "ml", "supervised learning",
                         "unsupervised learning"],
    "Deep Learning": ["deep learning", "dl", "neural networks", "neural network"],
    "Natural Language Processing": ["nlp", "natural language processing",
                                    "text mining", "text analytics"],
    "Computer Vision": ["computer vision", "cv", "image processing",
                        "image recognition"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Keras": ["keras"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Plotly": ["plotly"],
    "Jupyter Notebook": ["jupyter", "jupyter notebook", "ipynb"],

    # Data Engineering & Analytics
    "Data Analysis": ["data analysis", "data analytics", "data analyst"],
    "Data Visualization": ["data visualization", "data viz", "dashboards"],
    "Statistics": ["statistics", "statistical analysis", "probability",
                   "statistical modeling"],
    "Excel": ["excel", "ms excel", "microsoft excel", "spreadsheets"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Apache Spark": ["spark", "apache spark", "pyspark"],
    "Hadoop": ["hadoop", "hdfs", "mapreduce"],
    "ETL": ["etl", "extract transform load", "data pipeline"],

    # Cloud & DevOps
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda",
            "aws cloud", "amazon cloud"],
    "Azure": ["azure", "microsoft azure", "azure cloud"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "cicd", "continuous integration", "continuous deployment",
               "jenkins", "github actions", "gitlab ci"],
    "Linux": ["linux", "unix", "ubuntu", "centos"],
    "Terraform": ["terraform", "infrastructure as code", "iac"],

    # Version Control
    "Git": ["git", "version control"],
    "GitHub": ["github"],
    "GitLab": ["gitlab"],

    # Software Engineering
    "Data Structures": ["data structures", "dsa", "algorithms", "data structures and algorithms"],
    "Object-Oriented Programming": ["oop", "object-oriented", "object oriented programming",
                                    "oops", "object-oriented programming"],
    "REST APIs": ["rest api", "restful api", "rest", "api design", "api development",
                  "restful", "rest apis", "web api"],
    "GraphQL": ["graphql"],
    "Microservices": ["microservices", "microservice architecture"],
    "System Design": ["system design", "high-level design", "hld", "low-level design", "lld"],
    "Design Patterns": ["design patterns", "solid principles"],
    "Agile": ["agile", "scrum", "kanban", "sprint"],
    "Unit Testing": ["unit testing", "test-driven development", "tdd",
                     "pytest", "junit", "testing"],
    "DevOps": ["devops"],

    # Cybersecurity
    "Cybersecurity": ["cybersecurity", "information security", "infosec",
                      "network security", "ethical hacking", "penetration testing"],
    "Cryptography": ["cryptography", "encryption"],

    # Soft Skills
    "Communication Skills": ["communication", "verbal communication",
                              "written communication", "communication skills"],
    "Problem Solving": ["problem solving", "problem-solving", "analytical thinking",
                        "analytical skills"],
    "Teamwork": ["teamwork", "team player", "collaboration", "collaborative"],
    "Leadership": ["leadership", "team lead", "mentoring"],
    "Time Management": ["time management"],
    "Critical Thinking": ["critical thinking"],
    "Presentation Skills": ["presentation", "presentation skills", "public speaking"],
    "Documentation": ["documentation", "technical writing"],

    # Miscellaneous
    "Microsoft Office": ["ms office", "microsoft office", "word", "powerpoint"],
    "Project Management": ["project management", "pmp", "project planning"],
    "UI/UX Design": ["ui/ux", "user interface", "user experience", "figma",
                     "ux design", "ui design"],
}


def normalize_skill(skill: str) -> str:
    """
    Lowercase and strip whitespace from a skill name.
    Used to compare skills in a case-insensitive manner.
    """
    return skill.strip().lower()


def extract_skills_from_text(text: str) -> list:
    """
    Scan a job description text and return a list of canonical skill names
    found in that text.

    Strategy:
    - Convert text to lowercase.
    - For each skill in the dictionary, check if any alias appears in the text
      using word-boundary-aware regex so 'C' is not matched inside 'React'.
    - Return deduplicated list of matched canonical skill names.
    """
    if not text or not text.strip():
        return []

    text_lower = text.lower()
    found_skills = []

    for canonical_name, aliases in SKILL_DICTIONARY.items():
        matched = False
        for alias in aliases:
            alias_stripped = alias.strip()
            # Use word boundaries for short/ambiguous aliases to reduce false positives
            # e.g., avoid matching "R" inside "React"
            if len(alias_stripped) <= 3:
                pattern = r'\b' + re.escape(alias_stripped) + r'\b'
            else:
                pattern = re.escape(alias_stripped)
            if re.search(pattern, text_lower):
                matched = True
                break
        if matched:
            found_skills.append(canonical_name)

    return found_skills


def parse_user_skills(raw_input: str) -> list:
    """
    Parse a comma-separated or newline-separated string of user-entered skills.

    Returns a deduplicated list of canonical skill names where a match exists
    in the dictionary, or the cleaned raw name if no match is found.
    """
    if not raw_input or not raw_input.strip():
        return []

    # Split on commas, semicolons, or newlines
    separators = r'[,;\n]'
    raw_skills = re.split(separators, raw_input)

    parsed = []
    seen = set()

    for raw in raw_skills:
        skill = raw.strip()
        if not skill:
            continue

        canonical = _match_to_canonical(skill)
        key = normalize_skill(canonical)

        if key not in seen:
            seen.add(key)
            parsed.append(canonical)

    return parsed


def _match_to_canonical(skill: str) -> str:
    """
    Try to match a user-entered skill string to a canonical name from the
    dictionary. Returns the canonical name if found, otherwise returns the
    original string with title-cased formatting.
    """
    skill_lower = normalize_skill(skill)

    for canonical_name, aliases in SKILL_DICTIONARY.items():
        # Check if the input matches the canonical name itself
        if skill_lower == normalize_skill(canonical_name):
            return canonical_name
        # Check if the input matches any alias
        for alias in aliases:
            if skill_lower == alias.strip().lower():
                return canonical_name

    # No match found — return cleaned original
    return skill.strip().title()


def get_all_predefined_skills() -> list:
    """
    Return a sorted list of all canonical skill names in the dictionary.
    Used to populate the skill suggestions UI.
    """
    return sorted(SKILL_DICTIONARY.keys())


def get_suggested_skills() -> list:
    """
    Return a curated shortlist of common skills shown as quick-add suggestions
    in the student profile section.
    """
    return [
        "Python", "Java", "C++", "JavaScript", "SQL",
        "HTML", "CSS", "React", "Git", "GitHub",
        "Data Structures", "Machine Learning", "Pandas",
        "NumPy", "REST APIs", "Communication Skills",
        "Problem Solving", "Teamwork", "Linux", "Docker",
    ]
