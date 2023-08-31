import logging
import os

colors = {
    'BRIGHT_MAGENTA': '\033[95m',
    'BRIGHT_CYAN': '\033[96m',
    'BRIGHT_GREEN': '\033[92m',
    'BRIGHT_BLUE': '\033[94m',
    'BRIGHT_YELLOW': '\033[93m',
    # 'BRIGHT_RED': '\033[91m',
    # 'BRIGHT_BLACK': '\033[90m',
    # 'BRIGHT_WHITE': '\033[97m',
    'BRIGHT_END': '\033[0m',
}


color_idx = 0
default_color = colors['BRIGHT_END']
colors = list(colors.values())
log_dir = os.path.join('logs')


def simple_logger(name='main'):
    global color_idx
    try:
        color = colors[color_idx]
        color_idx = (color_idx + 1) % len(colors)
    except IndexError:
        logger.error('color exhausted')
        color = ''  # no color

    logger = logging.getLogger(name)
    log_format = f"{color}{name:<8} | [%(asctime)s] %(message)s {default_color}"
    formatter = logging.Formatter(log_format)

    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)

    os.makedirs(log_dir, exist_ok=True)
    filehandler = logging.FileHandler(filename=os.path.join(log_dir, f'{name}.log'), encoding='utf-8-sig')
    filehandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(streamhandler)
    logger.addHandler(filehandler)
    return logger
