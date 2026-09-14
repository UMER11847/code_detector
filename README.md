# 🔍 AI-Powered Code Review Assistant

An AI-powered developer tool that analyzes source code using Google's Gemini LLM and provides structured feedback on potential bugs, security issues, performance concerns, and code-quality problems.

The application also supports public GitHub repositories, allowing developers to load a repository, select a source file, and receive an AI-assisted code review with suggested improvements.

## 🚀 Features

* Analyze source code using Google Gemini
* Upload source-code files or paste code directly
* Load source files from public GitHub repositories
* Select individual files from a GitHub repository
* Detect programming language automatically
* Identify potential:

  * Bugs
  * Security issues
  * Performance concerns
  * Code-quality problems
* Classify findings by severity:

  * Critical
  * High
  * Medium
  * Low
* Generate structured review results using Pydantic
* Generate an improved version of the reviewed code
* Compare original code with AI-suggested improvements
* Display review results through an interactive Streamlit dashboard

## 🏗️ Architecture

```text
                 User
                   │
                   ▼
          ┌─────────────────┐
          │  Streamlit UI   │
          └────────┬────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Upload      Paste      GitHub
       File       Code       Repo
        │          │          │
        └──────────┼──────────┘
                   ▼
          Language Detection
                   │
                   ▼
          ┌─────────────────┐
          │  Gemini LLM     │
          │   Code Review   │
          └────────┬────────┘
                   │
                   ▼
          Pydantic Validation
                   │
                   ▼
          ┌─────────────────┐
          │ Review Dashboard│
          └────────┬────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
      Findings        Improved Code
```

## 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **Google Gemini API**
* **google-genai**
* **Pydantic**
* **PyGithub** / GitHub repository integration
* **Requests**
* **python-dotenv**

## 📁 Project Structure

```text
ai-code-reviewer/
│
├── app.py
├── reviewer.py
├── github_utils.py
├── models.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── sample_code/
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-code-reviewer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Setup

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file should never be committed to GitHub.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 How It Works

1. The user provides source code by uploading a file, pasting code, or loading a public GitHub repository.
2. For GitHub repositories, the application downloads the repository and allows the user to select a source file.
3. The programming language is detected from the file extension.
4. The selected source code is sent to Gemini for analysis.
5. Gemini identifies potential software issues and assigns severity levels.
6. The response is validated using Pydantic structured models.
7. The application displays the review findings in an interactive dashboard.
8. Gemini also generates a suggested improved version of the source code.
9. The developer can review the AI suggestions and decide whether to apply them.

## 🤝 Human-AI Collaboration

The project follows a **human-in-the-loop approach** to AI-assisted software development.

The AI acts as a code-review assistant rather than autonomously modifying the developer's project. It identifies potential issues and proposes improvements, while the developer remains responsible for reviewing and deciding which suggestions should be adopted.

This demonstrates how LLMs can support developers during software engineering tasks while keeping human oversight in the development workflow.

## ⚠️ Current Limitations

* GitHub integration currently supports public repositories.
* The application reviews one selected source file at a time.
* AI-generated improvements should be reviewed by a developer before being used in production.
* The quality of the review depends on the source code and LLM output.

## 🔮 Future Improvements

Possible future improvements include:

* Multi-file repository analysis
* Private GitHub repository support
* Review history
* Downloadable review reports
* Pull-request integration
* Automated testing of suggested changes
* Human feedback and evaluation of AI-generated reviews

## 📌 Purpose

This project was developed as a portfolio project exploring **LLM-assisted software engineering and human-AI collaboration**.
