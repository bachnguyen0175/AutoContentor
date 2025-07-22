# AutoContentor: AI-Powered Content Research Automation

**AutoContentor** is a sophisticated, multi-agent platform designed to automate the entire content research process. By leveraging Google's Agent Development Kit (ADK), it coordinates a team of specialized AI agents to perform in-depth analysis on keywords, audience demographics, competitor strategies, and market trends. The result is a comprehensive, structured report that provides actionable insights for content creators, marketers, and strategists.

## ✨ Features

- **Multi-Agent System**: A team of specialized agents for keywords, audience, competitors, and trends.
- **Automated Research**: Automates the entire content research workflow, from data gathering to report generation.
- **Comprehensive Reports**: Generates detailed reports including audience personas, SWOT analyses, and keyword metrics.
- **Scalable Architecture**: Built on a lightweight, file-based system that is easy to deploy and scale.
- **Developer-Friendly**: Run all services locally with a single command using the ADK Web UI for real-time monitoring.
- **Docker Support**: Optional Docker Compose setup available for containerized deployments.

## 🏛️ Architecture

AutoContentor is built on a microservices-style architecture, with each agent operating as a separate service. The **Orchestrator** acts as the central hub, managing research campaigns and delegating tasks to the specialized agents. The system is designed to be stateless and uses a file-based approach for data persistence, making it highly portable and easy to manage.

## 🚀 Getting Started

Follow these steps to get AutoContentor up and running on your local machine for development.

### Prerequisites

- [Python 3.11+](https://www.python.org/)
- [Pip](https://pip.pypa.io/en/stable/installation/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/AutoContentor.git
    cd AutoContentor
    ```

2.  **Set up a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    -   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    -   Open the `.env` file and add your API keys and any other necessary configurations.

5.  **Run the ADK Web UI:**
    ```bash
    adk web
    ```
    This will start all the backend services and the developer UI.

## ⚙️ Configuration

The following environment variables need to be set in your `.env` file:

| Variable                      | Description                                      |
| ----------------------------- | ------------------------------------------------ |
| `GOOGLE_API_KEY`              | Your Google API key for Trends, Search, etc.     |
| `GOOGLE_SEARCH_ENGINE_ID`     | Your Google Custom Search Engine ID.             |
| `OPENAI_API_KEY`              | Your OpenAI API key.                             |
| `GEMINI_API_KEY`              | Your Gemini API key.                             |
| `SERPAPI_KEY`                 | Your SerpAPI key for search results.             |
| `SECRET_KEY`                  | A secret key for securing the application.       |

## Usage

Once the services are running via `adk web`, you can interact with the system through the ADK Web UI or by sending API requests directly.

### Using the ADK Web UI

1.  Open your browser and navigate to the ADK Web UI (typically `http://127.0.0.1:8000`).
2.  Use the interface to start a new campaign and monitor the real-time logs and events from the agents.

### Using the API

You can start a new research campaign by sending a POST request to the Orchestrator's API.

-   **Endpoint:** `http://127.0.0.1:8000/api/start-campaign`
-   **Method:** `POST`
-   **Body:**
    ```json
    {
      "campaignId": "your-campaign-id",
      "seedKeywords": ["keyword1", "keyword2"],
      "competitorList": ["competitor1.com", "competitor2.com"],
      "region": "US"
    }
    ```
The Orchestrator will then start the research process.

## 📁 Project Structure

```
AutoContentor/
├── .env.example                # Environment variables template
├── docker-compose.yaml         # Docker Compose configuration
├── pyproject.toml              # Project dependencies and metadata
├── src/
│   └── auto_contentor/
│       ├── orchestrator/       # Orchestrator service
│       ├── agents/             # Specialized agent services
│       │   ├── keyword/
│       │   ├── audience/
│       │   ├── competitor/
│       │   ├── trend/
│       │   └── aggregator/
│       └── shared/             # Shared libraries and utilities
└── ui/                         # Frontend application (Next.js)
```

## 🗺️ Roadmap

- [ ] Implement real-time progress updates on the frontend.
- [ ] Add support for more data sources and APIs.
- [ ] Enhance report generation with more customization options.
- [ ] Develop a user authentication system.
- [ ] Add comprehensive test coverage.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
