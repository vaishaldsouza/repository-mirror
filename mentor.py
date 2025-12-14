def generate_summary(score: float, project_flags: list, readme_flags: list, test_count: int):
    summary = []
    if not readme_flags:
        summary.append("README present.")
    else:
        summary.append("README missing or incomplete.")
    if test_count == 0:
        summary.append("Add unit tests for reliability.")
    if project_flags:
        summary.append("Introduce CI/CD pipelines for automation.")
    return " ".join(summary)

def generate_roadmap(score: float, project_flags: list, readme_flags: list, test_count: int):
    roadmap = []
    if test_count == 0:
        roadmap.append("Add unit tests and integration tests.")
    if "Missing src/lib folder" in project_flags:
        roadmap.append("Refactor project structure: move source code to src/ and organize tests.")
    if "README missing" in readme_flags or readme_flags:
        roadmap.append("Update README with Installation, Usage, and Contributing sections.")
    roadmap.append("Set up CI/CD using GitHub Actions or similar.")
    return roadmap
