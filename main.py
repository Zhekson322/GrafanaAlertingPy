from flask import Flask, request, jsonify
import json
from db_utils import create_table_if_not_exists, insert_alert_data

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if request.method == 'POST':
        # Получаем данные из запроса
        data = request.get_json()
        # Преобразуем данные в читаемый формат
        pretty_data = json.dumps(data, indent=4)
        # Выводим данные в консоль
        #("Received webhook from Grafana:")
        print(pretty_data)
        title = data.get('title')
        alerts = data.get('alerts',[])
        for alert in alerts:
            status = alert.get('status')
            alertname = alert.get("labels")
            alertname = json.dumps(alertname, ensure_ascii=False)  # поле попробовать в одну строку
            description = alert.get('annotations', {}).get('description')
            sourceURL = alert.get('generatorURL')
            dashboardURL = alert.get('dashboardURL')
            panelURL = alert.get('panelURL')
            insert_alert_data(title, status, alertname, description, sourceURL, dashboardURL, panelURL)

        #title = data.get('title')
        #status = data.get('alerts', [{}])[0].get('status')
        #alertname = data.get('alerts', [{}])[0].get('labels')
        #alertname = json.dumps(alertname,ensure_ascii=False) #поле попробовать в одну строку
        #description = data.get('alerts', [{}])[0].get('annotations', {}).get('description')
        #sourceURL = data.get('alerts', [{}])[0].get('generatorURL')
        #dashboardURL = data.get('alerts', [{}])[0].get('dashboardURL')
        #panelURL = data.get('alerts', [{}])[0].get('panelURL')
        #insert_alert_data(title, status,alertname,description,sourceURL,dashboardURL,panelURL)

        return jsonify({"message": "Webhook received successfully"}), 200
    else:
        return jsonify({"error": "Произошла ошибка 405"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)