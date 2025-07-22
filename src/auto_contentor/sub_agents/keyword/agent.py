from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompts

MODEL = "gemini-2.5-flash"

keyword_agent = LlmAgent(
    name="keyword_agent",
    model=MODEL,
    instruction=prompts.KEYWORD_RESEARCH_PROMPT,
    tools=[google_search],
    output_key="keyword_analysis",
)