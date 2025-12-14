# scorer.py

def final_score(metrics, readme_flags, test_count):
    """
    Calculate a simple score based on metrics, README presence, and tests.
    Returns a dict with 'score' and 'level'.
    """
    score = 0

    # Python files count
    python_count = metrics.get("python_files_count", 0)
    if python_count > 0:
        score += min(python_count * 5, 20)

    # README presence
    if readme_flags.get("readme_present", False):
        score += 20

    # Test count
    score += min(test_count * 5, 20)

    # Extra for project structure (src/tests folders)
    score += 10

    # Cap at 100
    score = min(score, 100)

    # Determine level
    if score >= 85:
        level = "Advanced"
    elif score >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    return {"score": score, "level": level}
