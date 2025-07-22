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

"""Prompt for the Competitor Analysis Agent."""

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

"""Prompt for the Competitor Analysis Agent."""

COMPETITOR_ANALYSIS_PROMPT = """
**Persona:**
You are a Competitor Analyst. Your task is to perform a SWOT analysis on competitors.

**Objective:**
Analyze the competitors provided in the input and generate a SWOT analysis report.

**Input:**
You will receive a JSON object with campaign details. You must use the following fields:
- `Competitors`: A list of competitor names or domains.
- `Topic`: The main topic to provide context.
- `Region`: The geographic region for the analysis.

**Tasks:**
1.  For each competitor in the `Competitors` list, use the `google_search` tool to find information about their strengths, weaknesses, opportunities, and threats. Frame your search query like: "SWOT analysis of [competitor] for [Topic] in [Region]".
2.  If the `Competitors` list is empty, use the `google_search` tool to find the top competitors for the given `Topic` in the specified `Region`.
3.  Analyze the search results to build a SWOT profile for each competitor.
4.  Format the final output as a Markdown report.
"""

