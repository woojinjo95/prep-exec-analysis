import time
import getpass


def get_device_name():
    username = getpass.getuser()
    if '-' in username:
        username = username.replace('-', '_')
    with open('DeviceName.h', 'w') as f:
        f.write(f'#define DEVICE_NAME "BT_{username}"\n')
    f.close()
    time.sleep(1)
    

if __name__ == '__main__':
    get_device_name()