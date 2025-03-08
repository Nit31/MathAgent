# consumer.py

from kafka import KafkaConsumer, KafkaProducer
import json

# Configure Kafka Consumer
consumer = KafkaConsumer(
    'math-problems',
    bootstrap_servers='localhost:9093',
    group_id='math-agent',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Configure Kafka Producer to send solution back to a different topic
producer = KafkaProducer(
    bootstrap_servers='localhost:9093',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Listen for messages and process them
for message in consumer:
    problem = message.value['problem']
    print(f"Received problem: {problem}")
    
    try:
        solution = str(eval(problem))  # Not secure, just for demo purposes
        print(f"Solution: {solution}")

        # Send solution to the 'math-solutions' topic
        solution_message = {"problem": problem, "solution": solution}
        producer.send('math-solutions', solution_message)
        producer.flush()  # Ensure the message is sent

    except Exception as e:
        print(f"Error solving problem: {e}")
