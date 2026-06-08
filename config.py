import os

# URL
BASE_URL = "http://localhost:8000"
# chat model
REPO_ID = "Qwen/Qwen2.5-7B-Instruct"     # 100% free serverless model (no billing credits needed)
TEMPERATURE = 0.7
MAX_NEW_TOKENS = 1024

# Prompts paths
ADVISOR_PROMPT_PATH = os.path.join("prompts","advisor.txt")
MARKET_ANALYST_PROMPT_PATH = os.path.join("prompts","market_analyst.txt")
COMPETITOR_ANALYSIS_PROMPT_PATH = os.path.join("prompts","competitor_analyst_prompt.txt")
RISK_ASSESSOR_PROMPT_PATH = os.path.join("prompts","risk_assessor.txt")

# Graph
REPORTS_PATH = "reports"
GRAPH_VISUALIZATION_PATH = os.path.join(REPORTS_PATH,"ventureSense_graph.png")

ANALYSIS_LIST=["market_analysis","competition_analysis","risk_assessment"]