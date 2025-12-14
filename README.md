#  Repository Mirror Analyzer

Repository Mirror Analyzer is a Python + Streamlit tool that evaluates a GitHub repository or local project folder and provides:

* A **project quality score**
* **Skill level classification** (Beginner / Intermediate / Advanced)
* A **human-readable summary**
* A **personalized improvement roadmap**

This tool is designed for students, developers, and mentors to quickly assess project readiness and best practices.

---

##  Features

* Analyze **GitHub repositories** via URL
* Analyze **local project folders**
* Detect:

  * README presence
  * Project structure quality
  * Test coverage (basic detection)
* Generate:

  * Numerical score (0–100)
  * Skill level
  * Actionable feedback
* Streamlit-based **web UI**
* CLI support via `analyzer.py`

---

##  Tech Stack

* Python 3.9+
* Streamlit
* Git (for repository cloning)
* Standard Python libraries (os, subprocess, tempfile)

---

##  Project Structure

```
repository-mirror/
│
├── analyzer.py        # Core analysis logic
├── scorer.py          # Scoring algorithm
├── mentor.py          # Summary & roadmap generator
├── web_app.py         # Streamlit web interface
├── requirements.txt  # Python dependencies
└── README.md
```

---

##  Setup Instructions (Windows)

### 1️⃣ Create Virtual Environment

```powershell
py -m venv venv
```

### 2️⃣ Activate Virtual Environment

```powershell
venv\Scripts\Activate.ps1
```

> If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

### 3️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### 🔹 Streamlit Web App

```powershell
streamlit run web_app.py
```

Then open:

```
http://localhost:8501
```

---

### 🔹 Command Line (CLI)

```powershell
py analyzer.py
```

Follow the prompts to analyze a GitHub repository.

---

Live Demo: https://repository-mirror-lxpcfgfmpw36wca3fgqcuj.streamlit.app

##  Sample Output

```
Score: 50 / 100
Level: Intermediate

Summary:
README missing or incomplete.
Add unit tests for reliability.
Introduce CI/CD pipelines.

Personalized Roadmap:
- Add unit tests and integration tests
- Improve project structure
- Update README documentation
- Set up CI/CD automation
```

---

##  Use Cases

* Portfolio evaluation
* Student project assessment
* Hackathon submissions
* Internship readiness checks
* Self-improvement guidance

---
##  Notes

* Ensure no programs are locking cloned repositories
* Close file explorers if Git clone fails on Windows
* Internet connection required for GitHub analysis

---

## 📜 License

This project is open-source and intended for educational use.

---
