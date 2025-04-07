FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY src .

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "math_solver.consumer"]
