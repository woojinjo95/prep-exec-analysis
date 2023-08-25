from scripts.device.remocon.types.bluetooth.bt_constant import ASCIIKeyCodes, MEDIAKeyCodes
from scripts.device.remocon.types.bluetooth.bt_lib import (press, press_consumer_key,
                                                           press_media_key,
                                                           long_press_media,
                                                           release_all,
                                                           release_media, 
                                                           start, stop,
                                                           write, write_string,
                                                           disconnect,
                                                           get_device_name,
                                                           get_device_status,
                                                           get_device_type)



def pairing(ser, padding, duration):
    start(ser)


def unpairing(ser, padding, duration):
    stop(ser)


def disconnecting(ser, keyname, duration):
    disconnect(ser)


def device_status(ser, keyname, duration):
    get_device_status(ser)


def device_type(ser, keyname, duration):
    get_device_type(ser)
    

def device_name(ser, keyname, duration):
    get_device_name(ser)


def _volumeup(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_VOLUME_UP)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_VOLUME_UP)


def _volumedown(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_VOLUME_DOWN)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_VOLUME_DOWN)

def _mute(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_MUTE)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_MUTE)


def _channelup(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_CHANNEL_UP)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_CHANNEL_UP)


def _channeldown(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_CHANNEL_DOWN)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_CHANNEL_DOWN)


def _volumeup_rc(ser, keyname, duration):
    press_consumer_key(ser, "0 0 1 0")
    # release_all(ser)


def _volumedown_rc(ser, keyname, duration):
    press_consumer_key(ser, "0 0 2 0")
    # release_all(ser)


def _mute_rc(ser, keyname, duration):
    press_consumer_key(ser, "0 0 4 0")
    # release_all(ser)


def _assist(ser, keyname, duration):
    press_media_key(ser, 11)
    release_media(ser, 11)


def _home(ser, keyname, duration):
    press(ser, ASCIIKeyCodes.KEY_LEFT_GUI)
    press(ser, ASCIIKeyCodes.KEY_RETURN)
    release_all(ser)


def _ok(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_OK)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_OK)


def _ok_rc(ser, keyname, duration):
    press_consumer_key(ser, "0 0 0 128")
    # release_all(ser)


def _back(ser, keyname, duration):
    press(ser, ASCIIKeyCodes.KEY_LEFT_GUI)
    write(ser, ASCIIKeyCodes.ASCII_BS)
    release_all(ser)


def _search(ser, keyname, duration):
    press(ser, ASCIIKeyCodes.KEY_LEFT_GUI)
    release_all(ser)


def _up(ser, keyname, duration=0):
    if duration == 0:
        press(ser, ASCIIKeyCodes.KEY_UP_ARROW)
    else:
        long_press_media(ser, MEDIAKeyCodes.KEY_MEDIA_UP, duration)
    release_all(ser)


def _down(ser, keyname, duration=0):
    if duration == 0:
        press(ser, ASCIIKeyCodes.KEY_DOWN_ARROW)
    else:
        long_press_media(ser, MEDIAKeyCodes.KEY_MEDIA_DOWN, duration)
    release_all(ser)


def _right(ser, keyname, duration=0):
    if duration == 0:
        press(ser, ASCIIKeyCodes.KEY_RIGHT_ARROW)
    else:
        long_press_media(ser, MEDIAKeyCodes.KEY_MEDIA_RIGHT, duration)
    release_all(ser)


def _left(ser, keyname, duration=0):
    if duration == 0:
        press(ser, ASCIIKeyCodes.KEY_LEFT_ARROW)
    else:
        long_press_media(ser, MEDIAKeyCodes.KEY_MEDIA_LEFT, duration)
    release_all(ser)


def powerkey(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_POWER)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_POWER)
    # press_consumer_key(ser, "0 0 0 1")
    # release_all(ser)


def _numberkey(ser, keyname, duration):
    if keyname == 'num1':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_1)
    elif keyname == 'num2':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_2)
    elif keyname == 'num3':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_3)
    elif keyname == 'num4':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_4)
    elif keyname == 'num5':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_5)
    elif keyname == 'num6':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_6)
    elif keyname == 'num7':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_7)
    elif keyname == 'num8':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_8)
    elif keyname == 'num9':
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_9)
    else:
        write(ser, MEDIAKeyCodes.KEY_MEDIA_NUM_0)


def _sharpkey(ser, keyname, duration):
    write_string(ser, "#")


def _asterisk(ser, keyname, duration):
    write_string(ser, "*")


def chupkey(ser, keyname, duration):
    press_consumer_key(ser, "0 0 8 0")
    # release_all(ser)


def chdownkey(ser, keynam, duration):
    press_consumer_key(ser, "0 0 16 0")
    # release_all(ser)


def exitkey(ser, keyname, duration):
    press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_EXIT)
    release_media(ser, MEDIAKeyCodes.KEY_MEDIA_EXIT)


def favkey(ser, keyname, duration):
    pass


def searchkey(ser, keyname, duration):
    pass


def tvschedulekey(ser, keyname, duration):
    pass


def markkey(ser, keyname, duration):
    pass


def multiviewkey(ser, keyname, duration):
    pass


def colorkey(ser, keyname, duration):
    if keyname.find('red') > -1:
        press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_A_RED)
        release_media(ser, MEDIAKeyCodes.KEY_MEDIA_A_RED)
    if keyname.find('green') > -1:
        press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_B_GREEN)
        release_media(ser, MEDIAKeyCodes.KEY_MEDIA_B_GREEN)
    if keyname.find('blue') > -1:
        press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_D_BLUE)
        release_media(ser, MEDIAKeyCodes.KEY_MEDIA_D_BLUE)
    if keyname.find('yellow') > -1:
        press_media_key(ser, MEDIAKeyCodes.KEY_MEDIA_C_YELLOW)
        release_media(ser, MEDIAKeyCodes.KEY_MEDIA_C_YELLOW)


def menukey(ser, keyname, duration):
    press_consumer_key(ser, "0 0 0 32")
    # release_all(ser)


def sourcekey(ser, keyname, duration):
    pass


def fastforwardkey(ser, keyname, duration):
    press_consumer_key(ser, "0 0 128 0")
    # release_all(ser)


def rewindkey(ser, keyname, duration):
    press_consumer_key(ser, "0 0 64 0")
    # release_all(ser)


def advancekey(ser, keyname, duration):
    press_consumer_key(ser, "0 2 0 0")
    # release_all(ser)


def replaykey(ser, keyname, duration):
    press_consumer_key(ser, "0 1 0 0")
    # release_all(ser)


def playkey(ser, keyname, duration):
    press_consumer_key(ser, "0 0 32 0")
    # release_all(ser)


btnPageRemoconKey = {
    "pairing": pairing,
    "unpairing": unpairing,
    "num0": _numberkey,
    "num1": _numberkey,
    "num2": _numberkey,
    "num3": _numberkey,
    "num4": _numberkey,
    "num5": _numberkey,
    "num6": _numberkey,
    "num7": _numberkey,
    "num8": _numberkey,
    "num9": _numberkey,
    "sharp": _sharpkey,
    "asterisk": _asterisk,
    "volumeup": _volumeup,
    "volumedown": _volumedown,
    "mute": _mute,
    "volumeup_rc": _volumeup_rc,
    "volumedown_rc": _volumedown_rc,
    "mute_rc": _mute_rc,
    "left": _left,
    "right": _right,
    "up": _up,
    "down": _down,
    "back": _back,
    "home": _home,
    "search": _search,
    "ok": _ok,
    "ok_rc": _ok_rc,
    "assist": _assist,
    "tvpower": powerkey,
    "power": powerkey,
    "settoppower": powerkey,
    "channelup": _channelup,
    "channeldown": _channeldown,
    "channelup_rc": chupkey,
    "channeldown_rc": chdownkey,
    "exit": exitkey,
    "fav": favkey,
    "tvschedule": tvschedulekey,
    "mark": markkey,
    "multiview": multiviewkey,
    "red": colorkey,
    "green": colorkey,
    "yellow": colorkey,
    "blue": colorkey,
    "menu": menukey,
    "source": sourcekey,
    "fastforward": fastforwardkey,
    "rewind": rewindkey,
    "advance": advancekey,
    "replay": replaykey,
    "play": playkey,
    "disconnect": disconnecting,
    "device_status": device_status,
    "device_type": device_type,
    "device_name": device_name
}
