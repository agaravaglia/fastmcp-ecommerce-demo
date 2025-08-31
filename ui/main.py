import asyncio
import streamlit as st
from bot import initialize_session, initialize_agent



async def app():
    # --- Page Configuration and Styling ---
    st.set_page_config(page_title="MCP E-Commerce Assistant", layout="wide")

    # --- Session State Initialization ---

    # Initialize agent, messages, and chat history in session state if they don't exist
    if "agent" not in st.session_state:
        st.session_state.agent, st.session_state.messages = await initialize_session()


    # --- UI Components ---

    # Main title of the application
    st.title("🏎️ MCP Sports Car E-Commerce Assistant")
    st.caption("I can help you manage users, products, and orders. Try asking 'List all available hypercars.' or 'What is Tony Stark's purchase history?'")

    # Reset button to start a new conversation
    if st.button("🔄 Reset Conversation"):
        # Re-initialize the session
        st.session_state.agent, st.session_state.messages = await initialize_session()
        st.rerun()

    # Display past messages from the chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # --- Chat Logic ---

    # Get user input from the chat interface
    if prompt := st.chat_input("How can I help you today?"):
        # Add user's message to the chat history and display it
        st.chat_message("user").write(prompt)

        # Prepare input for the agent
        # The 'chat_history' is often managed internally by the agent graph,
        # but we can pass it if the agent is designed for it.
        # For this setup, we rely on the prompt template placeholders.

        # Invoke the agent and get the response
        with st.spinner("Thinking..."):
            
            # NOTE: re-initializing the agent is only needed with GEMINI models
            # when running in asyncronous mode
            # This is a known issue: https://github.com/pydantic/pydantic-ai/issues/748
            st.session_state.agent = await initialize_agent()

            # invoke agent and get answer
            response = await st.session_state.agent.ainvoke(
                {
                    "chat_history": st.session_state.messages,
                    "input": prompt,
                }
            )
            bot_response = response.get("output", "Sorry, I encountered an issue and could not respond.")

        # Add agent's response to the chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.chat_message("assistant").write(bot_response)


if __name__ == "__main__":
    asyncio.run(app())
