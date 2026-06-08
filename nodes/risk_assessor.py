from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Literal
from state.agent_state import AgentState
from models.chat_model import llm_with_tools, chat_model
import os
from config import RISK_ASSESSOR_PROMPT_PATH

def assess_risk(preferred_mode: Literal["chat_model", "tools"] = "chat_model"):
    def assessment_risk(state: AgentState) -> AgentState:
        """
        Analyzes risk factors and provide trends and insights.
        """
        if not os.path.exists(RISK_ASSESSOR_PROMPT_PATH):
            raise FileNotFoundError(f"Prompt file not found at {RISK_ASSESSOR_PROMPT_PATH}. Please check the path and try again.")
        try:
            template = open(RISK_ASSESSOR_PROMPT_PATH).read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found at {RISK_ASSESSOR_PROMPT_PATH}. Please check the path and try again.")
        
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", template),
                MessagesPlaceholder(variable_name="messages")
            ])
            
            if preferred_mode == "chat_model":
                chain = prompt_template | chat_model
            else:
                chain = prompt_template | llm_with_tools
                
            messages_input = state.get("messages", [])
            
            response = chain.invoke({
                "startup_idea": state["startup_idea"],
                "market_analysis": state["market_analysis"],
                "competition_analysis": state["competition_analysis"],
                "messages": messages_input
            })
            
            if hasattr(response, "tool_calls") and response.tool_calls:
                return {"messages": [response]}
            else:
                return {"risk_assessment": response.content, "messages": [response]}
        except Exception as e:
            raise ValueError(f"Error assessing risk : {e}")
            
    return assessment_risk