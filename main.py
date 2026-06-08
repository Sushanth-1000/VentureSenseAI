from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Annotated
from graphs.workflow import build_graph
import os

app = FastAPI(title="VentureSense AI Backend")
graph = build_graph()

# Mount static assets
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

# pydantic model for request body
class StartupIdea(BaseModel):
    startup_idea: Annotated[str, Field(..., description="Startup idea to validate")]

@app.get("/")
async def read_root():
    if os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    return {"message": "Welcome to the VentureSense AI API"}

@app.post("/validate")
async def research(idea:StartupIdea):
    try:
        result= await graph.ainvoke(
            {
                "startup_idea":idea.startup_idea,
                "market_analysis":None,
                "competition_analysis":None,
                "risk_assessment":None,
                "advisor_recommendations":None,
                "confidence":None,
                "summary":None,
                "advice":None,
                "messages":[]
                })
        return JSONResponse(status_code=200, 
                            content={
                                "startup_idea": result["startup_idea"],
                                "market_analysis":result["market_analysis"],
                                "competition_analysis": result["competition_analysis"],
                                "risk_assessment": result["risk_assessment"],
                                "advisor_recommendations": result["advisor_recommendations"],
                                "confidence": result.get("confidence", 80),
                                "summary": result.get("summary", ""),
                                "advice": result["advice"]}
                            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))