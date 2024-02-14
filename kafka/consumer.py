from kafka import KafkaConsumer
import psycopg2
from psycopg2 import sql
import json

def consume_and_store_messages(bootstrap_servers, topic_name, group_id, database_info):
    # Kafka consumer'ı oluşturma
    consumer = KafkaConsumer(
        topic_name,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',  # En eski mesajdan başlayarak oku
        enable_auto_commit=True,       # Otomatik commit et
        auto_commit_interval_ms=1000,   # Otomatik commit aralığı (milisaniye cinsinden)
        value_deserializer=lambda x: x.decode('utf-8')  # Mesaj değerlerini çözümleme
    )

    # Postgres veritabanına bağlanma
    conn = psycopg2.connect(
        host=database_info['host'],
        port=database_info['port'],
        dbname=database_info['dbname'],
        user=database_info['user'],
        password=database_info['password']
    )

    try:
        # Veritabanı bağlantısını oluştur
        cursor = conn.cursor()

        # Sonsuz bir döngüde Kafka'dan mesajları oku ve Postgres'e yaz
        for message in consumer:
            print(f"Received message: {message.value}")
            data_dict = json.loads(message.value)
            try:
                # Postgres'e mesajı ekleme
                cursor.execute(
                    """
                    INSERT INTO game_sales (rank, name, platform, year, genre, publisher, na_sales, eu_sales, jp_sales, other_sales, global_sales)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data_dict.get("Rank") or None,
                        data_dict.get("Name") or None,
                        data_dict.get("Platform") or None,
                        data_dict.get("Year") or None,
                        data_dict.get("Genre") or None,
                        data_dict.get("Publisher") or None,
                        data_dict.get("NA_Sales") or None,
                        data_dict.get("EU_Sales") or None,
                        data_dict.get("JP_Sales") or None,
                        data_dict.get("Other_Sales") or None,
                        data_dict.get("Global_Sales") or None
                    )
                )
            except psycopg2.errors.InvalidTextRepresentation as e:
                print("Invalid text representation error:", e)
                continue

            # Değişiklikleri kaydet
            conn.commit()

    except KeyboardInterrupt:
        print("Kullanıcı tarafından kapatıldı.")
    

    finally:
        # Cursor ve bağlantıyı kapat
        cursor.close()
        conn.close()

def main():
    # Kafka broker adresi ve portu
    bootstrap_servers = '172.18.0.4:9092'

    # Topic adı
    topic_name = 'game-sales'

    # Consumer group adı
    group_id = 'my-group'

    # Postgres veritabanı bilgileri
    database_info = {
        'host': 'localhost',
        'port': '5430',
        'dbname': 'postgres',
        'user': 'admin',
        'password': 'admin'
    }

    # Kafka'dan mesajları tüketme ve Postgres'e yazma işlevini çağırma
    consume_and_store_messages(bootstrap_servers, topic_name, group_id, database_info)

if __name__ == "__main__":
    main()
