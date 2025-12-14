# analyzer.py
import os
import shutil
import json
import requests
from git import Repo
from radon.complexity import cc_visit
from pylint.lint import Run
from io import StringIO
from contextlib import redirect_stdout
from scorer import final_score
from mentor import generate_summary, generate_roadmap

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_and_clone_repo(repo_url: str, local_path: str = "temp_repo") -> str | None:
    if os.path.exists(local_path):
        try:
            shutil.rmtree(local_path, ignore_errors=True)
        except Exception:
            pass
    try:
        Repo.clone_from(repo_url, local_path)
        return local_path
    except Exception as e:
        print(f"Clone failed: {e}")
        return None


def get_repo_metadata(owner: str, repo_name: str) -> dict:
    metadata = {}
    if not GITHUB_TOKEN:
        return metadata
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        repo_res = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers, timeout=10)
        lang_res = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/languages", headers=headers, timeout=10)
        commits_res = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/commits", headers=headers, timeout=10)
        if repo_res.status_code == 200:
            data = repo_res.json()
            metadata["description"] = data.get("description", "")
            metadata["stars"] = data.get("stargazers_count", 0)
            metadata["forks"] = data.get("forks_count", 0)
            metadata["open_issues"] = data.get("open_issues_count", 0)
        if lang_res.status_code == 200:
            metadata["languages"] = lang_res.json()
        if commits_res.status_code == 200:
            metadata["commit_count"] = len(commits_res.json())
    except requests.RequestException:
        pass
    return metadata


def analyze_python_code_metrics(repo_path: str) -> dict:
    results = {"python_files_count": 0, "avg_complexity": 0.0, "pylint_score": 0.0, "complexity_hotspots": []}
    python_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    results["python_files_count"] = len(python_files)
    if not python_files:
        return results

    total_complexity = 0
    total_blocks = 0
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            blocks = cc_visit(code)
            for block in blocks:
                total_complexity += block.complexity
                total_blocks += 1
                if block.complexity > 10:
                    results["complexity_hotspots"].append({"file": file_path, "name": block.name, "complexity": block.complexity})
        except Exception:
            continue
    if total_blocks > 0:
        results["avg_complexity"] = round(total_complexity / total_blocks, 2)

    pylint_buffer = StringIO()
    with redirect_stdout(pylint_buffer):
        Run(python_files + ["--score=y"], exit=False)
    pylint_output = pylint_buffer.getvalue()
    for line in pylint_output.splitlines():
        if "Your code has been rated at" in line:
            try:
                score = line.split("rated at ")[1].split("/")[0]
                results["pylint_score"] = round(float(score), 2)
            except ValueError:
                pass
    return results


def detect_project_flags(repo_path: str) -> dict:
    items = os.listdir(repo_path)
    has_readme = any(i.lower() == "readme.md" for i in items)
    has_tests = any("test" in i.lower() for i in items)
    has_ci = os.path.exists(os.path.join(repo_path, ".github", "workflows"))
    has_requirements = os.path.exists(os.path.join(repo_path, "requirements.txt"))
    return {"has_readme": has_readme, "has_tests": has_tests, "has_ci": has_ci, "has_requirements": has_requirements}


def analyze_folder_structure(repo_path: str) -> dict:
    root_files = os.listdir(repo_path)
    issues = []
    if len([f for f in root_files if f.endswith(".py")]) > 5:
        issues.append("Many Python files in root; consider creating src/ folder.")
    if not any(d in root_files for d in ["src", "lib"]):
        issues.append("Missing src/ or lib/ folder; consider organizing source code.")
    if any(f for f in root_files if f.endswith((".md", ".py", ".json"))):
        issues.append("Root folder contains mixed file types; consider organizing docs, code, and configs.")
    return {"folder_issues": issues}


def analyze_readme(repo_path: str) -> dict:
    readme_path = os.path.join(repo_path, "README.md")
    result = {"sections": 0, "has_installation": False, "has_usage": False, "has_contributing": False}
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()
        result["sections"] = content.count("#")
        result["has_installation"] = "installation" in content
        result["has_usage"] = "usage" in content
        result["has_contributing"] = "contributing" in content
    return result


def detect_tests(repo_path: str) -> int:
    test_count = 0
    for root, _, files in os.walk(repo_path):
        for file in files:
            if "test" in file.lower() and file.endswith(".py"):
                test_count += 1
    return test_count


if __name__ == "__main__":
    print("Repository Mirror Analyzer")
    choice = input("Analyze (1) GitHub URL or (2) Local folder? Enter 1 or 2: ").strip()
    if choice == "1":
        repo_url = input("Enter GitHub repository URL: ").strip()
        parts = repo_url.strip("/").split("/")
        owner, repo_name = parts[-2], parts[-1]
        temp_dir = "temp_repo"
        repo_path = fetch_and_clone_repo(repo_url, temp_dir)
    elif choice == "2":
        repo_path = input("Enter local repository path: ").strip()
        owner, repo_name = "local", os.path.basename(repo_path)
    else:
        print("Invalid choice"); exit()

    if repo_path:
        metadata = get_repo_metadata(owner, repo_name)
        metrics = analyze_python_code_metrics(repo_path)
        flags = detect_project_flags(repo_path)
        folder_analysis = analyze_folder_structure(repo_path)
        readme_analysis = analyze_readme(repo_path)
        tests_count = detect_tests(repo_path)
        if tests_count > 0:
            flags["has_tests"] = True

        score_data = final_score(metrics, metadata, flags, folder_analysis, readme_analysis, tests_count)
        summary = generate_summary(score_data["score"], metrics, flags, folder_analysis, readme_analysis, tests_count)
        roadmap = generate_roadmap(metrics, flags, folder_analysis, readme_analysis, tests_count)

        print(f"\nScore: {score_data['score']} / 100")
        print(f"Level: {score_data['level']}")
        print("Summary:")
        print(summary)
        print("Roadmap:")
        for step in roadmap:
            print(f"- {step}")

        # Save report
        report = {
            "score": score_data["score"],
            "level": score_data["level"],
            "summary": summary,
            "roadmap": roadmap,
            "metrics": metrics,
            "flags": flags,
            "folder_analysis": folder_analysis,
            "readme_analysis": readme_analysis
        }
        with open("analysis_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        try:
            shutil.rmtree(repo_path, ignore_errors=True)
        except Exception:
            pass
