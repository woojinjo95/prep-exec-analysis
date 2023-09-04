import requests
import json
import time


def new_scenario():
    payload = json.loads('''{
  "is_active": true,
  "name": "string",
  "tags": [
    "this sceanario is auto maked by /service/test/start.py"
  ],
  "block_group": [
    {
      "id": "string",
      "repeat_cnt": 0,
      "block": [
        {
          "type": "remocon_transmit",
          "name": "string",
          "args": [
            {
              "key": "string",
              "value": "string"
            }
          ],
          "delay_time": 3000,
          "id": "string"
        }
      ]
    }
  ]
}''')

    payload['name'] = f'test_{time.time()}'

    res = requests.post('http://localhost:5000/api/v1/scenario', json=payload)
    print(res.json())


def get_last_scenario_id() -> str:
    res = requests.get('http://localhost:5000/api/v1/scenario')
    scenario_id = res.json()['items'][-1]['id']
    return scenario_id


def new_testrun(scenario_id: str = None):
    if scenario_id is None:
        scenario_id = get_last_scenario_id()

    res = requests.post(f'http://localhost:5000/api/v1/scenario/testrun/{scenario_id}')