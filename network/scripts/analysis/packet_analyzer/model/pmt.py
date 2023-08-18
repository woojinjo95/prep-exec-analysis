from .model import pmt_descriptor


def es_info_descriptor_data_parser(tag: int, data: bytes) -> str:
    if tag == 0x0a:
        data_decoded = f'langauge_code: {data[:3].decode()} / type: {data[3]}'
    else:
        data_decoded = data.hex()
    return data_decoded


def es_info_parser(es_info_bytes: bytes) -> dict:
    es_info = {}
    while len(es_info_bytes) > 2:
        tag, length, data = es_info_bytes[0], es_info_bytes[1], es_info_bytes[2: 2 + es_info_bytes[1]]

        es_info[tag] = {'tag': pmt_descriptor[tag],
                        'data': es_info_descriptor_data_parser(tag, data)}
        es_info_bytes = es_info_bytes[length + 2:]
    return es_info
