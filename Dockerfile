FROM python:3.13-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy project metadata first (for dependency caching)
COPY pyproject.toml ./

# Install dependencies (including pydantic[email])
RUN uv sync

# Copy application code
COPY app ./app
COPY tests ./tests

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
