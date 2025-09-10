FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD [".venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]