class ASCIIKeyCodes:
    # non printable control char
    ASCII_NULL = 0x00  # 0 # NULL
    ASCII_SOH = 0x01  # 1  # start of heading
    ASCII_STX = 0x02  # 2  # start of text
    ASCII_EXT = 0x03  # 3  # end of text
    ASCII_EOT = 0x04  # 4  # end of transmission
    ASCII_EQ = 0x05  # 5  # enquiry
    ASCII_ACK = 0x06  # 6  # acknowledgement
    ASCII_BEL = 0x07  # 7  # bell
    ASCII_BS = 0x08  # 8  # back space
    ASCII_TAB = 0x09  # 9  # Horizontal tab
    ASCII_LF = 0x0A  # 10  # line feed, new line
    ASCII_VT = 0x0B  # 11  # vertical tap
    ASCII_FF = 0x0C  # 12  # NP from feed, new page
    ASCII_CR = 0x0D  # 13  # carrage return
    ASCII_SO = 0x0E  # 14  # shift out
    ASCII_SI = 0x0F  # 15  # shift in
    ASCII_DLE = 0x10  # 16  # data link escape
    ASCII_DC1 = 0x11  # 17  # device control 1
    ASCII_DC2 = 0x12  # 18  # device control 2
    ASCII_DC3 = 0x13  # 19  # device control 3
    ASCII_DC4 = 0x14  # 20  # device control 4
    ASCII_NAK = 0x15  # 21  # negative acknowledge
    ASCII_SYN = 0x16  # 22  # syncronous idle
    ASCII_ETB = 0x17  # 23  # end of transaction block
    ASCII_CAN = 0x18  # 24  # cancle
    ASCII_EM = 0x19  # 25  # end of medium
    ASCII_SUB = 0x1A  # 26  # substitute
    ASCII_ESC = 0x1B  # 27
    ASCII_FS = 0x1C  # 28  # file seperator
    ASCII_GS = 0x1D  # 29  # group seperator
    ASCII_RS = 0x1E  # 30  # record seperator
    ASCII_US = 0x1F  # 31  # unit seperator
    ASCII_SPACE = 0x20  # 32
    ASCII_DEL = 0x7F  # 127
    # Keyboard modifiers
    KEY_LEFT_CTRL = 0x80  # 128
    KEY_LEFT_SHIFT = 0x81  # 129
    KEY_LEFT_ALT = 0x82  # 130
    KEY_LEFT_GUI = 0x83  # 131
    KEY_RIGHT_CTRL = 0x84  # 132
    KEY_RIGHT_SHIFT = 0x85  # 133
    KEY_RIGHT_ALT = 0x86  # 134
    KEY_RIGHT_GUI = 0x87  # 135
    # Within the alphanumeric cluster
    KEY_TAB = 0xB3  # 179
    KEY_CAPS_LOCK = 0xC1  # 193
    KEY_BACKSPACE = 0xB2  # 178
    KEY_RETURN = 0xB0  # 176
    KEY_MENU = 0xED  # 237
    # Navigation cluster
    KEY_INSERT = 0xD1  # 209
    KEY_DELETE = 0xD4  # 212
    KEY_HOME = 0xD2  # 210
    KEY_END = 0xD5  # 213
    KEY_PAGE_UP = 0xD3  # 211
    KEY_PAGE_DOWN = 0xD6  # 214
    KEY_UP_ARROW = 0xDA  # 218
    KEY_DOWN_ARROW = 0xD9  # 217
    KEY_LEFT_ARROW = 0xD8  # 216
    KEY_RIGHT_ARROW = 0xD7  # 215
    # Numeric keypad
    KEY_NUM_LOCK = 0xDB  # 219
    KEY_KP_SLASH = 0xDC  # 220
    KEY_KP_ASTERISK = 0xDD  # 221
    KEY_KP_MINUS = 0xDE  # 222
    KEY_KP_PLUS = 0xDF  # 223
    KEY_KP_ENTER = 0xE0  # 224
    KEY_KP_1 = 0xE1  # 225
    KEY_KP_2 = 0xE2  # 226
    KEY_KP_3 = 0xE3  # 227
    KEY_KP_4 = 0xE4  # 228
    KEY_KP_5 = 0xE5  # 229
    KEY_KP_6 = 0xE6  # 230
    KEY_KP_7 = 0xE7  # 231
    KEY_KP_8 = 0xE8  # 232
    KEY_KP_9 = 0xE9  # 233
    KEY_KP_0 = 0xEA  # 234
    KEY_KP_DOT = 0xEB  # 235
    # Escape and function keys
    KEY_ESC = 0xB1  # 177
    KEY_F1 = 0xC2  # 194
    KEY_F2 = 0xC3  # 195
    KEY_F3 = 0xC4  # 196
    KEY_F4 = 0xC5  # 197
    KEY_F5 = 0xC6  # 198
    KEY_F6 = 0xC7  # 199
    KEY_F7 = 0xC8  # 200
    KEY_F8 = 0xC9  # 201
    KEY_F9 = 0xCA  # 202
    KEY_F10 = 0xCB  # 203
    KEY_F11 = 0xCC  # 204
    KEY_F12 = 0xCD  # 205
    KEY_F13 = 0xF0  # 240
    KEY_F14 = 0xF1  # 241
    KEY_F15 = 0xF2  # 242
    KEY_F16 = 0xF3  # 243
    KEY_F17 = 0xF4  # 244
    KEY_F18 = 0xF5  # 245
    KEY_F19 = 0xF6  # 246
    KEY_F20 = 0xF7  # 247
    KEY_F21 = 0xF8  # 248
    KEY_F22 = 0xF9  # 249
    KEY_F23 = 0xFA  # 250
    KEY_F24 = 0xFB  # 251
    # Function control keys
    KEY_PRINT_SCREEN = 0xCE  # 206 Print Screen or PrtSc / SysRq
    KEY_SCROLL_LOCK = 0xCF  # 207
    KEY_PAUSE = 0xD0  # 208 Pause / Break

class MEDIAKeyCodes:
    # KEY_MEDIA_NEXT_TRACK = 0
    # KEY_MEDIA_PREVIOUS_TRACK = 1
    # KEY_MEDIA_STOP = 2
    # KEY_MEDIA_PLAY_PAUSE = 3
    # KEY_MEDIA_MUTE = 4
    # KEY_MEDIA_VOLUME_UP = 5
    # KEY_MEDIA_VOLUME_DOWN = 6
    # KEY_MEDIA_WWW_HOME = 7
    # KEY_MEDIA_LOCAL_MACHINE_BROWSER = 8
    # KEY_MEDIA_CALCULATOR = 9
    # KEY_MEDIA_WWW_BOOKMARKS = 10
    # KEY_MEDIA_WWW_SEARCH = 11
    # KEY_MEDIA_WWW_STOP = 12
    # KEY_MEDIA_WWW_BACK = 13
    # KEY_MEDIA_CONSUMER_CONTROL_CONFIGURATION = 14
    # KEY_MEDIA_EMAIL_READER = 15
    KEY_MEDIA_POWER = 0x30
    KEY_MEDIA_UP = 0x42
    KEY_MEDIA_DOWN = 0x43
    KEY_MEDIA_LEFT = 0x44
    KEY_MEDIA_RIGHT = 0x45
    KEY_MEDIA_BACK = 0x244
    KEY_MEDIA_EXIT = 0x204
    KEY_MEDIA_MENU_HOME = 0x40
    KEY_MEDIA_VOLUME_UP = 0xe9
    KEY_MEDIA_VOLUME_DOWN = 0xea
    KEY_MEDIA_MUTE = 0xe2
    KEY_MEDIA_CHANNEL_UP = 0x9c
    KEY_MEDIA_CHANNEL_DOWN = 0x9d
    KEY_MEDIA_OK = 0x41
    KEY_MEDIA_PLAY_PAUSE = 0xcd
    KEY_MEDIA_FAST_FORWARD =0xb3
    KEY_MEDIA_REWIND = 0xb4
    KEY_MEDIA_ADVANCE = 0xb5
    KEY_MEDIA_REPLAY = 0xb6
    KEY_MEDIA_NUM_1 = 0xE1
    KEY_MEDIA_NUM_2 = 0xE2
    KEY_MEDIA_NUM_3 = 0xE3
    KEY_MEDIA_NUM_4 = 0xE4
    KEY_MEDIA_NUM_5 = 0xE5
    KEY_MEDIA_NUM_6 = 0xE6
    KEY_MEDIA_NUM_7 = 0xE7
    KEY_MEDIA_NUM_8 = 0xE8
    KEY_MEDIA_NUM_9 = 0xE9
    KEY_MEDIA_NUM_0 = 0xEA
    KEY_MEDIA_SEARCH = 0x221
    KEY_MEDIA_A_RED = 0x3d
    KEY_MEDIA_B_GREEN = 0x3e
    KEY_MEDIA_C_YELLOW = 0x3f
    KEY_MEDIA_D_BLUE = 0x40

MEDIAKeyCodesSet = set([
    # MEDIAKeyCodes.KEY_MEDIA_NEXT_TRACK,
    # MEDIAKeyCodes.KEY_MEDIA_PREVIOUS_TRACK,
    # MEDIAKeyCodes.KEY_MEDIA_STOP,
    # MEDIAKeyCodes.KEY_MEDIA_PLAY_PAUSE,
    # MEDIAKeyCodes.KEY_MEDIA_MUTE,
    # MEDIAKeyCodes.KEY_MEDIA_VOLUME_UP,
    # MEDIAKeyCodes.KEY_MEDIA_VOLUME_DOWN,
    # MEDIAKeyCodes.KEY_MEDIA_WWW_HOME,
    # MEDIAKeyCodes.KEY_MEDIA_LOCAL_MACHINE_BROWSER,
    # MEDIAKeyCodes.KEY_MEDIA_CALCULATOR,
    # MEDIAKeyCodes.KEY_MEDIA_WWW_BOOKMARKS,
    # MEDIAKeyCodes.KEY_MEDIA_WWW_SEARCH,
    # MEDIAKeyCodes.KEY_MEDIA_WWW_STOP,
    # MEDIAKeyCodes.KEY_MEDIA_WWW_BACK,
    # MEDIAKeyCodes.KEY_MEDIA_CONSUMER_CONTROL_CONFIGURATION,
    # MEDIAKeyCodes.KEY_MEDIA_EMAIL_READER,
])

class Commands:
    start = "bc011:"
    stop = "bc021:"
    write_key_code = "bc081:"
    write_media_key_code = "bc091:"
    press_key_code = "bc101:"
    press_media_key_code = "bc111:"
    release_key_code = "bc121:"
    release_media_key_code = "bc131:"
    release_all = "bc141:"
    disconnect = "bc021:"
    write_string = "bc151:" # not use

    set_delay = "bc071:"
    set_device_name = "bc031:"
    get_device_name = "bc041:"
    get_device_type = "bc051:"
    get_device_statue = "bc061:"

    long_press = "bc161:"
    repeat = "bc171:"
