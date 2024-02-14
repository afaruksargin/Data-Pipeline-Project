from confluent_kafka import Producer
import json
import requests
import json
import math
import time
import producer

def get_data(url, token, page_number):
    response = requests.get(
        url,
        headers={
            "Authorization": f"Token {token}"
        }
    )
    if response.status_code != 200:
        print("İstek başarısız. HTTP kodu:", response.status_code)
        return
    data = response.json()
    results = data.get("results")
    for data_row in results:
        row_id = data_row.get('id')
        producer.kafka_producer(data_row)
        requests.delete(
            f"https://api.baserow.io/api/database/rows/table/253809/{row_id}/",
            headers={
                "Authorization": f"Token {token}"
            }
        )


def kafka_producer(data):
    
    conf = {'bootstrap.servers':'172.18.0.4:9092',
            'client.id': 'python-producer'}

    producer = Producer(conf)

    json_data = json.dumps(data)

    topic = "game-sales"

    # Veriyi Kafka'ya gönderme
    producer.produce(topic, value=json_data)

    # Asenkron mesaj iletimini başlatma
    producer.flush()

    
def main():
    token = "JTryCIhKDigI8jbBErvEE8MMjw9ODUUL"
    url_template = "https://api.baserow.io/api/database/rows/table/253809/?page={}&user_field_names=true&size=200"

    while True:
        # GET isteği gönderme
        response = requests.get(
            url_template.format(1),
            headers={"Authorization": f"Token {token}"}
        )

        # Yanıtı kontrol etme
        if response.status_code == 200:
            # Başarılı yanıt alındıysa JSON verisini al
            data = response.json()
            count_data = data.get("count")
            for page_number in range(1, math.ceil(count_data / 200) + 1):
                url = url_template.format(page_number)
                get_data(url, token, page_number)
        else:
            print("İstek başarısız. HTTP kodu:", response.status_code)
            print(response.text)




if __name__ == "__main__":
    main()