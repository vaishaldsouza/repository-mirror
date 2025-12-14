# scorer.py

def normalize_score(raw_value, max_value=10):
    """Normalize a metric to 0-100"""
    return min(100, max(0, int((raw_value / max_value) * 100)))

def final_score(metrics, metadata, flags, folder_analysis=None, readme_analysis=None, tests_count=0):
    """Compute final score based on multiple metrics"""

    # Code quality
    code_quality = normalize_score(metrics.get("pylint_score", 0))
    # Maintainability
    complexity = metrics.get("avg_complexity", 0)
    maintainability = max(0, 100 - complexity * 10)

    # Project structure
    structure_score = 100
    if folder_analysis:
        issues = folder_analysis.get("folder_issues", [])
        structure_score -= len(issues) * 15

    # Documentation
    doc_score = 100
    if readme_analysis:
        if not readme_analysis.get("has_installation", False):
            doc_score -= 15
        if not readme_analysis.get("has_usage", False):
            doc_score -= 10
        if not readme_analysis.get("has_contributing", False):
            doc_score -= 10

    # Tests
    test_score = 100 if tests_count > 0 else 0

    # CI/CD
    ci_score = 100 if flags.get("has_ci") else 0

    # Commits
    commit_score = 50
    if metadata.get("commit_count", 0) > 10:
        commit_score += 25
    if metadata.get("commit_count", 0) > 50:
        commit_score += 25

    # Weighted final score
    final = int(0.25 * code_quality + 0.15 * maintainability + 0.15 * structure_score +
                0.15 * doc_score + 0.1 * test_score + 0.1 * ci_score + 0.1 * commit_score)

    # Level assignment
    if final >= 85:
        level = "Advanced"
    elif final >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    return {
        "score": final,
        "level": level,
        "breakdown": {
            "code_quality": code_quality,
            "maintainability": maintainability,
            "structure": structure_score,
            "documentation": doc_score,
            "tests": test_score,
            "ci_cd": ci_score,
            "commits": commit_score
        }
    }
