inverse_key_map = {'KEYCODE_1': ['1', 'num1'],
                   'KEYCODE_2': ['2', 'num2'],
                   'KEYCODE_3': ['3', 'num3'],
                   'KEYCODE_4': ['4', 'num4'],
                   'KEYCODE_5': ['5', 'num5'],
                   'KEYCODE_6': ['6', 'num6'],
                   'KEYCODE_7': ['7', 'num7'],
                   'KEYCODE_8': ['8', 'num8'],
                   'KEYCODE_9': ['9', 'num9'],
                   'KEYCODE_0': ['0', 'num0'],
                   #    'KEYCODE_DEL',
                   #    'KEYCODE_POUND',
                   #    'KEYCODE_SEARCH',
                   #    'KEYCODE_BOOKMARK',
                   'KEYCODE_MENU': ['menu'],
                   #    'KEYCODE_SKB_FUNC_02',
                   #    'KEYCODE_SKB_FUNC_03',
                   #    'KEYCODE_SKB_FUNC_04',
                   #    'KEYCODE_SKB_FUNC_05',
                   #    'KEYCODE_SKB_FUNC_06',
                   #    'KEYCODE_SKB_FUNC_07',
                   #    'KEYCODE_SKB_FUNC_08',
                   #    'KEYCODE_SKB_FUNC_09',
                   #    'KEYCODE_SKB_FUNC_10',
                   #    'KEYCODE_SKB_FUNC_11',
                   #    'KEYCODE_SKB_FUNC_12',
                   'KEYCODE_VOLUME_MUTE': ['mute', '조용히'],
                   'KEYCODE_VOLUME_DOWN': ['volumedown', '음량 ↓'],
                   'KEYCODE_VOLUME_UP': ['volumeup', '음량 ↑'],
                   'KEYCODE_CHANNEL_UP': ['channelup', '채널 ↑'],
                   'KEYCODE_CHANNEL_DOWN': ['channeldown', '채널 ↓'],
                   'KEYCODE_DPAD_UP': ['up', '↑'],
                   'KEYCODE_DPAD_LEFT': ['left', '←'],
                   'KEYCODE_DPAD_RIGHT': ['right', '→'],
                   'KEYCODE_DPAD_DOWN': ['down', '↓'],
                   'KEYCODE_DPAD_CENTER': ['ok'],
                   'KEYCODE_BACK': ['back', '이전'],
                   'KEYCODE_HOME': ['home'],
                   #    'KEYCODE_SKB_FUNC_01',
                   #    'KEYCODE_ASSIST',
                   #    'KEYCODE_MEDIA_PREVIOUS',
                   #    'KEYCODE_MEDIA_NEXT',
                   #    'KEYCODE_MEDIA_PLAY_PAUSE',
                   #    'KEYCODE_MEDIA_STOP',
                   #    'KEYCODE_MEDIA_REWIND',
                   #    'KEYCODE_MEDIA_FAST_FORWARD',
                   #    'KEYCODE_SKB_FUNC_13',
                   #    'KEYCODE_SKB_FUNC_14',
                   #    'KEYCODE_SKB_FUNC_15',
                   #    'KEYCODE_SKB_FUNC_16',
                   #    'KEYCODE_SKB_FUNC_17',
                   #    'KEYCODE_ENTER',
                   #    'KEYCODE_INFO',
                   #    'KEYCODE_MEDIA_STOP',
                   #    'KEYCODE_MEDIA_RECORD',
                   #    'KEYCODE_MEDIA_FAST_FORWARD',
                   #    'KEYCODE_MEDIA_REWIND',
                   #    'KEYCODE_MEDIA_STOP',
                   #    'KEYCODE_MEDIA_PLAY_PAUSE',
                   #    'KEYCODE_MEDIA_FAST_FORWARD',
                   #    'KEYCODE_SKB_FUNC_20',
                   #    'KEYCODE_SKB_FUNC_21',
                   #    'KEYCODE_SKB_FUNC_22',
                   #    'KEYCODE_SKB_FUNC_23',
                   #    'KEYCODE_SKB_FUNC_24',
                   #    'KEYCODE_SKB_FUNC_25',
                   #    'KEYCODE_TV',
                   #    'KEYCODE_CAPTIONS',
                   #    'KEYCODE_PAGE_UP',
                   #    'KEYCODE_PAGE_DOWN',
                   #    'KEYCODE_EISU',
                   #    'KEYCODE_MUHENKAN',
                   #    'KEYCODE_BUTTON_L1',
                   #    'KEYCODE_BUTTON_R1',
                   #    'KEYCODE_BUTTON_L2',
                   #    'KEYCODE_BUTTON_R2',
                   #    'KEYCODE_SKB_FUNC_32',
                   #    'KEYCODE_SKB_FUNC_33',
                   #    'KEYCODE_SKB_FUNC_34',
                   #    'KEYCODE_SKB_FUNC_35',
                   #    'KEYCODE_SKB_FUNC_36',
                   #    'KEYCODE_SKB_FUNC_37',
                   #    'KEYCODE_SKB_FUNC_38',
                   #    'KEYCODE_SKB_FUNC_39',
                   #    'KEYCODE_SKB_FUNC_40',
                   #    'KEYCODE_SKB_FUNC_41'
                   }

keymap = {}
for key, values in inverse_key_map.items():
    # 통신사마다, 같은 키라도 이름이 다르거나 기본적으로 2개씩 이름을 할당함
    # 따라서 위와 같이 리모콘 키가 아닌 같은 키 묶음으로 역으로 정의한 뒤 그것을 뒤집은 dict 이용
    # 만약 키가 겹치면 더 아래쪽 값이 우선됨.
    # 물론 ADB 키 자체를 입력하면 그대로 전달되는 함수 또한 존재함.
    for value in values:
        keymap[value] = key
