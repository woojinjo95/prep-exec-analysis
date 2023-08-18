from .model.model import mpeg2_stream_type
from .model.pmt import es_info_parser


def check_rtp_sequence(ip_dict: dict, info: tuple) -> bool:
    rtp_error = False
    current_rtp_sequence = info[0]
    if current_rtp_sequence < 0:
        # packet have not rtp layers.
        pass
    else:
        if (ip_dict['rtp_sequence'] + 1) % 0x10000 != current_rtp_sequence and ip_dict['rtp_sequence'] > 0:
            rtp_error = True
            ip_dict['rtp_errors'] += 1
        ip_dict['rtp_sequence'] = current_rtp_sequence

    return rtp_error


def check_iso_iec_structure(ip_dict: dict, timestamp: float, info: tuple):
    pid_values = info[1]
    pat_error = False
    pmt_error = False
    pid_error = False

    for (sync_byte, pid, ts_scramble, adaptation, cc, iso_iec_13818_1_bytes) in pid_values:

        # sync
        if sync_byte != 0x47:
            ip_dict['errors']['sync_bytes'] += 1
            ip_dict['errors']['ts_consecutive'] += 1
            if ip_dict['errors']['ts_consecutive'] > 2:
                ip_dict['errors']['ts_consecutive'] = 0
                ip_dict['errors']['ts_sync_loss'] += 1

        # PAT
        if pid == 0x0:
            ip_dict['timer']['pat'] = timestamp
            if ts_scramble >= 0b10 or iso_iec_13818_1_bytes[5] != 0x0:
                # PAT is scrambled
                # Table id (iso_iec_13818_1_bytes[5]) is not zero
                pat_error = True

            pmt_pid = (iso_iec_13818_1_bytes[15] & 0b00011111) * 256 + iso_iec_13818_1_bytes[16]
            if pmt_pid not in ip_dict['stream_info']['pmt'].keys():
                ip_dict['stream_info']['pmt'][pmt_pid] = {}

        # PMT
        elif pid in ip_dict['stream_info']['pmt'].keys():
            # PMT listed in the PAT is missing
            ip_dict['timer']['pmt'] = timestamp
            if ts_scramble >= 0b10 or iso_iec_13818_1_bytes[5] != 0x02:
                # PMT is scrambled
                # the table ID a PMT is not 2
                pmt_error = True

            program_map_table_length = 4 + (iso_iec_13818_1_bytes[6] & 0b1111) * 256 + iso_iec_13818_1_bytes[7]
            program_number = iso_iec_13818_1_bytes[8] * 256 + iso_iec_13818_1_bytes[9]
            program_info_length = iso_iec_13818_1_bytes[16]
            ip_dict['stream_info']['pmt'][pid]['program_number'] = program_number
            pmt_payload = iso_iec_13818_1_bytes[1 + 16 + program_info_length:program_map_table_length]

            while len(pmt_payload) > 4:
                stream_type, program_pid = pmt_payload[0], (pmt_payload[1] & 0b11111) * 256 + pmt_payload[2]
                if program_pid not in ip_dict['stream_info']['pid']:
                    ip_dict['stream_info']['pid'][program_pid] = {'stream_type_id': stream_type,
                                                                  'stream_type': mpeg2_stream_type[stream_type],
                                                                  'descriptor': es_info_parser(pmt_payload[5:5+pmt_payload[4]]),
                                                                  'count': 0}

                es_info_length = pmt_payload[4]
                pmt_payload = pmt_payload[1 + 4 + es_info_length:]

        # pid & CC
        elif adaptation % 2 == 1 and pid in ip_dict['stream_info']['pid'].keys():
            # pid
            ip_dict['stream_info']['pid'][pid]['count'] += 1
            if pid in ip_dict['continuous_count'].keys():
                if (ip_dict['continuous_count'][pid] + 1) % 0x10 != cc and pid:
                    ip_dict['errors']['continuous_count'][pid] += 1
            else:
                ip_dict['errors']['continuous_count'][pid] = 0

            ip_dict['continuous_count'][pid] = cc

        # timeout check
        if timestamp > ip_dict['timer']['pat'] + 0.5:
            # PAT error
            # PAT is missing
            # PAT repitition rate is greater than 500 ms
            ip_dict['timer']['pat'] = timestamp
            pat_error = True

        if timestamp > ip_dict['timer']['pmt'] + 0.5:
            # PMT error
            # a section of the PMT is not repeated after 500ms at the latest
            ip_dict['timer']['pmt'] = timestamp
            pmt_error = True

    if pat_error:
        ip_dict['errors']['pat'] += 1

    if pmt_error:
        ip_dict['errors']['pmt'] += 1
