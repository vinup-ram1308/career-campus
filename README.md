# CareerCompass — Multi-Agent Skill Gap Intelligence



**CareerCompass** is a multi-agent AI system designed for the Google Cloud Gen AI Academy APAC 2026 Hackathon to provide real-time, data-driven career roadmap intelligence. It analyzes the delta between a user's current profile and live market demand to generate actionable 14-day learning plans and portfolio projects.



---



## 🚀 Project Overview



Professionals often struggle to transition into new roles because they lack insight into which skills are currently "Rising" or "Critical" in the job market. CareerCompass replaces static advice with a dynamic intelligence engine.



### Key Features

* **Real-time Market Scanning**: Queries BigQuery `market_signals` to identify top-trending skills and job counts.

* **Intelligent Gap Analysis**: Compares the user's current skill set against market demand to prioritize gaps as Critical, Important, or Nice-to-have.

* **Automated Sprint Planning**: Generates day-by-day, 2-week learning schedules for missing skills.

* **Portfolio Advisor**: Recommends concrete, shareable projects to demonstrate mastery to hiring managers.



---



## 🏗️ Architecture



The system uses a sophisticated multi-agent orchestration pattern built with the **Google ADK** and **Gemini 2.5 Flash**.



* **Compute**: FastAPI wrapper deployed on **Google Cloud Run**.

* **Intelligence Layer**: A Root Orchestrator managing four specialized sub-agents:

    * **Job Market Scanner**: Identifies top in-demand skills for target roles.

    * **Skill Gap Analyst**: Performs delta analysis on user profiles vs. demand.

    * **Learning Sprint Planner**: Creates structured study timelines.

    * **Portfolio Advisor**: Generates project roadmaps.

* **Data Layer**: **Google BigQuery** hosting `user_profile`, `market_signals`, and `learning_sprints` tables.



---



## 🛠️ Tech Stack



| Component | Technology |

| :--- | :--- |

| **LLM** | Gemini 2.5 Flash |

| **Agent Framework** | Google ADK (Agent Development Kit) |

| **Data Warehouse** | Google BigQuery |

| **API Framework** | FastAPI |

| **Deployment** | Google Cloud Run |

| **Language** | Python 3.12 |



---



## 🚦 Getting Started



### Prerequisites

* A Google Cloud Project with the BigQuery API enabled.

* An API Key from Google AI Studio.



### Installation

1.  **Clone the Repository**:

    ```bash

    git clone https://github.com/vinupram/careercompass.git

    cd careercompass

    ```

2.  **Install Dependencies**:

    ```bash

    pip install -r requirements.txt

    ```

3.  **Environment Setup**:

    ```bash

    export GOOGLE_API_KEY="your-api-key"

    export GOOGLE_CLOUD_PROJECT="careercompass-492713"

    ```

4.  **Run Locally**:

    ```bash

    python main.py

    ```



---



## 📡 API Endpoints



### `POST /analyze`

Retrieves a full market analysis and prioritized skill gap report.

* **Request Body**: `{"user_id": "u001", "message": "Analyze my gap for Senior ML Engineer"}`



### `POST /plan`

Generates an immediate 2-week learning roadmap and project suggestions.

* **Request Body**: `{"user_id": "u001", "message": "Give me my roadmap"}`



---



## 📂 Directory Structure

```text

~/careercompass/

├── agent/

│   ├── __init__.py

│   └── agent.py       # Core ADK Agent definitions

├── main.py            # FastAPI entry point

├── requirements.txt   # Project dependencies

├── Dockerfile         # Cloud Run container definition

└── tools.yaml         # Original MCP tool definitions

```





---



**Author**: Vinup Ram  

**Live Demo**: [CareerCompass API](https://careercompass-api-947148723141.us-west1.run.app)
