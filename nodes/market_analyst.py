from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Literal
from langchain_core.messages import HumanMessage
from state.agent_state import AgentState
from models.chat_model import llm_with_tools, chat_model
from config import MARKET_ANALYST_PROMPT_PATH

def analyze_market(preferred_mode: Literal["chat_model", "tools"] = "chat_model"):
    def market_analyzation(state: AgentState) -> AgentState:
        """
        Creates a market analyst agent that can analyze market trends and provide insights.
        """
        try:
            template = open(MARKET_ANALYST_PROMPT_PATH).read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found at {MARKET_ANALYST_PROMPT_PATH}. Please check the path and try again.")
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", template),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        if preferred_mode == "chat_model":
            chain = prompt_template | chat_model
        else:
            chain = prompt_template | llm_with_tools
            
        messages_to_return = []
        messages_input = state.get("messages", [])
        if not messages_input:
            human_msg = HumanMessage(content=state["startup_idea"])
            messages_input = [human_msg]
            messages_to_return.append(human_msg)
            
        response = chain.invoke({
            "startup_idea": state["startup_idea"],
            "messages": messages_input
        })
        
        if hasattr(response, "tool_calls") and response.tool_calls:
            return {"messages": messages_to_return + [response]}
        else:
            return {"market_analysis": response.content, "messages": messages_to_return + [response]}
            
    return market_analyzation