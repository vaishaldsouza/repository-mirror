import os
import shutil
import stat
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

# Clone the repository
def fetch_and_clone_repo(repo_url, local_path="temp_repo"):
    if os.path.exists(local_path):
        shutil.rmtree(local_path, onerror=remove_readonly)
    Repo.clone_from(repo_url, local_path)
    return local_path

# Get repository metadata using GitHub API
def get_repo_metadata(owner, repo_name):
    metadata = {}
    if not GITHUB_TOKEN:
        return metadata
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        repo_res = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers, timeout=10)
        lang_res = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/languages", headers=headers, timeout=10)
        if repo_res.status_code == 200:
            data = repo_res.json()
            metadata["description"] = data.get("description", "")
            metadata["stars"] = data.get("stargazers_count", 0)
            metadata["forks"] = data.get("forks_count", 0)
        if lang_res.status_code == 200:
            metadata["languages"] = lang_res.json()
    except requests.RequestException:
        pass
    return metadata

# Analyze Python code metrics using Radon and Pylint
def analyze_python_code_metrics(repo_path):
    results = {"python_files_count": 0, "avg_complexity": 0.0, "pylint_score": 0.0}
    python_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    results["python_files_count"] = len(python_files)
    if not python_files:
        return results
    total_complexity = total_blocks = 0
    for file_path in python_files:
        try:
            code = open(file_path, encoding="utf-8", errors="ignore").read()
            blocks = cc_visit(code)
            for block in blocks:
                total_complexity += block.complexity
                total_blocks += 1
        except Exception:
            continue
    if total_blocks > 0:
        results["avg_complexity"] = round(total_complexity / total_blocks, 2)
    pylint_buffer = StringIO()
    with redirect_stdout(pylint_buffer):
        Run(python_files + ["--score=y"], exit=False)
    for line in pylint_buffer.getvalue().splitlines():
        if "rated at" in line:
            try:
                results["pylint_score"] = round(float(line.split("rated at ")[1].split("/")[0]), 2)
            except ValueError:
                continue
    return results

# Detect basic project flags
def detect_project_flags(repo_path):
    items = os.listdir(repo_path)
    return {
        "has_readme": any(i.lower() == "readme.md" for i in items),
        "has_tests": any("test" in i.lower() for i in items),
        "has_ci": os.path.exists(os.path.join(repo_path, ".github", "workflows"))
    }

# Remove read-only files for Windows
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

if __name__ == "__main__":
    repo_url = "https://github.com/vaishaldsouza/TechTide-Storefront"
    temp_dir = "temp_repo"
    parts = repo_url.strip("/").split("/")
    owner, repo_name = parts[-2], parts[-1]

    repo_path = fetch_and_clone_repo(repo_url, temp_dir)
    metadata = get_repo_metadata(owner, repo_name)
    metrics = analyze_python_code_metrics(repo_path)
    flags = detect_project_flags(repo_path)

    score_data = final_score(metrics, metadata, flags)
    summary = generate_summary(score_data["score"], metrics, flags)
    roadmap = generate_roadmap(metrics, flags)

    print(f"Score: {score_data['score']} / 100")
    print(f"Level: {score_data['level']}")
    print("Summary:")
    print(summary)
    print("Roadmap:")
    for step in roadmap:
        print(f"- {step}")

    shutil.rmtree(repo_path, onerror=remove_readonly)
