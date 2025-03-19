import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
from db_delete import fetch_and_delete_resolved_alerts

# Загрузка переменных из .env-файла
load_dotenv()

# Получение значений
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': 5432
}

def create_table_if_not_exists():
    """
    Создает таблицу, если она не существует.
    """
    query = """
    CREATE TABLE IF NOT EXISTS grafana_table (
        id SERIAL PRIMARY KEY,
        title TEXT,
        status TEXT,
        alertname TEXT,
        descriptions TEXT,
        sourceURL TEXT,
        dashboardURL TEXT,
        panelURL TEXT,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

def insert_alert_data(title, status,alertname,description,sourceURL,dashboardURL,panelURL):
    query = """
    INSERT INTO grafana_table (title,status,alertname,descriptions,sourceurl,dashboardurl,panelurl)
    VALUES (%s, %s, %s,%s, %s, %s,%s);
    """
    query_grafana_firing= """
    INSERT INTO grafana_firing (title,status,alertname,descriptions,sourceurl,dashboardurl,panelurl)
    VALUES (%s, %s, %s,%s, %s, %s,%s);
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (title, status,alertname,description,sourceURL,dashboardURL,panelURL))
                conn.commit()
                if status == "firing":
                    cursor.execute(query_grafana_firing,(title, status, alertname, description, sourceURL, dashboardURL, panelURL))
                conn.commit()
                if status == "resolved":
                    fetch_and_delete_resolved_alerts(conn)
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")