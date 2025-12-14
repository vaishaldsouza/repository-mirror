# Convert repo metrics into a score and level

def final_score(metrics, metadata, flags):
    score = 0

    # Python code metrics
    score += metrics.get("pylint_score", 0) * 5  # scale 0-10 -> 0-50
    score += max(0, 50 - metrics.get("avg_complexity", 0))  # lower complexity = higher score

    # Repo flags
    if flags.get("has_readme"):
        score += 10
    if flags.get("has_tests"):
        score += 10
    if flags.get("has_ci"):
        score += 10

    score = min(100, int(score))

    # Determine level
    if score >= 80:
        level = "Advanced"
    elif score >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    return {"score": score, "level": level}
