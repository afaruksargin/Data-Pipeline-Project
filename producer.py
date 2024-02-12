from confluent_kafka import Producer
import json


def kafka_producer(data):
    
    conf = {'bootstrap.servers':'172.20.0.4:9092',
            'client.id': 'python-producer'}

    producer = Producer(conf)

    json_data = json.dumps(data)

    topic = "game-sales"

    # Veriyi Kafka'ya gönderme
    producer.produce(topic, value=json_data)

    # Asenkron mesaj iletimini başlatma
    producer.flush()

