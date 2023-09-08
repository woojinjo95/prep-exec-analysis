from dataclasses import dataclass
from typing import List

# Mock data
class IGMPJoin:
    def __init__(self, timestamp, src, dst, channel_info):
        self.timestamp = timestamp
        self.src = src
        self.dst = dst
        self.channel_info = channel_info

class ChannelKeyInput:
    def __init__(self, timestamp, key):
        self.timestamp = timestamp
        self.key = key


@dataclass
class ChannelZappingEventData:
    event_time: float
    key: str = ''
    src: str = ''
    dst: str = ''
    channel_name: str = ''



igmp_join_infos = [
    IGMPJoin(10, 'src1', 'dst1', 'channel1'),
    IGMPJoin(20, 'src2', 'dst2', 'channel2'),
    IGMPJoin(30, 'src3', 'dst3', 'channel3'),
]

channel_key_inputs = [
    ChannelKeyInput(8, 'key1'),
    ChannelKeyInput(9, 'key2'),
    ChannelKeyInput(19, 'key3'),
    ChannelKeyInput(21, 'key4'),
    ChannelKeyInput(28, 'key5'),
    ChannelKeyInput(32, 'key6')
]


def get_channel_zapping_event_infos(igmp_join_infos: List[IGMPJoin], channel_key_inputs: List[ChannelKeyInput], 
                                    igmp_join_time_margin: int) -> List[ChannelZappingEventData]: 
    i, j = 0, 0
    n, m = len(igmp_join_infos), len(channel_key_inputs)

    event_times = []

    while i < n and j < m:
        igmp_join = igmp_join_infos[i]
        channel_key_input = channel_key_inputs[j]
        
        last_fitting_input = None  # To keep track of the last fitting channel_key_input
        
        while j < m and channel_key_input.timestamp <= igmp_join.timestamp:

            if channel_key_input.timestamp >= igmp_join.timestamp - igmp_join_time_margin:
                last_fitting_input = channel_key_input  # Update last fitting input
                
            j += 1  # Move to next channel_key_input
            if j < m:
                channel_key_input = channel_key_inputs[j]
                
        if last_fitting_input is not None:  # If a fitting input was found, store it
            event_times.append(ChannelZappingEventData(
                event_time=last_fitting_input.timestamp,
                key=last_fitting_input.key,
                src=igmp_join.src,
                dst=igmp_join.dst,
                channel_name=igmp_join.channel_info,
            ))
                            
        i += 1  # Move to next igmp_join
    
    return event_times


event_infos = get_channel_zapping_event_infos(igmp_join_infos, channel_key_inputs, 5)


# Output
for event_info in event_infos:
    print(event_info.event_time)
