import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.client import MultiServerMCPClient


#from langgraph.prebuilt import create_tool_calling_agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv


# Load environment variables
load_dotenv(dotenv_path='../.env')


SYSTEM_PROMPT = """
You are a helpful assistant for an employee managing a sports car ecommerce website.
Your role is to use the available tools to answer questions and perform operations related to users, products, and orders.

When answering a question, follow these guidelines:
- Be concise and clear in your responses.
- When you return data, format it nicely.
- If a tool call fails, explain the error to the user in a helpful way.
- Always check for a user's purchase history before suggesting a new purchase.
- Display JSON as tables if the JSON contains more than one record.
"""

async def initialize_agent():
    """
    Initializes the LangGraph agent, and other session state variables.

    Returns:
        An executable LangGraph agent and a list for storing chat messages.
    """
    # initialize MCP client
    mcp_client = MultiServerMCPClient({
        "fastmcp": {
            "url": os.environ['MCP_SERVER_URL'],
            "transport": "streamable_http",
        }
    })
    # Fetch tools from MCP client
    tools = await mcp_client.get_tools()

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    # Initialize chat model
    llm = ChatGoogleGenerativeAI(
        model=os.environ['GOOGLE_GEMINI_MODEL'],
        temperature=0.1,
        max_tokens=None,
        timeout=None,
        max_retries=5
    )

    # define agent
    agent_executor = AgentExecutor(
        agent=create_tool_calling_agent(
            llm=llm,
            prompt=prompt,
            tools=tools
        ),
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    # Initialize messages list for chat history
    # This is not ideal, but I am not interested in the agent definition
    # For the purpose of the demo this is enough
    return agent_executor


async def initialize_session() -> tuple[AgentExecutor, list]:
    """
    Initialize agent and messages from scrach

    Returns:
        Newly initialized agent and messages
    """
    agent = await initialize_agent()
    messages = []
    return agent, messages
