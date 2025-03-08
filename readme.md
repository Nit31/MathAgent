# Math agent

## How to run
1) `docker-compose up`
2) `python consumer.py`
3) `uvicorn main:app --reload`

## Example usage
```
import requests

base_url = "http://127.0.0.1:8000"

# Submit a math problem to the API
def submit_problem(problem):
    response = requests.post(f"{base_url}/submit-problem/", json={"problem": problem})
    if response.status_code == 200:
        print("Problem submitted:", response.json())
    else:
        print("Failed to submit problem:", response.text)


# Get the solution for a specific problem
def get_solution(problem):
    response = requests.get(f"{base_url}/get-solution/{problem}")
    if response.status_code == 200:
        print("Solution:", response.json())
    else:
        print("Failed to retrieve solution:", response.text)

# Example usage
problem = "2 + 2"
submit_problem(problem)
get_solution(problem)
```

## Repo structure:
```
math-solving-agent/
├── README.md                   # Project overview and setup instructions
├── docker-compose.yml           # Docker Compose configuration for Kafka and services
├── config/                      # Configuration files
│   └── kafka_config.yaml        # Kafka connection details (topic names, brokers)
│   └── agent_config.yaml       # Configuration for the math solver (e.g., OpenAI settings)
├── src/                         # Source code for the agent
│   ├── __init__.py              # Init file for the package
│   ├── api/                     # API layer (e.g., FastAPI or Flask)
│   │   ├── __init__.py
│   │   ├── main.py              # API entry point
│   │   ├── routes.py            # API routes (endpoints)
│   │   └── models.py            # API request/response models
│   ├── kafka/                   # Kafka consumer and producer
│   │   ├── __init__.py
│   │   ├── producer.py          # Kafka producer (sending messages to Kafka)
│   │   ├── consumer.py          # Kafka consumer (reading from Kafka and sending results)
│   │   └── utils.py             # Utility functions for Kafka message handling
│   ├── math_solver/             # Math-solving logic
│   │   ├── __init__.py
│   │   ├── solver.py            # Core math solving functionality (using OpenAI or other models)
│   │   └── parser.py            # Optional: parser for mathematical expressions (if needed)
│   ├── utils/                   # Helper utilities
│       ├── __init__.py
│       ├── logger.py            # Custom logging for debugging and tracing
│       └── exceptions.py        # Custom exceptions
├── tests/                       # Unit and integration tests
│   ├── __init__.py
│   ├── test_api.py              # Tests for API routes
│   ├── test_kafka.py            # Tests for Kafka producer/consumer
│   ├── test_solver.py           # Tests for math-solving logic
│   └── test_integration.py      # End-to-end integration tests
│
├── experiments/
│   ├-README.md
│   ├──Baseline.ipynb
│
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image configuration for the agent
└── .env                         # Environment variables (API keys, Kafka brokers, etc.)
```

## Как оформляем эксперименты
- Гипотезы
- Данные
- Метолодогия
- Результаты