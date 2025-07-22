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

"""Orchestrator agent that manages the content research workflow."""

import asyncio
from google.adk.agents import ParallelAgent, SequentialAgent

# Import all the sub-agents
from ..sub_agents.keyword.agent import keyword_agent
from ..sub_agents.audience.agent import audience_agent
from ..sub_agents.competitor.agent import competitor_agent
from ..sub_agents.trend.agent import trend_agent
from ..sub_agents.aggregator.agent import aggregator_agent

# The four research agents can run in parallel.
# Their combined output will be a dictionary with keys matching their `output_key`.
research_agents = ParallelAgent(
    name="ResearchAgent",
    sub_agents=[
        keyword_agent,
        audience_agent,
        competitor_agent,
        trend_agent,
    ],
)

# The sequential agent runs the parallel research agents first,
# then passes their combined output to the aggregator agent.
orchestrator_agent = SequentialAgent(
    name="OrchestratorAgent",
    sub_agents=[
        research_agents,
        aggregator_agent,
    ],
)

root_agent = orchestrator_agent

if __name__ == "__main__":
    async def main():
        """Main function to run the orchestrator."""
        print("Testing Orchestrator Agent...")
        
        # This is the input format the user will provide.
        campaign_input = {
            "Campaign Name": "AI Agent Deep Dive",
            "Topic": "Create content about AI agent",
            "Seed Keywords": ["ai agent", "generative ai", "multi-agent systems"],
            "Competitors": ["openai.com", "anthropic.com", "cohere.com"],
            "Region": "US",
            "Language": "en",
            "Persona Focus": "developers",
        }
        
        result = await root_agent.run(campaign_input)
        print("--- Orchestrator Result ---")
        print(result)

    asyncio.run(main())
