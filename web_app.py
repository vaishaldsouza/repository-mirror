# web_app.py
import os;
import streamlit as st
from analyzer import (
    fetch_and_clone_repo,
    get_repo_metadata,
    analyze_python_code,
    detect_project_flags,
    detect_readme_flags,
    detect_test_count
)
from scorer import final_score
from mentor import generate_summary, generate_roadmap

st.title("Repository Mirror Analyzer")
st.write("Analyze your GitHub repository or local project folder.")

analyze_by = st.radio("Analyze by:", ("GitHub URL", "Local Folder"))

repo_path = None
repo_name = ""

if analyze_by == "GitHub URL":
    repo_url = st.text_input("Enter GitHub repository URL")
    if st.button("Analyze") and repo_url:
        repo_name = repo_url.split("/")[-1]
        repo_path = fetch_and_clone_repo(repo_url)
        if not repo_path:
            st.error("Failed to clone repository or repository not accessible.")
elif analyze_by == "Local Folder":
    repo_path = st.text_input("Enter local folder path")
    if st.button("Analyze") and repo_path:
        repo_name = repo_path.split("/")[-1]
        if not repo_path or not os.path.exists(repo_path):
            st.error("Local folder path not found.")

if repo_path and os.path.exists(repo_path):
    with st.spinner("Analyzing repository..."):
        metadata = get_repo_metadata(repo_path, repo_name)
        metrics = analyze_python_code(repo_path)
        readme_flags = detect_readme_flags(repo_path)
        flags = detect_project_flags(repo_path)
        test_count = detect_test_count(repo_path)

        score_data = final_score(metrics, readme_flags, test_count)
        summary = generate_summary(score_data["score"], metrics, flags, readme_flags, test_count)
        roadmap = generate_roadmap(score_data["score"], metrics, flags)

        st.subheader("Score & Level")
        st.write(f"Score: {score_data['score']} / 100")
        st.write(f"Level: {score_data['level']}")

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Personalized Roadmap")
        for r in roadmap:
            st.write(f"- {r}")

        # Clean up temp repo if cloned
        if analyze_by == "GitHub URL" and repo_path:
            try:
                import shutil
                shutil.rmtree(repo_path, ignore_errors=True)
            except Exception:
                pass
