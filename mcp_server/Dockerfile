# Use the official Python image.
FROM python:3.13-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Expose the port that the MCP server will run on.
EXPOSE 8000

# Specify the command to run on container startup.
# Uvicorn is a lightning-fast ASGI server.
CMD ["python", "main.py"]