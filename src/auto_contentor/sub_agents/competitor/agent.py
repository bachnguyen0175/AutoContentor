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

"""Agent module for the Competitor Analysis Agent."""

import logging
import warnings
import asyncio
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .prompt import COMPETITOR_ANALYSIS_PROMPT

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

logger = logging.getLogger(__name__)

# Model configuration
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

competitor_agent = LlmAgent(
    name="CompetitorAnalysisAgent",
    model=AGENT_MODEL,
    instruction=COMPETITOR_ANALYSIS_PROMPT,
    description="Performs a SWOT analysis on competitors in a given industry.",
    tools=[google_search],
    output_key="competitor_swot",
)


if __name__ == "__main__":
    async def main():
        """Main function to run the agent."""
        print("Testing Competitor Analysis Agent...")
        result = await competitor_agent.run(
            {"query": "Analyze the competitors of online fitness coaching in Vietnam."}
        )
        print(result)

    asyncio.run(main())