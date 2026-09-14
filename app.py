import streamlit as st

from reviewer import review_code
from github_utils import get_repository_files
from utils import detect_language


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🔍 AI-Powered Code Review Assistant")

st.write(
    "Analyze source code with AI to identify potential bugs, "
    "security issues, performance concerns, and code-quality problems."
)

st.divider()


# --------------------------------------------------
# Code input method
# --------------------------------------------------

input_method = st.radio(
    "Choose how you want to provide your code:",
    [
        "Upload a file",
        "Paste code",
        "GitHub Repository"
    ],
    horizontal=True
)

code = ""
filename = "Pasted Code"


# --------------------------------------------------
# Upload file
# --------------------------------------------------

if input_method == "Upload a file":

    uploaded_file = st.file_uploader(
        "Upload a source code file",
        type=[
            "py",
            "js",
            "jsx",
            "ts",
            "tsx",
            "java",
            "cpp",
            "c",
            "cs",
            "php",
            "go"
        ]
    )

    if uploaded_file:

        filename = uploaded_file.name

        try:

            code = uploaded_file.read().decode("utf-8")

        except UnicodeDecodeError:

            st.error(
                "Unable to read this file. "
                "Please upload a UTF-8 text source file."
            )


# --------------------------------------------------
# Paste code
# --------------------------------------------------

elif input_method == "Paste code":

    code = st.text_area(
        "Paste your source code here:",
        height=400,
        placeholder="Paste your code here..."
    )


# --------------------------------------------------
# GitHub Repository
# --------------------------------------------------

else:

    st.write(
        "Enter the URL of a **public GitHub repository**."
    )

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repository"
    )

    if repo_url:

        if st.button("📥 Load Repository"):

            with st.spinner("Downloading repository..."):

                try:

                    github_files = get_repository_files(repo_url)

                    if not github_files:

                        st.warning(
                            "No supported source-code files were found."
                        )

                        st.stop()

                    st.session_state["github_files"] = github_files

                    st.success(
                        f"Found {len(github_files)} source files."
                    )

                except Exception as e:

                    st.error(
                        f"Unable to load repository: {e}"
                    )

                    st.stop()


    # --------------------------------------------------
    # File selection
    # --------------------------------------------------

    if "github_files" in st.session_state:

        github_files = st.session_state["github_files"]

        selected_file = st.selectbox(
            "Select a file to review:",
            range(len(github_files)),
            format_func=lambda index: github_files[index]["name"]
        )

        selected_data = github_files[selected_file]

        filename = selected_data["name"]

        code = selected_data["code"]

        st.info(
            f"Selected file: `{filename}`"
        )


# --------------------------------------------------
# Detect programming language
# --------------------------------------------------

language = detect_language(filename)


# --------------------------------------------------
# Analyze button
# --------------------------------------------------

st.divider()

analyze = st.button(
    "🔎 Analyze Code",
    type="primary",
    use_container_width=True
)


if analyze:

    if not code.strip():

        st.warning(
            "Please upload a file, paste some source code, "
            "or select a GitHub file first."
        )

        st.stop()


    # --------------------------------------------------
    # Run AI review
    # --------------------------------------------------

    with st.spinner("Gemini is reviewing your code..."):

        try:

            review = review_code(code)

        except Exception as e:

            st.error(
                f"An error occurred while reviewing the code: {e}"
            )

            st.stop()


    st.success("Code review completed!")


    # --------------------------------------------------
    # Review header
    # --------------------------------------------------

    st.subheader("📊 Review Overview")

    st.caption(f"Reviewed file: `{filename}`")

    st.caption(f"Detected language: `{language}`")


    # --------------------------------------------------
    # Calculate severity counts
    # --------------------------------------------------

    critical_count = sum(
        1
        for finding in review.findings
        if finding.severity.lower() == "critical"
    )

    high_count = sum(
        1
        for finding in review.findings
        if finding.severity.lower() == "high"
    )

    medium_count = sum(
        1
        for finding in review.findings
        if finding.severity.lower() == "medium"
    )

    low_count = sum(
        1
        for finding in review.findings
        if finding.severity.lower() == "low"
    )


    # --------------------------------------------------
    # Severity dashboard
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🔴 Critical",
            critical_count
        )

    with col2:

        st.metric(
            "🟠 High",
            high_count
        )

    with col3:

        st.metric(
            "🟡 Medium",
            medium_count
        )

    with col4:

        st.metric(
            "🟢 Low",
            low_count
        )


    st.divider()


    # --------------------------------------------------
    # Overall summary
    # --------------------------------------------------

    st.subheader("📋 Overall Summary")

    st.info(review.summary)


    # --------------------------------------------------
    # Findings
    # --------------------------------------------------

    st.subheader(
        f"🔎 Findings ({len(review.findings)})"
    )


    if not review.findings:

        st.success(
            "No significant issues were identified."
        )

    else:

        for finding in review.findings:

            severity = finding.severity.lower()

            if severity == "critical":

                icon = "🔴"

            elif severity == "high":

                icon = "🟠"

            elif severity == "medium":

                icon = "🟡"

            else:

                icon = "🟢"


            with st.expander(
                f"{icon} {finding.title} — {finding.severity}"
            ):

                st.write(
                    f"**Category:** {finding.category}"
                )

                st.write(
                    f"**Severity:** {finding.severity}"
                )

                st.write(
                    f"**Description:** {finding.description}"
                )

                st.write(
                    f"**Suggested Improvement:** "
                    f"{finding.suggestion}"
                )


    # --------------------------------------------------
    # Suggested improved code
    # --------------------------------------------------

    st.divider()

    st.subheader("✨ Suggested Improved Code")

    st.write(
        "Gemini-generated version with the identified issues addressed."
    )

    st.code(
        review.improved_code,
        language=language
    )


    # --------------------------------------------------
    # Original source code
    # --------------------------------------------------

    st.divider()

    st.subheader("💻 Original Source Code")

    with st.expander("View original code"):

        st.code(
            code,
            language=language
        )
