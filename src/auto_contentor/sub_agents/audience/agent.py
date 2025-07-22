# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Agent module for the Audience Persona Agent."""

import logging
import warnings
import asyncio
from google.adk.agents import LlmAgent
from .tools import youtube_search_tool
from .prompt import AUDIENCE_RESEARCH_PROMPT

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

logger = logging.getLogger(__name__)

# Model configuration
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

audience_agent = LlmAgent(
    name="AudienceResearchAgent",
    model=AGENT_MODEL,
    instruction=AUDIENCE_RESEARCH_PROMPT,
    description="Analyzes YouTube audience data to create detailed buyer personas.",
    tools=[youtube_search_tool],
    output_key="audience_persona",
)


if __name__ == "__main__":
    async def main():
        """Main function to run the agent."""
        print("Testing Audience Persona Agent...")
        result = await audience_agent.run(
            {
                "Topic": "AI Agent",
                "Persona Focus": "developers",
                "Region": "US"
            }
        )
        print(result)

    asyncio.run(main())
