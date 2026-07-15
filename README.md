# 🤖 CodeReviewCrew
A multi-agent AI system where specialized agents collaboratively write, review, analyze security vulnerabilities, and test Python code using CrewAI and Streamlit.

---

## ✨ Features

- 🧑‍💻 AI Code Generation
- 🔍 Automated Code Review
- 🔒 Security Analysis
- 🧪 Unit Test Generation
- 🔄 Iterative Improvement (up to 3 cycles)
- 📄 JSON Report Generation
- 🎨 Interactive Streamlit Dashboard

---

## 🛠️ Tech Stack

- Python
- CrewAI
- Streamlit
- Groq API
- python-dotenv

---

## 📁 Project Structure

```
CodeReviewCrew/
│── app.py
│── agents.py
│── tasks.py
│── crew.py
│── config.py
│── utils.py
│── outputs/
│── .env
│── requirements.txt
```

---

## 🚀 Running the Project

1. Clone the repository

```bash
git clone <repository-url>
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file

```text
GROQ_API_KEY=your_api_key
```

4. Run the application

```bash
streamlit.exe run app.py
```

---

## 🔄 Workflow

```
User Requirement
      │
      ▼
🧑‍💻 Coder
      │
      ▼
🔍 Reviewer
      │
      ▼
🔒 Security Reviewer
      │
      ▼
🧪 Tester
      │
      ▼
Final Report
```

If issues are detected, feedback is sent back to the Coder for another iteration (maximum 3 iterations).

---
