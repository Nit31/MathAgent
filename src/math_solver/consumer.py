import json
import logging
import os

from kafka import KafkaConsumer, KafkaProducer

from math_solver import Solver

logging.basicConfig(level=logging.INFO)

BOOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
CONSUMER_TOPIC = os.environ.get("KAFKA_CONSUMER_TOPIC", "math-problems")
PRODUCER_TOPIC = os.environ.get("KAFKA_PRODUCER_TOPIC", "math-solutions")
CONSUMER_GROUP_ID = os.environ.get("KAFKA_CONSUMER_GROUP_ID", "math-solution-group")


def main():
    consumer = KafkaConsumer(
        CONSUMER_TOPIC,
        bootstrap_servers=BOOOTSTRAP_SERVERS,
        group_id=CONSUMER_GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    solver = Solver()

    # Configure Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=BOOOTSTRAP_SERVERS, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    # Listen for messages and process them
    for message in consumer:
        problem = message.value["problem"]
        problem_hash = message.value["problem_hash"]
        print(f"Received problem: {problem} with hash: {problem_hash}")

        try:
            response = solver.solve(problem)

            # Send solution to the 'math-solutions' topic with problem hash
            solution_message = {
                "problem": problem,
                "problem_hash": problem_hash,
                "solution": response["solution"],
                "answer": response["answer"],
            }
        except Exception as e:
            print(f"Error occurred while processing the solution: {e}")
            print(response)
            solution_message = {
                "problem": problem,
                "problem_hash": problem_hash,
                "solution": str(e),
                "answer": response,
            }
        producer.send(PRODUCER_TOPIC, solution_message)
        producer.flush()  # Ensure the message is sent

        # except Exception as e:
        #     print(f"Error solving problem: {e}")


if __name__ == "__main__":
    logging.info("Starting Kafka consumer for math problems...")

    main()
