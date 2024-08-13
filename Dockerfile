# Dockerfile.generator
FROM python:3.9-slim

WORKDIR /app

COPY generator.py /app

RUN pip install flask

CMD ["python", "generator.py"]

# Dockerfile.invoker
FROM python:3.9-slim

WORKDIR /app

COPY invoker.py /app

RUN pip install flask requests redis cachetools

CMD ["python", "invoker.py"]

