import os
import shutil
import tempfile
import subprocess
import json
from git import Repo
from pathlib import Path
from radon.complexity import cc_visit
from mentor import generate_summary, generate_roadmap
from scorer import final_score

def fetch_and_clone_repo(repo_url: str) -> str:
    temp_dir = tempfile.gettempdir()
    repo_name = repo_url.rstrip('/').split('/')[-1]
    local_path = os.path.join(temp_dir, f"repo_{repo_name}")
    if os.path.exists(local_path):
        try:
            shutil.rmtree(local_path)
        except Exception as e:
            raise RuntimeError(f"Failed to remove existing folder. Please close any programs using it. {e}")
    try:
        print(f"Cloning repository into {local_path}...")
        Repo.clone_from(repo_url, local_path)
    except Exception as e:
        raise RuntimeError(f"Failed to clone repository: {e}")
    return local_path

def get_repo_metadata(repo_path: str, repo_name: str):
    python_files = list(Path(repo_path).rglob("*.py"))
    return {
        "repo_name": repo_name,
        "python_files_count": len(python_files),
        "files_count": sum(1 for _ in Path(repo_path).rglob("*") if _.is_file()),
        "folders_count": sum(1 for _ in Path(repo_path).rglob("*") if _.is_dir())
    }

def analyze_python_code(repo_path: str):
    python_files = list(Path(repo_path).rglob("*.py"))
    cc_results = {}
    for f in python_files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                code = file.read()
            cc_results[str(f)] = cc_visit(code)
        except Exception:
            continue
    # Lint score using subprocess pylint
    pylint_score = 0
    for f in python_files:
        try:
            result = subprocess.run(
                ["pylint", f"--score=y", "--disable=R,C"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.splitlines():
                if line.strip().startswith("Your code has been rated at"):
                    pylint_score += float(line.strip().split(" ")[6].split("/")[0])
        except Exception:
            continue
    pylint_score = pylint_score / max(1, len(python_files))
    return {"cyclomatic_complexity": cc_results, "pylint_score": pylint_score}

def detect_project_flags(repo_path: str):
    root_files = list(Path(repo_path).glob("*"))
    flags = []
    if not any(f.is_dir() and f.name.lower() in ["src", "lib"] for f in root_files):
        flags.append("Missing src/lib folder")
    if sum(f.is_file() for f in root_files) > 20:
        flags.append("Too many files in root")
    if any(f.is_file() and f.suffix not in [".py", ".md", ".txt", ".json"] for f in root_files):
        flags.append("Mixed file types in root")
    return flags

def detect_readme_flags(repo_path: str):
    readme_path = Path(repo_path) / "README.md"
    flags = []
    if not readme_path.exists():
        flags.append("README missing")
    else:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "installation" not in content.lower():
            flags.append("Missing Installation section")
        if "usage" not in content.lower():
            flags.append("Missing Usage section")
        if "contributing" not in content.lower():
            flags.append("Missing Contributing section")
    return flags

def detect_test_count(repo_path: str):
    test_files = list(Path(repo_path).rglob("test_*.py"))
    return len(test_files)

def detect_dependencies(repo_path: str):
    deps = []
    if (Path(repo_path) / "requirements.txt").exists():
        deps.append("requirements.txt")
    if (Path(repo_path) / "package.json").exists():
        deps.append("package.json")
    if (Path(repo_path) / "poetry.lock").exists():
        deps.append("poetry.lock")
    return deps

def save_report(report: dict, filename="analysis_report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
