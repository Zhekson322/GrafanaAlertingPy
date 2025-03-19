import psycopg2

def fetch_and_delete_resolved_alerts(conn):
    try:
        # Подключение к базе данных
        cursor = conn.cursor()
        # Выборка записей со статусом "Resolved"
        cursor.execute("""
            SELECT descriptions
            FROM grafana_table
            WHERE status = 'resolved';
        """)
        resolved_descriptions = cursor.fetchall()

        # Для каждого описания из "Resolved" ищем записи со статусом "Firing"
        for desc in resolved_descriptions:
            description = desc[0]
            cursor.execute("""
                DELETE FROM grafana_firing
                WHERE descriptions = %s AND status = 'firing';
            """, (description,))
            print("Отладка " + description)
            conn.commit()  # Фиксируем изменения


    except Exception as e:
        print(f"Ошибка при удаление firing-resolve в db_delete: {e}")