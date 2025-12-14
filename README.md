# Repository Mirror

**Repository Mirror** is a Python-based tool that analyzes GitHub repositories or local projects and provides a detailed report including **score, summary, and personalized roadmap**. It evaluates code quality, documentation, project structure, testing, and development practices.

---

## Project Overview

Repository Mirror helps developers, students, and mentors assess repository quality quickly and objectively.  
The tool provides actionable recommendations to improve coding practices and project organization.

### Key Features

1. **Repository Cloning**
   - Clone any public GitHub repository locally for analysis.

2. **GitHub Metadata Extraction**
   - Retrieve repository details such as languages, stars, forks, and description.

3. **Static Code Analysis**
   - Analyze Python code using Radon (complexity) and Pylint (quality).

4. **Project Structure & Flags**
   - Detect README, test files, and CI/CD workflows.
   - Check folder structure, large files, and missing src/ directories.

5. **Scoring Engine**
   - Generates a 0–100 score.
   - Assigns a proficiency level: Beginner, Intermediate, Advanced.

6. **AI Mentor Guidance**
   - Provides a written summary of repository quality.
   - Generates a personalized roadmap with actionable steps.

---

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/repository-mirror.git
cd repository-mirror
````

2. Create a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

* Windows:

```bash
venv\Scripts\activate
```

* Linux/Mac:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the analyzer:

```bash
python analyzer.py
```

---

## Example Usage

Analyze a GitHub repository:

```
Analyze (1) GitHub URL or (2) Local folder? Enter 1 or 2: 1
Enter GitHub repository URL: https://github.com/vaishaldsouza/TechTide-Storefront

Score: 55 / 100
Level: Intermediate
Summary:
Strong code consistency; some improvements needed. Add unit tests for reliability. Introduce CI/CD workflows.
Roadmap:
- Add unit tests and integration tests
- Introduce CI/CD using GitHub Actions
- Improve code quality based on Pylint suggestions
```

---

## Project Structure

```
repository-mirror/
│
├── analyzer.py        # Main script for repository analysis
├── scorer.py          # Converts metrics into score and level
├── mentor.py          # Generates summary and personalized roadmap
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## Approach

1. **Repository Cloning** – Clones the GitHub repository or analyzes a local folder.
2. **Metadata Retrieval** – Fetches repository details using GitHub API.
3. **Static Code Analysis** – Measures complexity and quality of Python files.
4. **Project Structure & Flags** – Detects README, tests, CI/CD workflows, folder structure.
5. **Scoring Engine** – Combines all metrics into a numerical score and proficiency level.
6. **AI Mentor Guidance** – Generates a written summary and roadmap with improvement suggestions.

---
Do you want me to do that next?
```
