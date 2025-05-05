from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
model = "llama-3.3-70b-versatile"

load_dotenv()
groq_api_key = os.getenv("API_KEY")
if not groq_api_key:
    raise ValueError("API_KEY environment variable not set.")
model = ChatGroq(groq_api_key=groq_api_key, model_name=model)

memory = MemorySaver()
search = TavilySearchResults(max_results=2)
tools = [search]
agent_executor = create_react_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="I live in dubai.whats the weather where I live?")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()