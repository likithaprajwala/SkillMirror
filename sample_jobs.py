"""
sample_jobs.py
--------------
Contains four built-in sample job descriptions.
Each entry maps a role name to a realistic job description text.

To add more samples: add a new key-value pair to SAMPLE_JOB_DESCRIPTIONS.
"""

SAMPLE_JOB_DESCRIPTIONS = {
    "Python Developer": """
We are looking for a Python Developer to join our growing engineering team.

Responsibilities:
- Develop and maintain backend services using Python and Flask or Django.
- Write clean, reusable, and well-documented Python code.
- Design and interact with SQL and PostgreSQL databases.
- Build and consume REST APIs.
- Work with Git and GitHub for version control and code reviews.
- Collaborate in an Agile/Scrum team environment.
- Write unit tests using pytest to ensure code quality.
- Deploy applications using Docker containers.
- Optionally work with AWS services such as EC2 and S3.

Requirements:
- Strong proficiency in Python.
- Experience with Flask or Django web frameworks.
- Solid understanding of SQL and relational databases (MySQL or PostgreSQL).
- Knowledge of REST API design and development.
- Familiarity with Git and GitHub.
- Understanding of Object-Oriented Programming (OOP) principles.
- Knowledge of Linux command-line environments.
- Good communication skills and teamwork.
- Problem-solving mindset.

Nice to have:
- Experience with Docker and containerisation.
- Familiarity with CI/CD pipelines and GitHub Actions.
- Knowledge of Pandas and NumPy for data tasks.
""",

    "Java Developer": """
We are hiring a Java Developer to build enterprise-grade applications.

Responsibilities:
- Design and develop scalable backend systems using Java and Spring Boot.
- Build and expose RESTful APIs consumed by frontend and mobile clients.
- Write SQL queries and manage relational databases (MySQL or PostgreSQL).
- Apply Object-Oriented Programming principles and Design Patterns.
- Use Git and GitHub for version control and team collaboration.
- Work in Agile sprints with daily stand-ups and sprint reviews.
- Write unit tests using JUnit and maintain high test coverage.
- Participate in code reviews and maintain documentation.

Requirements:
- Strong knowledge of Core Java and Java SE.
- Experience with Spring Boot and Spring Framework.
- Proficiency in SQL and MySQL or PostgreSQL.
- Understanding of REST APIs and HTTP protocols.
- Familiarity with Git and GitHub.
- Good understanding of OOP and design patterns such as Singleton and Factory.
- Ability to work in Linux/Unix environments.
- Strong communication skills and problem-solving abilities.

Nice to have:
- Experience with Docker and containerisation.
- Knowledge of Microservices architecture.
- Familiarity with Agile/Scrum methodology.
- Understanding of CI/CD pipelines.
""",

    "Data Analyst": """
We are looking for a Data Analyst to turn raw data into actionable insights.

Responsibilities:
- Collect, clean, and analyse large datasets using Python and Pandas.
- Write complex SQL queries to extract data from relational databases.
- Create clear, insightful data visualisations using Matplotlib, Seaborn, or Tableau.
- Build interactive dashboards in Power BI or Tableau for business stakeholders.
- Apply statistical analysis techniques to identify trends and patterns.
- Use Excel for ad-hoc reporting and data manipulation.
- Collaborate with cross-functional teams to define metrics and KPIs.
- Document analysis processes and present findings to non-technical audiences.

Requirements:
- Proficiency in Python with Pandas and NumPy for data analysis.
- Strong SQL skills including joins, subqueries, and aggregations.
- Experience with data visualisation tools: Matplotlib, Seaborn, Tableau, or Power BI.
- Understanding of statistics and basic probability.
- Familiarity with Excel for data manipulation.
- Good communication skills and presentation skills.
- Attention to detail and problem-solving approach.

Nice to have:
- Experience with Jupyter Notebook for exploratory data analysis.
- Familiarity with machine learning concepts.
- Knowledge of ETL pipelines and data warehousing.
- Experience with Apache Spark or big data tools.
""",

    "Machine Learning Intern": """
We are offering a Machine Learning Internship for students passionate about AI.

Responsibilities:
- Assist in building and evaluating machine learning models using Python and scikit-learn.
- Preprocess and clean datasets using Pandas and NumPy.
- Implement supervised and unsupervised learning algorithms.
- Conduct exploratory data analysis using Jupyter Notebook.
- Visualise model performance and data distributions using Matplotlib and Seaborn.
- Learn and apply natural language processing (NLP) techniques.
- Use Git and GitHub for version control.
- Document experiments, findings, and model results clearly.

Requirements:
- Basic proficiency in Python.
- Familiarity with machine learning concepts and algorithms.
- Knowledge of Pandas and NumPy for data manipulation.
- Understanding of scikit-learn for model building.
- Exposure to deep learning concepts (TensorFlow or PyTorch is a plus).
- Basic knowledge of statistics and data analysis.
- Experience with Jupyter Notebook.
- Good communication skills, teamwork, and problem-solving abilities.
- Understanding of data visualisation using Matplotlib or Seaborn.

Nice to have:
- Exposure to NLP techniques and text preprocessing.
- Knowledge of Computer Vision concepts.
- Familiarity with deep learning frameworks (TensorFlow, PyTorch, Keras).
- Understanding of Git and GitHub workflows.
""",
}


def get_sample_names() -> list:
    """Return the list of available sample job names."""
    return list(SAMPLE_JOB_DESCRIPTIONS.keys())


def get_sample_description(name: str) -> str:
    """
    Return the job description text for the given sample name.
    Returns an empty string if the name is not found.
    """
    return SAMPLE_JOB_DESCRIPTIONS.get(name, "")
