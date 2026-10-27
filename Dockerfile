FROM python:3.11-slim

WORKDIR /app
COPY src /app/src
COPY pyproject.toml /app/pyproject.toml
ENV PYTHONPATH=/app/src PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir "openpyxl>=3.1,<4"
RUN mkdir -p /result
ENTRYPOINT ["python", "-m", "datamate"]
