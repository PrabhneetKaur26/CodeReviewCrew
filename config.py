# config.py
import os
import crewai.llms.cache as _crewai_cache
from dotenv import load_dotenv
from crewai import LLM

# Fix for CrewAI bug #5886 — cache_breakpoint injected into non-Anthropic providers
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq LLM for use across all agents
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=4096
)