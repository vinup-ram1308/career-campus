import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agent.agent import root_agent

app = FastAPI(title="CareerCompass API")
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="careercompass", session_service=session_service)

class Query(BaseModel):
    user_id: str = "u001"
    message: str

@app.get("/")
def health():
    return {"status": "CareerCompass is running"}

@app.post("/analyze")
async def analyze(query: Query):
    session = await session_service.create_session(app_name="careercompass", user_id=query.user_id)
    enriched_message = f"[user_id: {query.user_id}] {query.message}"
    content = Content(role="user", parts=[Part(text=enriched_message)])
    response_text = ""
    async for event in runner.run_async(user_id=query.user_id, session_id=session.id, new_message=content):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    return {"response": response_text, "user_id": query.user_id}

@app.post("/plan")
async def plan(query: Query):
    session = await session_service.create_session(app_name="careercompass", user_id=query.user_id)
    # Specific instruction to skip market scan and focus on the roadmap
    plan_message = f"[user_id: {query.user_id}] Based on my profile, generate my 2-week learning sprints and portfolio project roadmap immediately."
    content = Content(role="user", parts=[Part(text=plan_message)])
    response_text = ""
    async for event in runner.run_async(user_id=query.user_id, session_id=session.id, new_message=content):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    return {"response": response_text, "user_id": query.user_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
