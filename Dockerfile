FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY canvas_reactive_kernel.py dag_dependency_resolver.py ./

ENV PYTHONUNBUFFERED=1
EXPOSE 8888

CMD ["python", "canvas_reactive_kernel.py"]
