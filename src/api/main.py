import hashlib
import json
import threading

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from kafka import KafkaConsumer, KafkaProducer

app = FastAPI()

producer = KafkaProducer(bootstrap_servers="localhost:9093", value_serializer=lambda v: json.dumps(v).encode("utf-8"))

# Store solutions in memory # FIXME:
solutions = {}


# Pydantic model for the problem request
class ProblemRequest(BaseModel):
    problem: str


# Generate a hash for the problem text
def generate_hash(problem_text):
    return hashlib.sha256(problem_text.encode("utf-8")).hexdigest()


# Configure Kafka Consumer to listen for solutions
def consume_solutions():
    consumer = KafkaConsumer(
        "math-solutions",  # Topic to listen for solutions
        bootstrap_servers="localhost:9093",
        group_id="math-solution-listener",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    for message in consumer:
        solution_data = message.value
        problem_hash = solution_data["problem_hash"]
        problem = solution_data["problem"]
        solution = solution_data["solution"]
        solutions[problem_hash] = {"problem": problem, "solution": solution}  # Store solution in memory
        print(f"Solution for {problem_hash}: {solution}")


# Run the consumer in a background thread
thread = threading.Thread(target=consume_solutions, daemon=True)
thread.start()


@app.post("/submit-problem/")
async def submit_problem(problem_request: ProblemRequest):
    """
    Accepts a math problem from the user and sends it to Kafka.
    If the problem has already been solved, returns the cached solution.
    """
    problem_hash = generate_hash(problem_request.problem)

    # Check if solution already exists
    if problem_hash in solutions:
        return {
            "message": "Problem already solved",
            "problem": solutions[problem_hash]["problem"],
            "problem_hash": problem_hash,
        }

    # If not solved, send to Kafka
    message = {"problem": problem_request.problem, "problem_hash": problem_hash}
    producer.send("math-problems", message)
    producer.flush()
    return {"message": "Problem sent to Kafka", "problem": problem_request.problem, "problem_hash": problem_hash}


@app.get("/get-solution/{problem_hash}")
async def get_solution(problem_hash: str):
    """
    Retrieve the solution for the given problem hash from Kafka.
    """
    if problem_hash in solutions:
        return {"problem": solutions[problem_hash]["problem"], "solution": solutions[problem_hash]["solution"]}
    else:
        return {"message": "Solution not yet available"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
