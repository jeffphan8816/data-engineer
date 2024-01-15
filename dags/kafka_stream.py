from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Jeff Phan',
    'start_date': datetime(2024, 1, 10, 14, 00)
}


def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    producer.send('user_created', 'diofjiodj')
    cur_time = time.time()
    while True:
        if time.time() > cur_time + 60:
            break
        try:
            res = fetch_data()
            producer.send('user_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            continue


def fetch_data():
    import json
    import requests
    # API_KEY = '6de6abfedb24f889e0b5f675edc50deb'
    res = requests.get(f"https://randomuser.me/api")
    res = res.json()
    return format_data(res['results'][0])


def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['email'] = res['email']
    data['gender'] = res['gender']
    data['address'] = f"{location['street']['number']} {location['street']['name']}, {location['city']}, " \
                      f"{location['state']} {location['postcode']}, {location['country']}"
    data['dob'] = res['dob']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    data['registered_on'] = res['registered']['date']
    return data


with DAG('user_automation', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    streaming_task = PythonOperator(
        task_id='streaming_data_from_api',
        python_callable=stream_data
    )

