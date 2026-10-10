"""
roadmap.py
----------
Generates a personalised learning roadmap from the list of missing skills.

Priority Rules (transparent and explainable):
- HIGH   : foundational programming, core tools, and domain-critical skills
           that most job listings require and that unblock other learning.
- MEDIUM : supporting technical skills and frameworks that build on the core.
- LOW    : optional, complementary, or role-specific advanced topics.

Students should focus on HIGH-priority skills first, then MEDIUM, then LOW.
These priorities are general guidelines and may differ based on your specific
role, team, and company.
"""

# ---------------------------------------------------------------------------
# Skill Metadata Catalogue
# Keyed by canonical skill name (must match SKILL_DICTIONARY keys).
# Each entry contains: priority, topic, and a practical mini-task.
# ---------------------------------------------------------------------------
SKILL_METADATA = {
    # --- Programming Languages ---
    "Python": {
        "priority": "HIGH",
        "topic": "Python Programming Fundamentals",
        "task": "Write a Python script that reads a CSV file and prints row counts per column.",
    },
    "Java": {
        "priority": "HIGH",
        "topic": "Core Java & OOP Concepts",
        "task": "Build a simple Student Management System using Java classes and ArrayLists.",
    },
    "C++": {
        "priority": "HIGH",
        "topic": "C++ Fundamentals and Pointers",
        "task": "Implement a stack using C++ classes and dynamic memory allocation.",
    },
    "C": {
        "priority": "HIGH",
        "topic": "C Programming and Memory Management",
        "task": "Write a C program to sort an array using bubble sort.",
    },
    "C#": {
        "priority": "MEDIUM",
        "topic": "C# and .NET Basics",
        "task": "Create a console-based to-do list application in C#.",
    },
    "JavaScript": {
        "priority": "HIGH",
        "topic": "JavaScript ES6+ Fundamentals",
        "task": "Build a dynamic to-do list webpage using vanilla JavaScript.",
    },
    "TypeScript": {
        "priority": "MEDIUM",
        "topic": "TypeScript Types and Interfaces",
        "task": "Refactor a JavaScript project to TypeScript and add type annotations.",
    },
    "Go": {
        "priority": "MEDIUM",
        "topic": "Go Language Basics and Concurrency",
        "task": "Write a Go program that spawns goroutines to fetch data concurrently.",
    },
    "Rust": {
        "priority": "LOW",
        "topic": "Rust Ownership and Safety Model",
        "task": "Implement a basic linked list in Rust without using unsafe code.",
    },
    "Swift": {
        "priority": "MEDIUM",
        "topic": "Swift for iOS Development",
        "task": "Build a simple iOS calculator app in Swift using Xcode.",
    },
    "Kotlin": {
        "priority": "MEDIUM",
        "topic": "Kotlin for Android Development",
        "task": "Create a basic Android app in Kotlin that displays a list of items.",
    },
    "R": {
        "priority": "MEDIUM",
        "topic": "R for Statistical Analysis",
        "task": "Load a dataset in R and produce a summary statistics report with ggplot2.",
    },
    "PHP": {
        "priority": "MEDIUM",
        "topic": "PHP Web Development Basics",
        "task": "Build a contact form with PHP that stores submissions in a MySQL table.",
    },
    "Ruby": {
        "priority": "MEDIUM",
        "topic": "Ruby on Rails MVC Pattern",
        "task": "Create a simple blog app using Ruby on Rails with CRUD operations.",
    },
    "Scala": {
        "priority": "LOW",
        "topic": "Scala Functional Programming",
        "task": "Write Scala code to process a list using map, filter, and reduce.",
    },
    "MATLAB": {
        "priority": "LOW",
        "topic": "MATLAB for Numerical Computing",
        "task": "Plot a sinusoidal signal and apply a simple FFT in MATLAB.",
    },
    "Bash": {
        "priority": "MEDIUM",
        "topic": "Bash Scripting for Automation",
        "task": "Write a Bash script to automate directory backup with timestamps.",
    },
    "PowerShell": {
        "priority": "LOW",
        "topic": "PowerShell Scripting on Windows",
        "task": "Write a PowerShell script that lists all running processes sorted by CPU.",
    },

    # --- Web Frontend ---
    "HTML": {
        "priority": "HIGH",
        "topic": "HTML5 Structure and Semantics",
        "task": "Build a personal portfolio webpage using semantic HTML5 tags.",
    },
    "CSS": {
        "priority": "HIGH",
        "topic": "CSS3 Layouts and Responsive Design",
        "task": "Style the portfolio page using Flexbox, Grid, and a mobile-first approach.",
    },
    "React": {
        "priority": "HIGH",
        "topic": "React Components, Hooks, and State",
        "task": "Build a weather dashboard React app that fetches and displays city data.",
    },
    "Angular": {
        "priority": "MEDIUM",
        "topic": "Angular Components and Services",
        "task": "Create an Angular app with a reusable card component and HTTP service.",
    },
    "Vue.js": {
        "priority": "MEDIUM",
        "topic": "Vue.js Reactivity and Component System",
        "task": "Build a simple quiz app using Vue.js with reactive data binding.",
    },
    "Next.js": {
        "priority": "MEDIUM",
        "topic": "Next.js Server-Side Rendering and Routing",
        "task": "Build a blog with Next.js using static site generation (SSG).",
    },
    "Bootstrap": {
        "priority": "MEDIUM",
        "topic": "Bootstrap Grid and Components",
        "task": "Convert a raw HTML page to a responsive Bootstrap 5 layout.",
    },
    "Tailwind CSS": {
        "priority": "MEDIUM",
        "topic": "Tailwind CSS Utility-First Styling",
        "task": "Redesign a UI page using only Tailwind CSS utility classes.",
    },
    "jQuery": {
        "priority": "LOW",
        "topic": "jQuery DOM Manipulation",
        "task": "Add interactive accordion and tab components to a webpage using jQuery.",
    },

    # --- Web Backend ---
    "Node.js": {
        "priority": "HIGH",
        "topic": "Node.js Event Loop and Async Programming",
        "task": "Build a REST API with Node.js and Express for a task manager app.",
    },
    "Express.js": {
        "priority": "HIGH",
        "topic": "Express.js Routing and Middleware",
        "task": "Build a RESTful API with Express.js that includes CRUD routes and validation.",
    },
    "Django": {
        "priority": "HIGH",
        "topic": "Django MVT Architecture and ORM",
        "task": "Build a blog with Django where users can create, edit, and delete posts.",
    },
    "Flask": {
        "priority": "HIGH",
        "topic": "Flask Routing, Templates, and Forms",
        "task": "Create a Flask app with a login page and a protected dashboard route.",
    },
    "FastAPI": {
        "priority": "MEDIUM",
        "topic": "FastAPI for Modern Python APIs",
        "task": "Build a FastAPI service that validates input with Pydantic and returns JSON.",
    },
    "Spring Boot": {
        "priority": "HIGH",
        "topic": "Spring Boot REST APIs and JPA",
        "task": "Build a product catalogue REST API using Spring Boot and H2 database.",
    },
    "Laravel": {
        "priority": "MEDIUM",
        "topic": "Laravel MVC and Eloquent ORM",
        "task": "Create a Laravel app with authentication and a simple CRUD for a resource.",
    },
    "ASP.NET": {
        "priority": "MEDIUM",
        "topic": "ASP.NET Core Web API Development",
        "task": "Build a student management API with ASP.NET Core and Entity Framework.",
    },

    # --- Databases ---
    "SQL": {
        "priority": "HIGH",
        "topic": "SQL Queries: SELECT, JOIN, GROUP BY, Subqueries",
        "task": "Write SQL queries on a sample sales database to answer 10 business questions.",
    },
    "MySQL": {
        "priority": "HIGH",
        "topic": "MySQL Database Design and Queries",
        "task": "Design an ER diagram and implement a library management database in MySQL.",
    },
    "PostgreSQL": {
        "priority": "MEDIUM",
        "topic": "PostgreSQL Advanced Features",
        "task": "Use PostgreSQL window functions to calculate running totals on order data.",
    },
    "SQLite": {
        "priority": "MEDIUM",
        "topic": "SQLite for Embedded Applications",
        "task": "Build a Python CLI app that uses SQLite to manage personal expenses.",
    },
    "MongoDB": {
        "priority": "MEDIUM",
        "topic": "MongoDB Document Model and Aggregation",
        "task": "Build a Node.js app that stores and queries blog posts in MongoDB.",
    },
    "Redis": {
        "priority": "LOW",
        "topic": "Redis Caching and Data Structures",
        "task": "Add Redis caching to an API endpoint to reduce database calls.",
    },
    "Firebase": {
        "priority": "MEDIUM",
        "topic": "Firebase Realtime Database and Auth",
        "task": "Build a real-time chat app using Firebase Realtime Database and Firebase Auth.",
    },

    # --- Data Science & ML ---
    "Machine Learning": {
        "priority": "HIGH",
        "topic": "ML Algorithms: Regression, Classification, Clustering",
        "task": "Train a classifier on the Iris dataset and evaluate accuracy using scikit-learn.",
    },
    "Deep Learning": {
        "priority": "MEDIUM",
        "topic": "Neural Network Architecture and Backpropagation",
        "task": "Build and train a simple CNN to classify MNIST handwritten digits.",
    },
    "Natural Language Processing": {
        "priority": "MEDIUM",
        "topic": "Text Preprocessing, TF-IDF, Sentiment Analysis",
        "task": "Build a sentiment classifier on movie reviews using TF-IDF and Logistic Regression.",
    },
    "Computer Vision": {
        "priority": "MEDIUM",
        "topic": "Image Processing with OpenCV and CNNs",
        "task": "Use OpenCV to detect faces in images using Haar cascades.",
    },
    "TensorFlow": {
        "priority": "MEDIUM",
        "topic": "TensorFlow 2.x Model Building and Training",
        "task": "Train a TensorFlow neural network on the CIFAR-10 dataset.",
    },
    "PyTorch": {
        "priority": "MEDIUM",
        "topic": "PyTorch Tensors, Autograd, and Training Loops",
        "task": "Implement a custom training loop in PyTorch for a binary classification task.",
    },
    "Keras": {
        "priority": "MEDIUM",
        "topic": "Keras Sequential and Functional API",
        "task": "Build an image classification model with Keras on the MNIST dataset.",
    },
    "Scikit-learn": {
        "priority": "HIGH",
        "topic": "Scikit-learn Pipelines and Model Evaluation",
        "task": "Build an end-to-end ML pipeline using scikit-learn with preprocessing and cross-validation.",
    },
    "Pandas": {
        "priority": "HIGH",
        "topic": "Pandas DataFrames: Load, Clean, Transform",
        "task": "Analyse a real-world CSV dataset using Pandas: handle nulls, merge tables, group and aggregate.",
    },
    "NumPy": {
        "priority": "HIGH",
        "topic": "NumPy Arrays, Broadcasting, and Linear Algebra",
        "task": "Implement matrix multiplication and compute basic statistics using NumPy.",
    },
    "Matplotlib": {
        "priority": "MEDIUM",
        "topic": "Matplotlib Charts and Subplots",
        "task": "Create a multi-panel figure with bar, line, and scatter charts using Matplotlib.",
    },
    "Seaborn": {
        "priority": "MEDIUM",
        "topic": "Seaborn Statistical Visualizations",
        "task": "Generate a heatmap and pair plot for a dataset using Seaborn.",
    },
    "Plotly": {
        "priority": "MEDIUM",
        "topic": "Plotly Interactive Charts",
        "task": "Build an interactive dashboard with dropdown-controlled Plotly charts.",
    },
    "Jupyter Notebook": {
        "priority": "HIGH",
        "topic": "Jupyter for Exploratory Data Analysis",
        "task": "Conduct a full EDA on a public dataset inside a Jupyter Notebook.",
    },

    # --- Data Engineering & Analytics ---
    "Data Analysis": {
        "priority": "HIGH",
        "topic": "Data Analysis Workflow: Load, Clean, Explore, Report",
        "task": "Perform a complete data analysis project on a Kaggle dataset and share findings.",
    },
    "Data Visualization": {
        "priority": "MEDIUM",
        "topic": "Effective Data Storytelling with Charts",
        "task": "Create a visual report comparing two datasets using at least three chart types.",
    },
    "Statistics": {
        "priority": "HIGH",
        "topic": "Descriptive Stats, Hypothesis Testing, Distributions",
        "task": "Perform a t-test on two sample datasets and interpret the p-value.",
    },
    "Excel": {
        "priority": "MEDIUM",
        "topic": "Excel PivotTables, VLOOKUP, and Charts",
        "task": "Build a monthly sales dashboard in Excel using PivotTables and conditional formatting.",
    },
    "Power BI": {
        "priority": "MEDIUM",
        "topic": "Power BI Reports and DAX Basics",
        "task": "Connect a CSV to Power BI and build an interactive sales report.",
    },
    "Tableau": {
        "priority": "MEDIUM",
        "topic": "Tableau Dashboards and Calculated Fields",
        "task": "Create a Tableau Public dashboard showing geographical sales distribution.",
    },
    "Apache Spark": {
        "priority": "LOW",
        "topic": "Spark RDDs, DataFrames, and SparkSQL",
        "task": "Process a large CSV with PySpark and compute aggregated statistics.",
    },
    "ETL": {
        "priority": "MEDIUM",
        "topic": "ETL Pipelines: Extract, Transform, Load",
        "task": "Build a Python ETL script that reads an API, transforms the data, and loads to CSV.",
    },

    # --- Cloud & DevOps ---
    "AWS": {
        "priority": "MEDIUM",
        "topic": "AWS Core Services: EC2, S3, IAM, Lambda",
        "task": "Deploy a static website to S3 and set up a Lambda function triggered by an event.",
    },
    "Azure": {
        "priority": "MEDIUM",
        "topic": "Azure App Service and Azure DevOps Basics",
        "task": "Deploy a web app to Azure App Service and set up a CI pipeline.",
    },
    "GCP": {
        "priority": "LOW",
        "topic": "GCP Compute Engine and BigQuery",
        "task": "Run a SQL query on a public BigQuery dataset and visualise the results.",
    },
    "Docker": {
        "priority": "HIGH",
        "topic": "Docker Containers, Images, and Compose",
        "task": "Dockerise a Python web application and run it locally using docker-compose.",
    },
    "Kubernetes": {
        "priority": "LOW",
        "topic": "Kubernetes Pods, Services, and Deployments",
        "task": "Deploy a simple containerised application on a local Minikube cluster.",
    },
    "CI/CD": {
        "priority": "MEDIUM",
        "topic": "GitHub Actions for Automated Testing and Deployment",
        "task": "Set up a GitHub Actions workflow that runs tests on every push to main.",
    },
    "Linux": {
        "priority": "HIGH",
        "topic": "Linux Command Line: Navigation, Permissions, Processes",
        "task": "Complete a set of 20 Linux command-line exercises on a free online sandbox.",
    },
    "Terraform": {
        "priority": "LOW",
        "topic": "Terraform for Infrastructure as Code",
        "task": "Write Terraform scripts to provision an S3 bucket and EC2 instance on AWS.",
    },

    # --- Version Control ---
    "Git": {
        "priority": "HIGH",
        "topic": "Git: Commit, Branch, Merge, Rebase",
        "task": "Create a Git repository, branch for a feature, merge via pull request, and resolve a conflict.",
    },
    "GitHub": {
        "priority": "HIGH",
        "topic": "GitHub: Repos, Pull Requests, Issues, Actions",
        "task": "Contribute to an open-source project by forking, making a change, and opening a PR.",
    },
    "GitLab": {
        "priority": "MEDIUM",
        "topic": "GitLab CI/CD Pipelines",
        "task": "Configure a .gitlab-ci.yml file to run unit tests on every commit.",
    },

    # --- Software Engineering ---
    "Data Structures": {
        "priority": "HIGH",
        "topic": "Arrays, Linked Lists, Stacks, Queues, Trees, Graphs",
        "task": "Solve 20 LeetCode Easy/Medium problems covering each core data structure.",
    },
    "Object-Oriented Programming": {
        "priority": "HIGH",
        "topic": "OOP: Classes, Inheritance, Polymorphism, Encapsulation",
        "task": "Design a library management system using OOP principles in your preferred language.",
    },
    "REST APIs": {
        "priority": "HIGH",
        "topic": "REST API Design: Endpoints, HTTP Methods, Status Codes",
        "task": "Build a REST API for a bookstore with GET, POST, PUT, and DELETE endpoints.",
    },
    "GraphQL": {
        "priority": "LOW",
        "topic": "GraphQL Schemas, Queries, and Mutations",
        "task": "Build a simple GraphQL API for a product catalogue with nested queries.",
    },
    "Microservices": {
        "priority": "LOW",
        "topic": "Microservices Architecture and Communication",
        "task": "Split a monolithic app into two microservices that communicate via REST.",
    },
    "System Design": {
        "priority": "MEDIUM",
        "topic": "Scalability, Load Balancing, Caching, Database Sharding",
        "task": "Design a URL shortener system: draw the architecture and explain design choices.",
    },
    "Design Patterns": {
        "priority": "MEDIUM",
        "topic": "GoF Patterns: Singleton, Factory, Observer, Strategy",
        "task": "Implement three design patterns in a mini-project and explain when to use each.",
    },
    "Agile": {
        "priority": "MEDIUM",
        "topic": "Agile Methodology: Scrum Ceremonies and Kanban Boards",
        "task": "Run a two-week sprint simulation for your mini-project using a Trello Kanban board.",
    },
    "Unit Testing": {
        "priority": "MEDIUM",
        "topic": "Writing Unit Tests with pytest / JUnit",
        "task": "Write unit tests for a calculator module, achieving at least 80% code coverage.",
    },
    "DevOps": {
        "priority": "MEDIUM",
        "topic": "DevOps Principles: Automation, Monitoring, IaC",
        "task": "Set up a simple CI/CD pipeline with automated tests and deployment to a staging server.",
    },

    # --- Soft Skills ---
    "Communication Skills": {
        "priority": "HIGH",
        "topic": "Professional Communication: Emails, Presentations, Meetings",
        "task": "Prepare and deliver a 5-minute presentation about your project to peers.",
    },
    "Problem Solving": {
        "priority": "HIGH",
        "topic": "Structured Problem Solving: Break Down, Analyse, Solve",
        "task": "Solve 10 logical reasoning and coding problems on a platform like HackerRank.",
    },
    "Teamwork": {
        "priority": "HIGH",
        "topic": "Collaboration, Conflict Resolution, Shared Ownership",
        "task": "Contribute to a team project on GitHub: review at least two peers' pull requests.",
    },
    "Leadership": {
        "priority": "MEDIUM",
        "topic": "Team Leadership: Planning, Delegation, Motivation",
        "task": "Lead a small group project from planning to demo, acting as the team coordinator.",
    },
    "Time Management": {
        "priority": "MEDIUM",
        "topic": "Time Boxing, Prioritisation, and Productivity Tools",
        "task": "Track your study hours for one week using a time-tracking app and review patterns.",
    },
    "Documentation": {
        "priority": "MEDIUM",
        "topic": "Technical Writing: README, API Docs, Code Comments",
        "task": "Write a complete README and inline documentation for one of your existing projects.",
    },

    # --- Miscellaneous ---
    "UI/UX Design": {
        "priority": "LOW",
        "topic": "UX Principles, Wireframing with Figma",
        "task": "Create a low-fidelity wireframe for a mobile app in Figma and gather feedback.",
    },
    "Project Management": {
        "priority": "LOW",
        "topic": "Project Planning, Milestones, and Risk Management",
        "task": "Define scope, timeline, and risks for a personal project using a simple PM template.",
    },
    "Cybersecurity": {
        "priority": "MEDIUM",
        "topic": "Web Security Basics: OWASP Top 10",
        "task": "Audit a sample web app for OWASP Top 10 vulnerabilities and document findings.",
    },
}

# Default metadata for skills not explicitly listed above
DEFAULT_METADATA = {
    "priority": "MEDIUM",
    "topic": "Explore foundational concepts and official documentation",
    "task": "Build a small project that uses this skill and document your learning.",
}

# Priority ordering for sorting
PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def generate_roadmap(missing_skills: list, target_role: str = "") -> list:
    """
    Generate a learning roadmap from the list of missing skills.

    Parameters
    ----------
    missing_skills : list of canonical skill names the student is missing
    target_role    : optional role name for context (not currently used in logic)

    Returns
    -------
    List of dicts, each containing:
        skill     - skill name
        priority  - HIGH / MEDIUM / LOW
        topic     - suggested learning topic
        task      - practical mini-task description
        done      - bool (False by default; managed via session_state in app.py)
    """
    roadmap = []

    for skill in missing_skills:
        meta = SKILL_METADATA.get(skill, DEFAULT_METADATA)
        roadmap.append({
            "skill": skill,
            "priority": meta["priority"],
            "topic": meta["topic"],
            "task": meta["task"],
            "done": False,
        })

    # Sort by priority (HIGH first), then alphabetically within each group
    roadmap.sort(key=lambda x: (PRIORITY_ORDER.get(x["priority"], 99), x["skill"]))

    return roadmap


def roadmap_to_report_lines(roadmap: list) -> list:
    """
    Convert roadmap data to a list of plain-text lines for the report.
    """
    lines = []
    lines.append("--- Learning Roadmap ---")
    if not roadmap:
        lines.append("  No missing skills — nothing to learn for this role!")
        return lines

    current_priority = None
    for item in roadmap:
        if item["priority"] != current_priority:
            current_priority = item["priority"]
            lines.append(f"\n  [{current_priority} PRIORITY]")
        status = "✓ Done" if item.get("done") else "☐ To Do"
        lines.append(f"    {status}  {item['skill']}")
        lines.append(f"           Topic : {item['topic']}")
        lines.append(f"           Task  : {item['task']}")

    return lines


def get_priority_counts(roadmap: list) -> dict:
    """Return count of items per priority level."""
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for item in roadmap:
        p = item.get("priority", "MEDIUM")
        counts[p] = counts.get(p, 0) + 1
    return counts
