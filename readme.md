# Math agent

This project aims to develop an LLM agent capable of efficiently solving multi-step math problems through a multi-phase experimental approach.

The final version of the agent replicates the implementation in `experiments/reflection_agent.ipynb`. All experiments can be found in the `experiments` folder. The detailed experiments explanation is written in [this readme](experiments/README.md) file.

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
    - Edit the .env file with your OpenAI API key

4) Build and start the services
```
docker-compose up -d
```

5) Now the API is accessible on `http://127.0.0.1:8080`

## Usage

You can find usage example in the Jupyter notebook at [example.ipynb](app/example.ipynb) 

Moreover, you can run a simple web application by following the instruction:
1) `pip install streamlit`
2) `streamlit run app/app.py`



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
