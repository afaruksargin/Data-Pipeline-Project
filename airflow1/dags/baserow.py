from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago, datetime
import csv
import requests
import time
import os
import sys

parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)

def add_row_to_baserow(row, token):
    response = requests.post(
        "https://api.baserow.io/api/database/rows/table/253809/?user_field_names=true",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        },
        json=row
    )
    if response.status_code == 200:
        print("İstek başarılı.")
    elif response.status_code == 201:
        print("Yeni kayıt başarıyla oluşturuldu.")
    else:
        print(f"İstek başarısız. HTTP yanıt kodu: {response.status_code}")
        print(response.text)

def main():
    token = "JTryCIhKDigI8jbBErvEE8MMjw9ODUUL"

    while True:
        with open("./data/vgsales.csv", "r", newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)  # CSV dosyasındaki tüm satırları al
            if not rows:
                print("CSV dosyasında veri bulunmuyor. 10 dakika sonra tekrar kontrol edilecek.")
                break
            
            # İlk satırı işle ve Baserow'a ekle
            record = {
                "Rank": rows[0]["Rank"],
                "Name": rows[0]["Name"],
                "Platform": rows[0]["Platform"],
                "Year": rows[0]["Year"],
                "Genre": rows[0]["Genre"],
                "Publisher": rows[0]["Publisher"],
                "NA_Sales": rows[0]["NA_Sales"],
                "EU_Sales": rows[0]["EU_Sales"],
                "JP_Sales": rows[0]["JP_Sales"],
                "Other_Sales": rows[0]["Other_Sales"],
                "Global_Sales": rows[0]["Global_Sales"]
            }
            add_row_to_baserow(record, token)
            
            # İlk satırı CSV dosyasından sil
            rows = rows[1:]

        # CSV dosyasındaki satırları güncellenmiş haliyle tekrar yaz
        with open("./data/vgsales.csv", "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

with DAG(
    dag_id = "upload_csv_to_kafka",
    description='Baserow Data DAG',
    schedule_interval='*/10 * * * *',
    start_date=datetime(2024, 2, 15, 15, 40),
    tags=['baserow'],
) as dag:
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')  
    
    consumer_task=PythonOperator(
        task_id="consumer_task",
        python_callable=main
    )
        
    start >> consumer_task >> end