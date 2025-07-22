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

"""Main module for the Orchestrator FastAPI app."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from .agent import root_agent as orchestrator_agent

# Define the input model based on the campaign format
class CampaignInput(BaseModel):
    campaign_name: str = Field(..., description="Name of the campaign.")
    topic: str = Field(..., description="Core context for the content research.")
    seed_keywords: Optional[List[str]] = Field(None, description="Seed keywords for research.")
    competitors: Optional[List[str]] = Field(None, description="List of competitor domains.")
    region: Optional[str] = Field("global", description="Geographic region (e.g., US, VN).")
    language: Optional[str] = Field("en", description="Language code (e.g., en, vi).")
    persona_focus: Optional[str] = Field(None, description="Target audience persona.")


app = FastAPI(
    title="AutoContentor Orchestrator",
    description="API for running content research campaigns.",
)

@app.post("/run_campaign/")
async def run_campaign(campaign_input: CampaignInput):
    """
    Endpoint to run a new content research campaign.
    """
    try:
        # The Pydantic model is converted to a dict to be passed to the agent
        input_dict = campaign_input.model_dump(exclude_unset=True)
        
        # The field names in the Pydantic model use underscores, but the agent
        # prompts expect spaces. We need to convert them.
        formatted_input = {key.replace('_', ' ').title(): value for key, value in input_dict.items()}

        result = await orchestrator_agent.run(formatted_input)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Orchestrator is running. Go to /docs to see the API."}
