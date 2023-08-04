class Command:
    status_set = '01'
    repeat = '02'
    transmit = '03'

class Status:
    ready = '01'
    network = '02'
    start = '03'
    finish = '04'
    findme = '05'
    found = '06'
    poweroff = '07'
    status_list = ['ready', 'network', 'start', 'finish', 'findme', 'found', 'poweroff']

class Thermistor:
    nomal = '00'
    error = '01'

class IrBtRcvSet:
    ir_on = '01'
    bt_on = '10'
    ir_bt_on = '11'
    ir_bt_off = '00'

class HpdSet:
    on = '01'
    off = '00'

class LanSet:
    on = '01'
    off = '00'

class VacSet:
    on = '01'
    off = '00'

class NwsbcpwrSet:
    on = '01'
    off = '00'

class StartEnd:
    start = 'aa'
    end = 'ee'
    
class CounterSet:
    start = '01'
    stop = '02'
    reset = '03'
    request = '00'

class IrFrame:
    start = 'aa15010000000000ee'
    end = 'aa15020000000000ee'
