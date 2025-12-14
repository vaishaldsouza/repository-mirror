import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from git import Repo
from scorer import final_score
from mentor import generate_summary, generate_roadmap

# ---------------------------
# Repo Fetch & Clone
# ---------------------------
def fetch_and_clone_repo(repo_url):
    temp_dir = tempfile.mkdtemp(prefix="repo_")
    try:
        print(f"Cloning repository into {temp_dir}...")
        Repo.clone_from(repo_url, temp_dir)
        print("Cloning successful.")
        return temp_dir
    except Exception as e:
        print("Failed to clone repository or repository not accessible:", e)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None

# ---------------------------
# Repo Metadata
# ---------------------------
def get_repo_metadata(repo_path, repo_name):
    metadata = {}
    metadata["repo_name"] = repo_name
    metadata["total_files"] = sum([len(files) for _, _, files in os.walk(repo_path)])
    metadata["total_folders"] = sum([len(dirs) for _, dirs, _ in os.walk(repo_path)])
    return metadata

# ---------------------------
# Python Code Analysis
# ---------------------------
def analyze_python_code(repo_path):
    python_files_count = 0
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                python_files_count += 1
    metrics = {
        "python_files_count": python_files_count
    }
    return metrics

# ---------------------------
# Detect README
# ---------------------------
def detect_readme_flags(repo_path):
    readme_files = [f for f in os.listdir(repo_path) if f.lower().startswith("readme")]
    return {"readme_present": bool(readme_files)}

# ---------------------------
# Detect Project Flags
# ---------------------------
def detect_project_flags(repo_path):
    flags = []
    if not os.path.exists(os.path.join(repo_path, "src")):
        flags.append("Missing src folder")
    if not os.path.exists(os.path.join(repo_path, "tests")):
        flags.append("Missing tests folder")
    return flags

# ---------------------------
# Detect Test Count
# ---------------------------
def detect_test_count(repo_path):
    test_count = 0
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_count += 1
    return test_count

# ---------------------------
# Run Pylint (Python Code Quality)
# ---------------------------
def run_pylint(file_path):
    try:
        result = subprocess.run(["pylint", file_path, "--disable=all", "--enable=E,F,W,C,R"], capture_output=True, text=True)
        score = 50  # Placeholder
        return score
    except Exception:
        return 0

# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    print("Repository Mirror Analyzer")
    choice = input("Analyze (1) GitHub URL or (2) Local folder? Enter 1 or 2: ").strip()

    repo_path = None
    repo_name = ""

    if choice == "1":
        repo_url = input("Enter GitHub repository URL: ").strip()
        repo_name = repo_url.split("/")[-1]
        repo_path = fetch_and_clone_repo(repo_url)
    elif choice == "2":
        repo_path = input("Enter local folder path: ").strip()
        repo_name = os.path.basename(os.path.abspath(repo_path))
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    if not repo_path:
        print("Repository not available. Exiting.")
        exit(1)

    metadata = get_repo_metadata(repo_path, repo_name)
    metrics = analyze_python_code(repo_path)
    readme_flags = detect_readme_flags(repo_path)
    flags = detect_project_flags(repo_path)
    test_count = detect_test_count(repo_path)

    score_data = final_score(metrics, readme_flags, test_count)
    summary = generate_summary(score_data["score"], metrics, flags, readme_flags, test_count)
    roadmap = generate_roadmap(score_data["score"], metrics, flags)

    print("\nScore & Level")
    print(f"Score: {score_data['score']} / 100")
    print(f"Level: {score_data['level']}\n")
    print("Summary")
    print(summary)
    print("\nPersonalized Roadmap")
    for r in roadmap:
        print(f"- {r}")

    # Cleanup temp repo if cloned
    if choice == "1" and repo_path:
        try:
            shutil.rmtree(repo_path, ignore_errors=True)
        except Exception:
            pass
