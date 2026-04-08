import os
from google.cloud import bigquery
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "careercompass-492713")
DATASET = "careercompass"
client = bigquery.Client(project=PROJECT)

def row_to_dict(row):
    """Convert a BigQuery row to a JSON-serializable dict."""
    return {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in dict(row).items()}

def search_job_market(target_role: str) -> dict:
    """Search the job market for a given role and return top in-demand skills."""
    query = f"""
        SELECT skill_name, job_count, trend_direction, scan_date
        FROM `{PROJECT}.{DATASET}.market_signals`
        ORDER BY job_count DESC
        LIMIT 10
    """
    rows = list(client.query(query).result())
    return {"results": [row_to_dict(r) for r in rows]}

def get_skill_trends(skill_name: str) -> dict:
    """Get the trend direction for a specific skill."""
    query = f"""
        SELECT skill_name, job_count, trend_direction, scan_date
        FROM `{PROJECT}.{DATASET}.market_signals`
        WHERE LOWER(skill_name) = LOWER('{skill_name}')
        LIMIT 1
    """
    rows = list(client.query(query).result())
    return {"results": [row_to_dict(r) for r in rows]}

def get_user_profile(user_id: str) -> dict:
    """Retrieve the current skill profile and career goals for a user."""
    query = f"""
        SELECT user_id, name, current_role, target_role, skills
        FROM `{PROJECT}.{DATASET}.user_profile`
        WHERE user_id = '{user_id}'
        LIMIT 1
    """
    rows = list(client.query(query).result())
    return {"results": [row_to_dict(r) for r in rows]}

def get_learning_sprints(user_id: str) -> dict:
    """Get all learning sprints for a user."""
    query = f"""
        SELECT sprint_id, skill, start_date, end_date, status
        FROM `{PROJECT}.{DATASET}.learning_sprints`
        WHERE user_id = '{user_id}'
        ORDER BY start_date ASC
    """
    rows = list(client.query(query).result())
    return {"results": [row_to_dict(r) for r in rows]}

tools = [
    FunctionTool(search_job_market),
    FunctionTool(get_skill_trends),
    FunctionTool(get_user_profile),
    FunctionTool(get_learning_sprints),
]

job_market_agent = Agent(
    name="job_market_scanner",
    model="gemini-2.5-flash",
    description="Scans the job market and identifies top in-demand skills for a target role.",
    instruction="""
You are a Job Market Scanner. When given a target role, use the search_job_market tool
to retrieve current in-demand skills. Present the results clearly showing skill name,
job count, and whether the skill is rising, stable, or emerging.
Always summarize the top 3 skills the user should focus on.
""",
    tools=tools,
)

skill_gap_agent = Agent(
    name="skill_gap_analyst",
    model="gemini-2.5-flash",
    description="Compares a user's current skills against market demand and identifies gaps.",
    instruction="""
You are a Skill Gap Analyst. Use get_user_profile to fetch the user's current skills
and target role. Use search_job_market to get market demand.
Compare the two and produce a prioritized list of skill gaps.
Score each gap as Critical, Important, or Nice-to-have.
""",
    tools=tools,
)

sprint_planner_agent = Agent(
    name="learning_sprint_planner",
    model="gemini-2.5-flash",
    description="Creates a 2-week learning sprint plan for each skill gap.",
    instruction="""
You are a Learning Sprint Planner. Use get_learning_sprints to check existing sprints
for the user. Based on skill gaps provided, create a structured 2-week sprint plan
for each missing skill. For each sprint specify: skill, goal, recommended resources,
and a daily time commitment. Present as a clear week-by-week plan.
""",
    tools=tools,
)

portfolio_advisor_agent = Agent(
    name="portfolio_advisor",
    model="gemini-2.5-flash",
    description="Recommends concrete projects to build for each skill gap.",
    instruction="""
You are a Portfolio Advisor. For each skill gap identified, recommend one concrete
project the user can build to demonstrate that skill to employers. Each project should:
- Have a clear title
- Take 1-2 weeks to build
- Be deployable/shareable (GitHub, HuggingFace, etc.)
- Directly signal the skill to a hiring manager
Present as a numbered portfolio roadmap.
""",
    tools=tools,
)

root_agent = Agent(
    name="careercompass_orchestrator",
    model="gemini-2.5-flash",
    description="CareerCompass: Your AI career intelligence co-pilot.",
    instruction="""
You are CareerCompass, an intelligent career co-pilot. You help users understand
their skill gaps, plan their learning, and build a portfolio to reach their career goals.

When a user describes their situation or asks for career guidance:
1. Use job_market_scanner to understand what skills the market demands for their target role
2. Use skill_gap_analyst to identify which of those skills the user is missing
3. Use learning_sprint_planner to create a structured learning plan
4. Use portfolio_advisor to recommend projects that demonstrate each skill

Always present a unified, actionable career roadmap at the end combining all insights.
Be encouraging, specific, and data-driven.
For user_id, default to "u001" unless the user specifies otherwise.
""",
    sub_agents=[job_market_agent, skill_gap_agent, sprint_planner_agent, portfolio_advisor_agent],
    tools=tools,
)
