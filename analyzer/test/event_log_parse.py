import datetime
from typing import List, Dict


event_result = {'items': [{'data': {'scenario_id': '5e731960-616a-436e-9cad-84fdbb39bbf4',
'testrun_id': '2023-08-14T054428F718593',
'workspace_path': './data/workspace/testruns'},
'msg': 'workspace',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 6, 597000)},
{'data': {'control': 'start'},
'msg': 'stb_log',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 6, 597000)},
{'data': {'action': 'start'},
'msg': 'streaming',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 6, 598000)},
{'data': {'log': 'Already streaming service Started',
'state': 'streaming'},
'msg': 'streaming_response',
'service': 'media',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 6, 601000)},
{'data': {'key': 'Power',
'name': 'sk',
'press_time': 0,
'type': 'ir'},
'msg': 'remocon_transmit',
'service': 'frontend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 10, 165000)},
{'data': {'key': 'Power',
'press_time': 0,
'sensor_time': 1692596171.117575,
'type': 'ir'},
'msg': 'remocon_response',
'service': 'control',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 11, 207000)},
{'data': {'scenario_id': '5e731960-616a-436e-9cad-84fdbb39bbf4',
'testrun_id': '2023-08-14T054428F718593',
'workspace_path': './data/workspace/testruns'},
'msg': 'workspace',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 11, 278000)},
{'data': {'control': 'start'},
'msg': 'stb_log',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 11, 278000)},
{'data': {'action': 'start'},
'msg': 'streaming',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 11, 279000)},
{'data': {'log': 'Already streaming service Started',
'state': 'streaming'},
'msg': 'streaming_response',
'service': 'media',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 11, 283000)},
{'data': {'key': 'Power',
'name': 'sk',
'press_time': 0,
'type': 'ir'},
'msg': 'remocon_transmit',
'service': 'frontend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 20, 437000)},
{'data': {'key': 'Power',
'press_time': 0,
'sensor_time': 1692596181.3712912,
'type': 'ir'},
'msg': 'remocon_response',
'service': 'control',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 21, 460000)},
{'data': {'scenario_id': '5e731960-616a-436e-9cad-84fdbb39bbf4',
'testrun_id': '2023-08-14T054428F718593',
'workspace_path': './data/workspace/testruns'},
'msg': 'workspace',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 21, 511000)},
{'data': {'control': 'start'},
'msg': 'stb_log',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 21, 512000)},
{'data': {'action': 'start'},
'msg': 'streaming',
'service': 'backend',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 21, 512000)},
{'data': {'log': 'Already streaming service Started',
'state': 'streaming'},
'msg': 'streaming_response',
'service': 'media',
'timestamp': datetime.datetime(2023, 8, 21, 5, 36, 21, 515000)}]}


def get_remocon_times(event_result: Dict) -> List[float]:
    remocon_times = []
    for item in event_result.get('items', []):
        service = item.get('service', '')
        msg = item.get('msg', '')
        data = item.get('data', {})
        key = data.get('key', '')
        if service == 'control' and msg == 'remocon_response' and key == 'Power':
            try:
                sensor_time = data['sensor_time']
                remocon_times.append(sensor_time)
            except KeyError:
                pass
    return remocon_times

remocon_times = get_remocon_times()
print(f'remocon_times: {remocon_times}')
