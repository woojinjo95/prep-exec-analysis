from pprint import pprint

from .common import convert_ip_bytes_string


def pprint_stream_dict(stream_dict: dict):
    for key, value in stream_dict.items():
        if type(value) == dict:
            print('='*100)
            if value['stream_info']['pmt'] and value['count'] > 0:
                for pid_value in value['stream_info']['pid'].values():
                    pid_value['bytes'] = pid_value.get('count', 0) * 188
                print(f'{convert_ip_bytes_string(key)}')
                pprint(value, width=120)
                print('')
            else:
                print(f'{convert_ip_bytes_string(key)} / not video stream!')
                pprint({k: v for k, v in value.items() if k in ['bytes', 'start_timestamp', 'timestamp']}, width=120)


def pprint_archived_stream_dict(stream_dict: dict):
    if stream_dict is None:
        return
    for key, value_list in stream_dict.items():
        print(f'{convert_ip_bytes_string(key)}')
        print([(value['start_timestamp'], value['timestamp']) for value in value_list])

        for value in value_list:
            if type(value) == dict:
                print('='*100)
                if value['stream_info']['pmt'] and value['count'] > 0:
                    for pid_value in value['stream_info']['pid'].values():
                        pid_value['bytes'] = pid_value.get('count', 0) * 188
                    pprint(value, width=120)
                    print('')
                else:
                    pass

def post_process_stream_dict(stream_dict: dict):
    pass
