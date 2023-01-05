# --> Building Stage
FROM python:3.10-slim AS builder

RUN apt-get update
RUN apt-get install -y libpq-dev gcc \
    musl-dev libffi-dev musl-dev g++

# Create & Activate Virtual Env
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Poetry and Requirements
RUN pip install poetry
COPY pyproject.toml poetry.lock .
# Because Poetry sometimes has issues with Docker, we revert back to PIP
RUN poetry export -f requirements.txt --output requirements.txt
#COPY requirements.txt .
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt


# --> Operational Stage
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq-dev python3-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Move from builder to this image
COPY --from=builder /opt/venv /opt/venv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /code
COPY . /code/

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
