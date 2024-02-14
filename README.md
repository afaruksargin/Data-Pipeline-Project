# DataProjectPipeline

# Airflow Kafka PostgreSQL Pipeline

Bu proje, Apache Airflow kullanarak bir veri boru hattı oluşturmak için Docker konteynerleri kullanır. Bu boru hattı, belirli aralıklarla bir CSV dosyasından veri okuyacak, bu verileri Kafka'ya yazacak ve ardından PostgreSQL veritabanına aktaracaktır.

## Kurulum

1. Bu depoyu klonlayın:

    ```bash
    git clone https://github.com/kullanici/adresi.git
    ```

2. Docker ve Docker Compose yüklü olmalıdır.

3. `docker-compose.yml` dosyasını düzenleyin ve gerektiğinde yapılandırın.

## Kullanım

1. Docker Compose kullanarak Airflow'u başlatın:

    ```bash
    docker-compose -f airflow1/ up -d
    ```
     ```bash
     docker-compose -f kafka/docker-compose-outher.yml  up -d
    ```

2. Tarayıcınızda Airflow arayüzüne gidin: [http://localhost:8080](http://localhost:8080)

3. Airflow arayüzünden oluşturulmuş olan DAG'ları görebilir ve çalıştırabilirsiniz.

## Veri Boru Hattı Açıklaması

- **CSV Dosyası Yükleme**: `upload_csv_to_kafka` adlı bir DAG, belirli aralıklarla bir CSV dosyasından veri okur ve bu verileri Baserow'a yazar.
  
  
- **Producer**: Baserrowdan okuduğu verileri Kafka'ya yazmak için kullanılan bir Python uygulaması.
  
- **Consumer**: Kafka'dan veri okuyan ve PostgreSQL veritabanına yazan bir Python uygulaması.




