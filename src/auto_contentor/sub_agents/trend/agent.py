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

"""Agent module for the Trend Analysis Agent."""

import logging
import warnings
import asyncio
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .prompt import TREND_ANALYSIS_PROMPT

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

logger = logging.getLogger(__name__)

# Model configuration
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

trend_agent = LlmAgent(
    name="TrendAnalysisAgent",
    model=AGENT_MODEL,
    instruction=TREND_ANALYSIS_PROMPT,
    description="Analyzes content trends using Google Search.",
    tools=[google_search],
    output_key="trend_analysis",
)


if __name__ == "__main__":
    async def main():
        """Main function to run the agent."""
        print("Testing Trend Analysis Agent...")
        result = await trend_agent.run(
            {
                "Topic": "ai agents",
                "Region": "US"
            }
        )
        print(result)

    asyncio.run(main())
