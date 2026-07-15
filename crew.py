import time
from crewai import Crew, Process
from agents import coder_agent, reviewer_agent, security_agent, tester_agent
from tasks import create_tasks

MAX_ITERATIONS = 3

def run_crew(user_requirement):
    
    iteration_logs = []
    previous_feedback = ""
    final_code = ""
    overall_status = "FAILED"

    for iteration in range(1, MAX_ITERATIONS + 1):
        
        print(f"\n{'='*50}")
        print(f"ITERATION {iteration} of {MAX_ITERATIONS}")
        print(f"{'='*50}\n")

        coding_task, review_task, security_task, testing_task = create_tasks(
            user_requirement=user_requirement,
            previous_feedback=previous_feedback
        )

        crew = Crew(
            agents=[coder_agent, reviewer_agent, security_agent, tester_agent],
            tasks=[coding_task, review_task, security_task, testing_task],
            process=Process.sequential,
            verbose=True
        )

        # Wait between tasks to avoid hitting Groq TPM rate limits
        time.sleep(30)

        # Note: stopping condition relies on agents using exact keywords
        crew.kickoff()

        coder_output    = str(coding_task.output.raw)    if coding_task.output    else "No output"
        reviewer_output = str(review_task.output.raw)    if review_task.output    else "No output"
        security_output = str(security_task.output.raw)  if security_task.output  else "No output"
        tester_output   = str(testing_task.output.raw)   if testing_task.output   else "No output"

        final_code = coder_output

        iteration_logs.append({
            "iteration": iteration,
            "coder": coder_output,
            "reviewer": reviewer_output,
            "security": security_output,
            "tester": tester_output
        })

        tests_passed = (
            "PASSED" in tester_output.upper() and
            "FAILED" not in tester_output.upper()
        )

        reviewer_approved = (
            "APPROVED" in reviewer_output.upper() and
            "NEEDS IMPROVEMENT" not in reviewer_output.upper()
        )

        security_approved = (
            "SECURE" in security_output.upper() and
            "VULNERABILITIES FOUND" not in security_output.upper()
        )

        if reviewer_approved and security_approved:
            overall_status = "SUCCESS"
            print(f"\n✅ All checks passed at iteration {iteration}. Stopping loop.")
            break
        else:
            previous_feedback = (
                f"Reviewer feedback:\n{reviewer_output}\n\n"
                f"Security feedback:\n{security_output}\n\n"
                f"Tester feedback:\n{tester_output}"
            )
            if iteration < MAX_ITERATIONS:
                print(f"\n⚠️ Issues found. Proceeding to iteration {iteration + 1}.")
            else:
                print("\n❌ Maximum iterations reached.")

    summary = generate_summary(iteration_logs, overall_status, final_code)
    return summary


def generate_summary(iteration_logs, overall_status, final_code):
    summary = {
        "status": overall_status,
        "total_iterations": len(iteration_logs),
        "final_code": final_code,
        "iterations": iteration_logs
    }
    return summary