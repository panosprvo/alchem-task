import requests
import random
import time

api_url = 'http://localhost:5000/simulate'


def simulate_event():
    object_id = f"obj-{random.randint(1, 10)}"
    status = random.choice(['active', 'inactive', 'error'])
    response = requests.post(api_url, json={'object_id': object_id, 'status': status})
    print(f'Simulated event: {response.json()}')


if __name__ == '__main__':
    while True:
        simulate_event()
        time.sleep(5)  # Simulate an event every 5 seconds
