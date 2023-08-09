def is_running_in_docker():
    return True
    try:
        with open('/proc/1/cgroup', 'rt') as f:
            return 'docker' in f.read()
    except FileNotFoundError:
        return False


def convert_if_docker_localhost(url: str) -> str:
    if url in ('localhost', '127.0.0.1') and is_running_in_docker():
        url = 'host.docker.internal'
    return url
