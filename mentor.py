# mentor.py

def generate_summary(score, metrics, flags, readme_flags, test_count):
    """
    Generate a human-readable summary of the analysis.
    """
    summary_parts = []

    # README
    if readme_flags.get("readme_present", False):
        summary_parts.append("README present.")
    else:
        summary_parts.append("README missing or incomplete.")

    # Tests
    if test_count == 0:
        summary_parts.append("Add unit tests for reliability.")
    else:
        summary_parts.append(f"{test_count} test files detected.")

    # Project structure flags
    if flags:
        summary_parts.extend(flags)

    # Score-based advice
    if score < 50:
        summary_parts.append("Focus on code quality, tests, and project structure.")
    elif score < 85:
        summary_parts.append("Introduce CI/CD pipelines for automation.")
    else:
        summary_parts.append("Project is well-structured; consider advanced practices.")

    return " ".join(summary_parts)


def generate_roadmap(score, metrics, flags):
    """
    Generate a personalized roadmap based on score and metrics.
    """
    roadmap = []

    if score < 50:
        roadmap.append("Refactor project structure: move source code to src/ and organize tests.")
        roadmap.append("Update README with Installation, Usage, and Contributing sections.")
    if score < 85:
        roadmap.append("Add unit tests and integration tests.")
        roadmap.append("Set up CI/CD using GitHub Actions or similar.")
    if score >= 85:
        roadmap.append("Focus on performance optimization and deployment.")
        roadmap.append("Consider contributing to open source.")

    return roadmap
