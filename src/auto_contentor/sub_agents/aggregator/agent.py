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

"""Agent module for the Aggregator Agent."""

import logging
import warnings
import asyncio
from google.adk.agents import LlmAgent
from .prompt import AGGREGATOR_PROMPT
from .tools import save_report_tool

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

logger = logging.getLogger(__name__)

# Model configuration
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

aggregator_agent = LlmAgent(
    name="AggregatorAgent",
    model=AGENT_MODEL,
    instruction=AGGREGATOR_PROMPT,
    description="Aggregates research from other agents and saves it as a document.",
    tools=[save_report_tool],
)


if __name__ == "__main__":
    async def main():
        """Main function to run the agent."""
        print("Testing Aggregator Agent...")
        
        # Mock input from other agents
        mock_input = {
            "keyword_analysis": {"..."},
            "audience_persona": {"..."},
            "competitor_swot": {"..."},
            "trend_analysis": {"..."}
        }
        
        result = await aggregator_agent.run(mock_input)
        print(result)

    asyncio.run(main())
