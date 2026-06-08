from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode,tools_condition
import os
from langchain_core.messages import ToolMessage
from state.agent_state import AgentState
from nodes.market_analyst import analyze_market
from nodes.competitor_analysis import analyze_competition
from nodes.risk_assessor import assess_risk
from nodes.advisor import advisor
from tools.web_search_tool import web_search
from config import REPORTS_PATH,GRAPH_VISUALIZATION_PATH,ANALYSIS_LIST

def router(state:AgentState):       # Handles the routing logic after the tools node
    current_analysis = None
    for analysis in ANALYSIS_LIST:
        if state.get(analysis) is None:
            current_analysis = analysis
            break
            
    if current_analysis is None:
        return "advisor"
        
    last_message = state["messages"][-1]
    
    # Check if tool execution failed
    tool_failed = isinstance(last_message, ToolMessage) and last_message.content == "tool_failed"
    
    if tool_failed:
        if current_analysis == "market_analysis":
            return "analyze_market_fallback"
        elif current_analysis == "competition_analysis":
            return "analyze_competition_fallback"
        elif current_analysis == "risk_assessment":
            return "assess_risk_fallback"
    else:
        # Tool succeeded: loop back to the corresponding node to synthesize search results
        if current_analysis == "market_analysis":
            return "analyze_market"
        elif current_analysis == "competition_analysis":
            return "analyze_competition"
        elif current_analysis == "risk_assessment":
            return "assess_risk"
            
    return "advisor"

def build_graph():
    try:
        graph_builder = StateGraph(AgentState)
        
        # define the nodes
        graph_builder.add_node("analyze_market",analyze_market(preferred_mode="tools"))
        graph_builder.add_node("analyze_competition",analyze_competition(preferred_mode="tools"))
        graph_builder.add_node("assess_risk",assess_risk(preferred_mode="tools"))

        # fallback nodes (chat_model only)
        graph_builder.add_node("analyze_market_fallback",analyze_market(preferred_mode="chat_model"))
        graph_builder.add_node("analyze_competition_fallback",analyze_competition(preferred_mode="chat_model"))
        graph_builder.add_node("assess_risk_fallback",assess_risk(preferred_mode="chat_model"))
        
        graph_builder.add_node("advisor", advisor)
        graph_builder.add_node("tools", ToolNode(tools=[web_search]))  # tools node for tool calls
        
        graph_builder.set_entry_point("analyze_market")     # entry point of the graph
        graph_builder.add_conditional_edges("analyze_market",tools_condition,{"tools": "tools","__end__":"analyze_competition"})  # condition to check if tools are needed
        graph_builder.add_conditional_edges("analyze_competition",tools_condition,{"tools": "tools","__end__":"assess_risk"})
        graph_builder.add_conditional_edges("assess_risk",tools_condition,{"tools": "tools","__end__":"advisor"})
        graph_builder.add_conditional_edges("tools",router)
        graph_builder.add_edge("analyze_market_fallback","analyze_competition")
        graph_builder.add_edge("analyze_competition_fallback","assess_risk")
        graph_builder.add_edge("assess_risk_fallback","advisor")

        graph_builder.add_edge("advisor", END)
        
        graph=graph_builder.compile()       # compile the graph
        
        return graph
    except Exception as e:
        print(f"Error in building graph: {e}")
        return None