# FastMCP E-Commerce Agent Demo

This repository provides a demonstration of a Model-Context-Protocol (MCP) server implemented using the `FastMCP` Python package.

The demo is built around a concrete use case: a chatbot assistant for an e-commerce website that sells sports cars. The AI agent can access information about users, products, and orders, and perform actions like creating new orders or updating user information.

The project is fully containerized using Docker and orchestrated with Docker Compose.

## 🚀 How to Run the Demo

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root of the project by copying the example below. You will need to provide your Google API Key for the agent's LLM.

    ```env
    # PostgreSQL Credentials
    POSTGRES_DB=ecommercedb
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=secret

    # Google Gemini LLM Credentials
    GOOGLE_API_KEY=...
    GOOGLE_GEMINI_MODEL=gemini-2.5-flash

    # MCP Server URL (as seen from the UI container)
    MCP_SERVER_URL=http://mcp_server:8000
    ```

3.  **Build and run the services:**
    From the root directory, run the following command:
    ```bash
    docker-compose up --build
    ```

4.  **Interact with the Chatbot:**
    Open your web browser and navigate to `http://localhost:8501`. You can now chat with the e-commerce assistant!

## 🐳 Docker Compose Services

The `docker-compose.yaml` file orchestrates the three main services of this demo:

-   **`postgresdb`**:
    -   A PostgreSQL database service using the `postgres:16` image.
    -   It stores all the application data for users, products, and orders.
    -   On startup, it runs the `data/init.sql` script to create the necessary tables and populate them with initial data.
    -   Data is persisted in a Docker volume (`postgres_data`) to survive container restarts.
    -   A health check is configured to ensure the `mcp_server` only starts after the database is ready.

-   **`mcp_server`**:
    -   The core backend service, built from the `mcp_server/` directory.
    -   It runs the FastMCP server, which exposes a set of tools and resources for the AI agent.
    -   It depends on the `postgresdb` service being healthy before it starts.
    -   The server is accessible on port `8000` within the Docker network.

-   **`ui`**:
    -   A Streamlit web application, built from the `ui/` directory.
    -   It provides a user-friendly chat interface to interact with the agent.
    -   It depends on the `mcp_server` to be running, as it connects to it to fetch tools and execute agent requests.
    -   The UI is accessible on your local machine at port `8501`.

## 📂 Project Structure

### `data/`

This folder contains the initial dataset and the database schema.

-   **`users.json`, `products.json`, `orders.json`**: These JSON files contain fake data for 10 users, 20 sports cars, and 30 orders.
-   **`init.sql`**: This SQL script is executed when the `postgresdb` container starts. It creates the `users`, `products`, and `orders` tables and populates them with the data from the corresponding JSON files.

### `mcp_server/`

This directory contains the implementation of the MCP server using `FastMCP`. It's designed to be modular and scalable.

-   **`main.py`**: The main entry point for the server. It creates a primary `FastMCP` application and mounts the individual servers for `users`, `products`, and `orders` under their respective prefixes (`/users`, `/products`, `/orders`).
-   **`backend.py`**: Contains shared, reusable components:
    -   `@db_connector`: A decorator that handles the lifecycle of a database connection (open, commit, close) for any function it wraps.
    -   `@handle_errors`: A decorator that provides robust error handling. It wraps all tool and resource functions, catching any exceptions and returning a standardized JSON error response that the agent can understand and explain.
    -   `parse_output`: A utility function to convert raw database cursor results into clean lists of dictionaries.
-   **`servers/`**: This directory holds the logic for each domain, separated into modules.
    -   Each subdirectory (`users/`, `products/`, `orders/`) contains:
        -   `server.py`: Defines the MCP interface. It uses `@server.tool` to expose functions the agent can call (e.g., `add_new_user`) and `@server.resource` to expose data endpoints (e.g., `data://users`) that can be queried.
        -   `helpers.py`: Contains the business logic and database interaction code, keeping the `server.py` file clean and focused on the API definition.
        -   Pydantic models for data validation.

### `ui/`

This directory contains the Streamlit frontend application for the chatbot.

-   **`main.py`**: The main Streamlit application file. It sets up the page configuration, title, and chat interface. It manages the display of the conversation history and handles user input. It uses `asyncio` to handle the asynchronous agent calls.
-   **`bot.py`**: This file contains the core logic for the AI agent.
    -   The `initialize_agent` function sets up the agent.
    -   It uses `langchain_mcp_adapters.MultiServerMCPClient` to connect to our `mcp_server` and dynamically fetch all the available tools.
    -   It constructs an `AgentExecutor` using `langchain.agents.create_tool_calling_agent`, providing it with a `ChatGoogleGenerativeAI` LLM, a system prompt, and the tools from the MCP server.

## 🤖 Example Agent Interactions

Once the application is running, you can try asking the assistant questions like:

-   "List all available products."
-   "Show me the details for product 'prod_c6a7b8d9'."
-   "Who are our customers? List their names and IDs."
-   "What is Tony Stark's purchase history?"
-   "Create a new order for Bruce Wayne for one 'prod_a1b2c3d4'."
-   "Add a new user named 'Peter Parker' with email 'p.parker@dailybugle.com'."
