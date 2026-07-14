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
            "Do NOT rewrite the code. Only provide feedback."
        ),
        expected_output=(
            "A structured review with:\n"
            "- APPROVED or NEEDS IMPROVEMENT status\n"
            "- List of specific issues found (if any)\n"
            "- Suggestions for improvement"
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
            "- Missing input validation\n"
            "- Any other security vulnerabilities\n\n"
            "Do NOT rewrite the code. Only report findings."
        ),
        expected_output=(
            "A security report with:\n"
            "- SECURE or VULNERABILITIES FOUND status\n"
            "- List of security issues with explanation (if any)\n"
            "- Recommended fixes for each issue"
        ),
        agent=security_agent,
        context=[coding_task]
    )

    testing_task = Task(
        description=(
            "Write and execute unit tests for the Python function written by the Coder agent.\n"
            "Requirements:\n"
            "- Write at least 4 test cases\n"
            "- Cover normal inputs, edge cases, and invalid inputs\n"
            "- Execute the tests\n"
            "- Report pass/fail status for each test"
        ),
        expected_output=(
            "A test report with:\n"
            "- PASSED or FAILED overall status\n"
            "- List of individual test cases with pass/fail\n"
            "- Error details for any failing tests"
        ),
        agent=tester_agent,
        context=[coding_task]
    )

    return coding_task, review_task, security_task, testing_task