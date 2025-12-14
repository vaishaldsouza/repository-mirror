import streamlit as st
from analyzer import (
    fetch_and_clone_repo,
    get_repo_metadata,
    analyze_python_code,
    detect_project_flags,
    detect_readme_flags,
    detect_test_count,
    save_report
)
from scorer import final_score
from mentor import generate_summary, generate_roadmap

st.title("Repository Mirror Analyzer")
st.write("Analyze your GitHub repository or local project folder.")

mode = st.radio("Analyze by:", ("GitHub URL", "Local Folder"))

repo_path = None
repo_name = ""

if mode == "GitHub URL":
    repo_url = st.text_input("Enter GitHub repository URL")
    if st.button("Analyze") and repo_url:
        try:
            repo_path = fetch_and_clone_repo(repo_url)
            repo_name = repo_url.rstrip("/").split("/")[-1]
        except Exception as e:
            st.error(f"Failed to clone repository or repository not accessible: {e}")
elif mode == "Local Folder":
    repo_path = st.text_input("Enter local folder path")
    if st.button("Analyze") and repo_path:
        repo_name = Path(repo_path).name

if repo_path:
    metadata = get_repo_metadata(repo_path, repo_name)
    metrics = analyze_python_code(repo_path)
    project_flags = detect_project_flags(repo_path)
    readme_flags = detect_readme_flags(repo_path)
    test_count = detect_test_count(repo_path)

    score_data = final_score(metrics, project_flags, readme_flags, test_count)
    summary = generate_summary(score_data["score"], project_flags, readme_flags, test_count)
    roadmap = generate_roadmap(score_data["score"], project_flags, readme_flags, test_count)

    st.subheader("Score & Level")
    st.write(f"Score: {score_data['score']} / 100")
    st.write(f"Level: {score_data['level']}")

    st.subheader("Summary")
    st.write(summary)

    st.subheader("Personalized Roadmap")
    for item in roadmap:
        st.write(f"- {item}")

    save_report({
        "metadata": metadata,
        "metrics": metrics,
        "score_data": score_data,
        "summary": summary,
        "roadmap": roadmap
    })
