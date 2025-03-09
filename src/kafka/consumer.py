from kafka import KafkaConsumer, KafkaProducer
import json
from math_solver import Solver

# Configure Kafka Consumer
consumer = KafkaConsumer(
    'math-problems',
    bootstrap_servers='localhost:9093',
    group_id='math-agent',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

solver = Solver()

# Configure Kafka Producer to send solution back to a different topic
producer = KafkaProducer(
    bootstrap_servers='localhost:9093',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Listen for messages and process them
for message in consumer:
    problem = message.value['problem']
    problem_hash = message.value['problem_hash']
    print(f"Received problem: {problem} with hash: {problem_hash}")
    
    try:
        solution = solver.solve(problem)
        print(f"Solution: {solution}")

        # Send solution to the 'math-solutions' topic with problem hash
        solution_message = {
            "problem": problem, 
            "problem_hash": problem_hash,
            "solution": solution
        }
        producer.send('math-solutions', solution_message)
        producer.flush()  # Ensure the message is sent

    except Exception as e:
        print(f"Error solving problem: {e}")
