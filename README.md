# Repository Mirror

**Repository Mirror** is an AI-driven system designed to analyze GitHub repositories and provide actionable insights. It evaluates repositories across multiple dimensions—including code quality, documentation, testing, and version control practices—and generates a **score, summary, and personalized improvement roadmap** for developers.

---

## Project Overview

A GitHub repository often represents a developer’s practical work. Repository Mirror helps developers, students, and mentors assess the quality of code, project structure, and development practices objectively.

### Key Features

1. **Repository Cloning**  
   - Accepts a public GitHub repository URL and clones it locally for analysis.

2. **GitHub Metadata Extraction**  
   - Retrieves repository details such as languages, stars, forks, and description via the GitHub API.

3. **Static Code Analysis (Python)**  
   - Uses **Radon** to measure cyclomatic complexity.  
   - Uses **Pylint** to assess code quality and readability.  
   - Computes average complexity and code quality scores.

4. **Project Flag Detection**  
   - Detects the presence of `README.md`, test files, and CI/CD workflows.

5. **Scoring Engine**  
   - Generates a **0–100 score** based on metrics.  
   - Assigns a proficiency level: Beginner, Intermediate, or Advanced.

6. **AI Mentor Guidance**  
   - Generates a concise **summary** highlighting strengths and weaknesses.  
   - Provides a **personalized roadmap** with actionable recommendations.

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/repository-mirror.git
cd repository-mirror
````

2. **Create a Python virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

* **Windows**

```bash
venv\Scripts\activate
```

* **Linux/Mac**

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **(Optional) Set GitHub token** to fetch repository metadata

* **Windows (PowerShell)**

```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

* **Linux/Mac**

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

6. **Run the analyzer**

```bash
python analyzer.py
```

---

## Sample Input / Output

**Input:** `https://github.com/vaishaldsouza/TechTide-Storefront`

**Output:**

```
Score: 60 / 100
Level: Intermediate
Summary:
Strong code consistency; some improvements needed.
Roadmap:
- Add unit tests
- Introduce CI/CD using GitHub Actions
```

---

## Project Structure

```
repository-mirror/
│
├── analyzer.py        # Main script for repository analysis
├── scorer.py          # Converts metrics into score and level
├── mentor.py          # Generates summary and personalized roadmap
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

---

## Approach

1. **Repository Cloning**: Clone the specified GitHub repository locally.
2. **Metadata Retrieval**: Fetch repository metadata such as languages, stars, and forks using the GitHub API.
3. **Static Code Analysis**: Analyze Python files using Radon and Pylint to compute complexity and code quality metrics.
4. **Project Flag Detection**: Detect presence of README, tests, and CI/CD workflow files.
5. **Scoring Engine**: Combine metrics and flags into a score (0–100) and assign a proficiency level.
6. **AI Mentor Guidance**: Generate a summary and roadmap with actionable improvement steps.

---

## Future Enhancements

* Support for multiple programming languages (JavaScript, HTML, CSS).
* Analysis of commit history and commit message quality.
* Detection of outdated dependencies and package management issues.
* Integration with test coverage tools to provide more detailed insights.

---

## License

This project is open-source and freely available for academic and personal use.

```
