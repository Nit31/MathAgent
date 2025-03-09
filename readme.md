# Math agent

This project aims to develop an LLM agent capable of efficiently solving multi-step math problems through a multi-phase experimental approach.

## Installation
1) Prerequisites
    - Docker and Docker Compose installed
    - Python 3.10+ installed
    - Git installed

2) Clone the repository
```
git clone https://github.com/Nit31/MathAgent.git
cd MathAgent
```

3) Set up environment variables
    - Copy the example .env file with `cp .env.example .env`
    - Edit the .env file with your API keys and configuration

4) Build and start the services
```
docker-compose up -d
```

5) Install Python dependencies (will be containerized later)
```
pip install -r requirements.txt
```

6) Start the servers
```
./scripts/start_api.sh
./scripts/start_kafka.sh
```

7) Now the API is accessible on `http://127.0.0.1:8000`

## Usage 

You can find usage examples in the Jupyter notebook at [request.ipynb](experiments/request.ipynb) 

## API Endpoints

`POST /submit-problem/`

**Request:**
| Field | Type | Description |
|-------|------|-------------|
| `problem` | string | Math problem to solve |

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| `message` | string | Status message |
| `problem` | string | Original problem |
| `problem_hash` | string | Unique problem identifier |

`GET /get-solution/{problem_hash}`

**Path Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `problem_hash` | string | Problem identifier |

**Response (when available):**
| Field | Type | Description |
|-------|------|-------------|
| `problem` | string | Original problem |
| `solution` | string | Problem solution |

**Response (when pending):**
| Field | Type | Description |
|-------|------|-------------|
| `message` | string | "Solution not yet available" |
