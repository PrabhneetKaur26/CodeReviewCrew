# tasks.py
from crewai import Task
from agents import coder_agent, reviewer_agent, security_agent, tester_agent

def create_tasks(user_requirement, previous_feedback=""):
    
    coding_task = Task(
        description=(
            f"Write a Python function based on this requirement:\n{user_requirement}\n\n"
            f"Previous feedback to address (if any):\n{previous_feedback}\n\n"
            "Requirements:\n"
            "- Write clean, readable Python code\n"
            "- Include a docstring\n"
            "- Handle edge cases\n"
            "- Return only the function code, nothing else"
        ),
        expected_output=(
    "A complete Python function containing a docstring and inline comments. "
    "Return only the function code."),

        agent=coder_agent
    )

    review_task = Task(
    description=(
        "Review the Python function written by the Coder agent.\n"
        "Check for:\n"
        "- Logic errors or bugs\n"
        "- Missing edge cases\n"
        "- Poor variable naming\n"
        "- Readability issues\n"
        "- Best practice violations\n\n"
        "Do NOT rewrite the code. Only provide feedback.\n"
        "Be decisive — if there are issues, write NEEDS IMPROVEMENT.\n"
        "Only say APPROVED if the code truly needs no changes.\n\n"
        "At the very end of your response, write exactly one of these two lines, "
        "verbatim, as the very last line and nothing after it:\n"
        "VERDICT: APPROVED\n"
        "VERDICT: NEEDS IMPROVEMENT"
    ),
    expected_output=(
        "A structured review ending with exactly 'VERDICT: APPROVED' or 'VERDICT: NEEDS IMPROVEMENT'."
    ),
    agent=reviewer_agent,
    context=[coding_task]
)

    security_task = Task(
    description=(
        "Perform a security review of the Python function written by the Coder agent.\n"
        "Check for:\n"
        "- Use of eval() or exec()\n"
        "- Shell injection risks\n"
        "- Hardcoded secrets or credentials\n"
        "- Unsafe file operations\n"
        "- Missing input validation\n\n"
        "Be decisive — only flag real vulnerabilities, not theoretical ones.\n"
        "Do NOT suggest general improvements if no real vulnerabilities exist.\n\n"
        "At the very end of your response, write exactly one of these two lines, "
        "verbatim, as the very last line and nothing after it:\n"
        "VERDICT: SECURE\n"
        "VERDICT: VULNERABILITIES FOUND"
    ),
    expected_output=(
        "A security report ending with exactly 'VERDICT: SECURE' or 'VERDICT: VULNERABILITIES FOUND'."
    ),
    agent=security_agent,
    context=[coding_task]
)

    testing_task = Task(
    description=(
        "Write unit tests for the Python function written by the Coder agent.\n"
        "Requirements:\n"
        "- Write at least 4 test cases covering normal inputs, edge cases, and invalid inputs\n"
        "- After writing the tests, simulate running them mentally based on the code logic\n"
        "- At the very end of your response, write exactly one of these two lines, "
        "verbatim, as the very last line and nothing after it:\n"
        "VERDICT: PASSED\n"
        "VERDICT: FAILED\n"
        "- Write VERDICT: PASSED if all tests would pass based on the code logic\n"
        "- Write VERDICT: FAILED if any test would fail, and explain why before the verdict line"
    ),
    expected_output=(
    "Unit tests followed by a clear verdict.\n"
    "Last line must be exactly 'VERDICT: PASSED' or 'VERDICT: FAILED'."
),
    agent=tester_agent,
    context=[coding_task]
)

    return coding_task, review_task, security_task, testing_task