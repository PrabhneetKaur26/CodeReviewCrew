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
        "Be decisive — if there are issues, say NEEDS IMPROVEMENT.\n"
        "Only say APPROVED if the code truly needs no changes."
    ),
    expected_output=(
        "A structured review with:\n"
        "- APPROVED (if code needs no changes) or NEEDS IMPROVEMENT (if issues exist)\n"
        "- If NEEDS IMPROVEMENT: list specific issues only, no suggestions for approved code\n"
        "- If APPROVED: confirm what is correct, no improvement suggestions"
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
        "Do NOT suggest general improvements if no real vulnerabilities exist."
    ),
    expected_output=(
        "A security report with:\n"
        "- SECURE (if no real vulnerabilities found) or VULNERABILITIES FOUND (if issues exist)\n"
        "- If SECURE: briefly confirm what was checked\n"
        "- If VULNERABILITIES FOUND: list each issue with explanation and fix"
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
        "- At the very end of your response, write either PASSED or FAILED on its own line\n"
        "- Write PASSED if all tests would pass based on the code logic\n"
        "- Write FAILED if any test would fail, and explain why"
    ),
    expected_output=(
        "Unit tests followed by a clear verdict.\n"
        "Last line must be either PASSED or FAILED."
    ),
    agent=tester_agent,
    context=[coding_task]
)

    return coding_task, review_task, security_task, testing_task