import os
import crewai.llms.cache as _crewai_cache
from dotenv import load_dotenv
from crewai import LLM

# Fix for CrewAI bug #5886
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

load_dotenv()

# Large model
large_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
    max_tokens=4096
)

# Small model
small_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
    max_tokens=4096
)

llm = large_llm