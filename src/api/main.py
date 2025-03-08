from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer, KafkaConsumer
import json
import threading
import uvicorn

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='localhost:9093',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Store solutions in memory (for demo purposes)
solutions = {}

# Pydantic model for the problem request
class ProblemRequest(BaseModel):
    problem: str

# Configure Kafka Consumer to listen for solutions
def consume_solutions():
    consumer = KafkaConsumer(
        'math-solutions',  # Topic to listen for solutions
        bootstrap_servers='localhost:9093',
        group_id='math-solution-listener',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    for message in consumer:
        solution_data = message.value
        problem = solution_data['problem']
        solution = solution_data['solution']
        solutions[problem] = solution  # Store solution in memory
        print(f"Solution for {problem}: {solution}")

# Run the consumer in a background thread
thread = threading.Thread(target=consume_solutions, daemon=True)
thread.start()

@app.post("/submit-problem/")
async def submit_problem(problem_request: ProblemRequest):
    """
    Accepts a math problem from the user and sends it to Kafka.
    """
    message = {"problem": problem_request.problem}
    producer.send('math-problems', message)
    producer.flush()
    return {"message": "Problem sent to Kafka", "problem": problem_request.problem}

@app.get("/get-solution/{problem}")
async def get_solution(problem: str):
    """
    Retrieve the solution for the given math problem from Kafka.
    """
    if problem in solutions:
        return {"problem": problem, "solution": solutions[problem]}
    else:
        return {"message": "Solution not yet available"}
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
