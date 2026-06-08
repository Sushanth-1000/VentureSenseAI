from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

#State model for the agent
class AgentState(TypedDict):
    startup_idea: str
    market_analysis: Optional[str]
    competition_analysis: Optional[str]
    risk_assessment: Optional[str]
    advisor_recommendations: Optional[str]
    confidence: Optional[int]
    summary: Optional[str]
    advice: Optional[str]
    messages: Annotated[List[BaseMessage], add_messages]