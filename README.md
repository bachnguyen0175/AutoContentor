# AutoContentor

AutoContentor is a multi-agent content research automation platform built on Google's Agent Development Kit (ADK). It orchestrates specialized agents to gather keyword data, audience personas, competitor SWOT analysis, and content trends, then aggregates results into structured reports.

---

## Features

- **Orchestrator**: Receives campaign metadata (campaignId, seedKeywords, competitorList, region), starts sessions, and dispatches tasks to agents.
- **Keyword Agent**: Fetches keyword metrics (volume, difficulty, CPC, trends, related terms) via SEMrush, Ahrefs, DataForSEO.
- **Audience Agent**: Builds customer personas (demographics, interests, pain points, sentiment) via Brandwatch, Twitter, Facebook.
- **Competitor Agent (SWOT)**: Conducts SWOT analysis (strengths, weaknesses, opportunities, threats) using Ahrefs, BuzzSumo, SimilarWeb.
- **Trend Agent**: Tracks content trends from Google Trends, Twitter, Reddit, Feedly.
- **Aggregator Agent**: Waits for all agent results, combines data into a `ReportEntity`, and generates final reports.
- **Shared Libraries**: Centralized API clients, Pydantic models, and utility helpers.
- **Dev-UI**: FastAPI + ADK Web UI for real-time logs, events, and workflow visualization.
- **Front-End**: React/Next.js interface for starting campaigns and viewing reports.
- **Local Dev**: Docker Compose setup to run all services locally.

---

## Repository Structure

```text
AutoContentor/
├── pyproject.toml              # Root project config
├── docker-compose.yaml         # Local development
├── .env.example                # Environment template
├── requirements.txt            # Root dependencies
├── src/
│   └── auto_contentor/
│       ├── __init__.py
│       ├── shared/             # Consolidated shared components
│       │   ├── __init__.py
│       │   ├── models/         # All Pydantic models here
│       │   │   ├── __init__.py
│       │   │   ├── campaign.py
│       │   │   ├── keyword.py
│       │   │   ├── audience.py
│       │   │   ├── competitor.py
│       │   │   ├── trend.py
│       │   │   └── report.py
│       │   ├── clients/        # API clients
│       │   │   ├── __init__.py
│       │   │   └── api_clients.py
│       │   ├── utils/          # Utilities
│       │   │   ├── __init__.py
│       │   │   ├── logger.py
│       │   │   ├── validators.py
│       │   │   └── helpers.py
│       │   └── config/         # Configuration management
│       │       ├── __init__.py
│       │       ├── settings.py
│       │       └── constants.py
│       ├── orchestrator/       # Orchestrator service
│       │   ├── __init__.py
│       │   ├── main.py         # FastAPI app
│       │   ├── agent.py        # Orchestrator agent
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   ├── job_dispatcher.py
│       │   │   └── health_check.py
│       │   └── api/
│       │       ├── __init__.py
│       │       ├── routes.py
│       │       └── schemas.py
│       └── agents/
│           ├── __init__.py
│           ├── base/           # Base agent classes
│           │   ├── __init__.py
│           │   └── base_agent.py
│           ├── keyword/
│           │   ├── __init__.py
│           │   ├── main.py
│           │   ├── agent.py
│           │   ├── services/
│           │   │   ├── __init__.py
│           │   │   ├── keyword_service.py
│           │   │   └── data_sources/
│           │   │       ├── semrush.py
│           │   │       ├── ahrefs.py
│           │   │       └── dataforseo.py
│           │   └── config.py
│           ├── audience/       # Similar structure
│           ├── competitor/     # Similar structure
│           ├── trend/          # Similar structure
│           └── aggregator/     # Similar structure
├── tests/                      # Root level tests
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── ui/                        # Frontend (optional)
│   └── nextjs/
└── docs/                      # Documentation
    ├── api.md
    ├── deployment.md
    └── development.md
```

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repo_url> AutoContentor
   cd AutoContentor
   ```
2. Copy environment template:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
3. Build and run all services:
   ```bash
   docker-compose up --build
   ```
4. Check service health:
   ```bash
   docker-compose ps
   ```

---

## Architecture

The system uses a stateless, file-based approach for data persistence. All agent results and reports are stored as JSON files in the local filesystem, making the system lightweight and easy to deploy without external database dependencies.

---

## Front-End (React/Next.js)

- Scaffold under `ui/nextjs` with TypeScript:
  ```bash
  npx create-next-app ui/nextjs --typescript
  cd ui/nextjs
  npm install axios swr tailwindcss
  ```
- Key pages:
  - `/start-campaign`: Form to POST campaign data to `/api/orchestrator`.
  - `/campaign/[id]`: Dashboard polling `/api/getReport?id=` to display report.
- Components: `KeywordTable`, `PersonaCard`, `SWOTGrid`, `TrendList`, etc.
- API routes proxy to FastAPI orchestrator endpoints.

---

## Next Steps

1. Implement core agent functionality.
2. Develop ADK integration and workflow orchestration.
3. Create file-based data persistence layer.
4. Scaffold front-end and API routes.
5. Integrate Dev-UI in orchestrator.
6. Add CI/CD workflows and full test coverage.

---

## License

MIT