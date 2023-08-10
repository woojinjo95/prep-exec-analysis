import re
from log_stream import split_log_stream, convert_timestamp


def parse_tag_dumpsys_meminfo_timestamp(chunk):
    dumpsys_meminfo_timestamp_pattern = re.compile(r"^.?Timestamp : (?P<time>.*)$")
    mat = dumpsys_meminfo_timestamp_pattern.match(chunk[0])
    res = {"raw": chunk[:]}
    res["log_type"] = "dumpsys_meminfo"
    res["log_tag"] = "dumpsys_meminfo_timestamp"
    if mat:
        res.update(mat.groupdict())
    return res


split_patterns = {
    'timestamp': re.compile(r'^Timestamp :*'),
    'detail': re.compile(r"^Applications Memory Usage*"),
    'summary': re.compile(r'^Total RAM:*'),
}


def get_section(line, current_section):
    if re.match(r'^Total PSS by process:*', line) is not None:
        current_section = 'pss_by_process'
    elif re.match(r'^Total PSS by OOM adjustment:*', line) is not None:
        current_section = 'pss_by_oom_adj'
    elif re.match(r'^Total PSS by category:*', line) is not None:
        current_section = 'pss_by_category'
    return current_section


def get_adj(line, adj_info):
    match = re.match(r'\s*(?P<adj_pss>[0-9\,\-]+)\s?(K|kB)\s?\:\s?(?P<adj>.*)', line)
    if match is not None:
        adj_info = match.groupdict()
    return adj_info


def initialize_detail_result():
    return {'section': None,
            'adj': None,
            'adj_pss': None,
            'category': None,
            'process': None,
            'pid': None,
            'pss': None}


def initialize_adj():
    return {'adj': None, 'adj_pss': None}


def parse_detail(chunk):
    section = None
    adj_info = initialize_adj()
    for line in chunk:
        detail_result = initialize_detail_result()
        section = get_section(line, section)
        detail_result.update({'section': section})

        match = re.match(r'\s*(?P<pss>[0-9\,\-]+)\s?(K|kB)\s?\:\s?(?P<process>.+)\s\(\s?pid\s(?P<pid>\d+)', line)
        if match is None:
            if section == 'pss_by_oom_adj':
                adj_info = get_adj(line, adj_info)
            else:
                adj_info = initialize_adj()
            if section == 'pss_by_category':
                match = re.match(r'\s*(?P<pss>[0-9\,\-]+)\s?(K|kB)\s?\:\s?(?P<category>.*)', line)
                if match is not None:
                    detail_result.update(match.groupdict())
                    yield detail_result
        else:
            detail_result.update(adj_info)
            detail_result.update(match.groupdict())
            yield detail_result


def parse_summary(chunk):
    summary_result = {'Total_RAM': None, 'Free_RAM': None, 'Used_RAM': None, 'Lost_RAM': None}
    for line in chunk:
        # summary_result check
        summary_match = None
        if 'Total RAM:' in line:
            summary_match = re.match(r'\s*Total RAM:\s*(?P<Total_RAM>[0-9\,\-]+)', line)
        elif 'Free RAM:' in line:
            summary_match = re.match(r'\s*Free RAM:\s*(?P<Free_RAM>[0-9\,\-]+)', line)
        elif 'Used RAM:' in line:
            summary_match = re.match(r'\s*Used RAM:\s*(?P<Used_RAM>[0-9\,\-]+)', line)
        elif 'Lost RAM:' in line:
            summary_match = re.match(r'\s*Lost RAM:\s*(?P<Lost_RAM>[0-9\,\-]+)', line)
        if summary_match is not None:
            summary_result.update(summary_match.groupdict())
    if any(k is None for k in summary_result.values()):
        summary_result = {}
    return summary_result


def parse_dumpsys_meminfo(dumpsys_meminfo_log_file):
    current_time_stamp = None
    for k, chunk in split_log_stream(dumpsys_meminfo_log_file, split_patterns):
        if k == 'timestamp':
            r = parse_tag_dumpsys_meminfo_timestamp(chunk)
            if 'time' in r:
                current_time_stamp = convert_timestamp(r['time'])
        elif k == 'summary':
            header_info = parse_summary(chunk)
            if header_info and current_time_stamp:
                yield 'summary', (current_time_stamp, header_info)
        elif k == 'detail':
            if current_time_stamp:
                for detail in parse_detail(chunk):
                    yield 'detail', (current_time_stamp, detail)
        else:
            pass


def process_dumpsys_meminfo(dumpsys_meminfo_log_file):
    summary_list = []
    detail_list = []
    for k, (time_stamp, item) in parse_dumpsys_meminfo(dumpsys_meminfo_log_file):
        if k == 'summary':
            summary_list.append({'timestamp': time_stamp, **item})
        elif k == 'detail':
            detail_list.append({'timestamp': time_stamp, **item})
    return summary_list, detail_list
