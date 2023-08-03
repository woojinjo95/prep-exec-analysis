import logging
from .ir_constant import Command, Status, Thermistor, IrBtRcvSet, HpdSet, LanSet, VacSet, NwsbcpwrSet, CounterSet

logger = logging.getLogger('serial')


def set_packet(command=Command.status_set, status: str = None, thermistor=Thermistor.nomal, reserved: str = '00',
               irbtrcv: str = None, hpd=HpdSet.on, lan=LanSet.on, vac=VacSet.on, nwsbcpwr=NwsbcpwrSet.on) -> str:
    value = change_value(status, irbtrcv, hpd, lan, vac)
    state = value.get('state')
    irbtrcv = value.get('irbtrcv')
    hpd = value.get('hpd')
    lan = value.get('lan')
    vac = value.get('vac')
    setting_packet = f'{command}0{state}{thermistor}{reserved}{irbtrcv}{hpd}{lan}{vac}{nwsbcpwr}'
    return setting_packet


def trans_start(command: str = Command.transmit, reserved: str = '00', irformat: str = '03', length: str = None):
    code = f'{command}{reserved*3}{length}{reserved}{irformat}{reserved*2}'
    return code


def trans_data(command: str = Command.transmit, value: str = None, reserved: str = '00', irformat: str = '03',
               index_1: str = '00', index_2: str = '00'):
    code = f'{command}{value}{reserved}{irformat}{index_1}{index_2}'
    return code


def trans_end(command: str = Command.transmit, reserved: str = '00', irformat: str = '03', padding: str = "ff"):
    code = f'{command}{reserved*5}{irformat}{padding*2}'
    return code


def repeat_ir(command: str = Command.repeat, reserved: str = '00', irformat: str = '03', repeat_num: int = 0):
    code = f'{command}{reserved*5}{irformat}{reserved}{get_hex(repeat_num)}'
    return code


def led_state(command: str = Command.status_set, setting: int = 0, reserved: str = '00', irformat: str = '03'):
    code = f'{command}0{setting}{reserved*4}{irformat}{reserved*2}'
    return code


def counter_set(command: str = '06', control: str = None, reserved: str = '00'):
    control.lower()
    if control == 'start':
        control_set = CounterSet.start
    elif control == 'stop':
        control_set = CounterSet.stop
    elif control == 'reset':
        control_set = CounterSet.reset
    else:
        control_set = CounterSet.request
    code = f'{command}{control_set}{reserved*7}'
    return code


def get_hex(dec: int) -> str:
    if dec > 0xff:
        logger.warning('decimal is bigger than 255. set value to 255.')
        dec = 255

    if dec < 0x10:
        return '0' + hex(dec)[2:]
    else:
        return hex(dec)[2:]


def change_value(status: str, irbtrcv: str, hpd: str, lan: str, vac: str):
    if status in Status.status_list:
        state = Status.status_list.index(status) + 1

    # [ 'iron' | 'bton' | irbton' | 'irbtoff' ]
    if irbtrcv == 'iron':
        irbtrcv = IrBtRcvSet.ir_on
    elif irbtrcv == 'bton':
        irbtrcv = IrBtRcvSet.bt_on
    elif irbtrcv == 'irbton':
        irbtrcv = IrBtRcvSet.ir_bt_on
    else:
        irbtrcv = IrBtRcvSet.ir_bt_off

    hpd = HpdSet.off if hpd == 'off' else HpdSet.on
    lan = LanSet.off if lan == 'off' else LanSet.on
    vac = VacSet.off if vac == 'off' else VacSet.on

    result = {'state': state, 'irbtrcv': irbtrcv, 'hpd': hpd, 'lan': lan, 'vac': vac}
    return result
