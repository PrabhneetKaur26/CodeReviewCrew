import os
import crewai.llms.cache as _crewai_cache
from dotenv import load_dotenv
from crewai import LLM

# Fix for CrewAI bug #5886
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

load_dotenv()

# Large LLM for complex logic & analysis (Reviewer, Security)
large_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=2000
)

# Small LLM for simpler tasks (Coder, Tester)
small_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=1500
)

llm = large_llm