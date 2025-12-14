# mentor.py

def generate_summary(score, metrics, flags, folder_analysis=None, readme_analysis=None, tests_count=0):
    """Generate human-readable summary"""
    summary = []
    if score >= 85:
        summary.append("Excellent project structure and code quality.")
    elif score >= 50:
        summary.append("Strong code consistency; some improvements needed.")
    else:
        summary.append("Basic project structure; significant improvements required.")

    if folder_analysis and folder_analysis.get("folder_issues"):
        summary.append("Folder structure can be improved: " + "; ".join(folder_analysis["folder_issues"]))

    if readme_analysis:
        missing_sections = []
        if not readme_analysis.get("has_installation"):
            missing_sections.append("Installation instructions")
        if not readme_analysis.get("has_usage"):
            missing_sections.append("Usage examples")
        if not readme_analysis.get("has_contributing"):
            missing_sections.append("Contributing guide")
        if missing_sections:
            summary.append("Improve README: add " + ", ".join(missing_sections))

    if tests_count == 0:
        summary.append("Add unit tests for reliability.")

    if not flags.get("has_ci"):
        summary.append("Introduce CI/CD workflows.")

    if metrics.get("complexity_hotspots"):
        hotspots = ", ".join([f"{h['name']}({h['complexity']})" for h in metrics["complexity_hotspots"]])
        summary.append(f"Refactor complex functions: {hotspots}")

    return " ".join(summary)


def generate_roadmap(metrics, flags, folder_analysis=None, readme_analysis=None, tests_count=0):
    """Generate stepwise roadmap for improvement"""
    roadmap = []

    # Project structure
    if folder_analysis and folder_analysis.get("folder_issues"):
        roadmap.append("Refactor project structure: move source code to src/ and organize tests.")

    # Documentation
    if readme_analysis:
        missing = []
        if not readme_analysis.get("has_installation"):
            missing.append("Installation instructions")
        if not readme_analysis.get("has_usage"):
            missing.append("Usage examples")
        if not readme_analysis.get("has_contributing"):
            missing.append("Contributing guide")
        if missing:
            roadmap.append("Update README: add " + ", ".join(missing))

    # Tests
    if tests_count == 0:
        roadmap.append("Add unit tests and integration tests.")

    # CI/CD
    if not flags.get("has_ci"):
        roadmap.append("Introduce CI/CD using GitHub Actions or similar.")

    # Code quality
    if metrics.get("pylint_score", 0) < 8:
        roadmap.append("Improve code quality based on Pylint suggestions.")

    # Complexity hotspots
    if metrics.get("complexity_hotspots"):
        roadmap.append("Refactor high-complexity functions (complexity > 10) for maintainability.")

    return roadmap
