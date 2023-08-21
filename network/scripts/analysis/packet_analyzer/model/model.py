from collections import defaultdict

# https://learn.microsoft.com/en-us/previous-versions/windows/desktop/mstv/mpeg2streamtype
# iso standard needed.

mpeg2_stream_type = defaultdict(lambda: 'User defined')
reserved_stream_type = {
    0x00: 'ISO/IEC Reserved',
    0x01: 'MPEG1 video',
    0x02: 'MPEG2 video',
    0x03: 'MPEG1 audio',
    0x04: 'MPEG2 audio',
    0x05: 'Private section',
    0x06: 'Private data',
    0x07: 'ISO_IEC_13522_MHEG',
    0x08: 'ANNEX_A_DSM_CC',
    0x09: 'ITU_T_REC_H_222_1',
    0x0a: 'ISO_IEC_13818_6_TYPE_A',
    0x0b: 'ISO_IEC_13818_6_TYPE_B',
    0x0c: 'ISO_IEC_13818_6_TYPE_C',
    0x0d: 'ISO_IEC_13818_6_TYPE_D',
    0x0e: 'ISO_IEC_13818_1_AUXILIARY',
    0x0f: 'AAC audio',
    0x10: 'MPEG4 video',
    0x11: 'AAC LATM audio',
    0x15: 'Metadata',
    0x1b: 'H264 video',
    0x24: 'H265 video',
    0x42: 'CAVS video',
    0x81: 'AC3 audio',
    0x82: 'DTS audio',
    0x83: 'True HD audio',
    0x86: 'SCTE35',
    0x87: 'EAC3 Audio',
    0xea: 'VC1 video',
    0xd1: 'DIRAC video',
}
mpeg2_stream_type.update(reserved_stream_type)


pmt_descriptor = defaultdict(lambda: 'Unknown')
reserved_pmt_descriptor = {
    0x52: 'Stream identifier',
    0x0a: 'ISO 639 Language',
    0x81: 'ATSC A/52 AC-3 Audio',
}
pmt_descriptor.update(reserved_pmt_descriptor)
