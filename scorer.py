def final_score(metrics: dict, project_flags: list, readme_flags: list, test_count: int) -> dict:
    score = 50.0

    # Code quality
    score += metrics.get("pylint_score", 0) * 5 / 10
    # Project structure
    if "Missing src/lib folder" not in project_flags:
        score += 10
    # README
    if not readme_flags:
        score += 10
    # Tests
    if test_count > 0:
        score += 10
    # Cap
    score = min(score, 100)
    # Level
    if score >= 85:
        level = "Advanced"
    elif score >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"
    return {"score": score, "level": level}
