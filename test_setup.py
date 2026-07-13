import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)

test_agent = Agent(
    role="Python Developer",
    goal="Write simple Python functions",
    backstory="You are an experienced Python developer.",
    llm=llm,
    verbose=True,
    cache=False
)

test_task = Task(
    description="Write a Python function that adds two numbers and returns the result.",
    expected_output="A working Python function with a brief explanation.",
    agent=test_agent
)

crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    verbose=True
)

result = crew.kickoff()
print("\n✅ RESULT:\n", result)