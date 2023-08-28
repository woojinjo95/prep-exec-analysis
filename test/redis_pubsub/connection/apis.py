import requests


def new_scenario():
    payload = {
        "is_active": True,

    }
    requests.post('http://localhost:5000/api/v1/scenario', json=payload)
