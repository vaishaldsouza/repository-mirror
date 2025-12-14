# Generate summary and roadmap based on repo evaluation

def generate_summary(score, metrics, flags):
    summary = []
    if score >= 80:
        summary.append("Excellent project depth and clean codebase.")
    elif score >= 50:
        summary.append("Strong code consistency; some improvements needed.")
    else:
        summary.append("Basic project structure but poor documentation and inconsistent commits.")
    return " ".join(summary)

def generate_roadmap(metrics, flags):
    roadmap = []
    if not flags.get("has_tests"):
        roadmap.append("Add unit tests")
    if not flags.get("has_readme"):
        roadmap.append("Add README with project instructions")
    if not flags.get("has_ci"):
        roadmap.append("Introduce CI/CD using GitHub Actions")
    if metrics.get("avg_complexity", 0) > 10:
        roadmap.append("Refactor complex functions for readability")
    return roadmap
