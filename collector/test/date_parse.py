import re
from datetime import datetime

def extract_timestamp(line):
    pattern1 = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})'  # matches "[ 07-24 04:35:29.422"
    pattern2 = r'Timestamp\s:\s(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6})'  # matches "Timestamp : 2023-07-11 18:28:41.105968"

    match1 = re.search(pattern1, line)
    match2 = re.search(pattern2, line)

    if match1:
        # Format for pattern1 is "MM-DD HH:MM:SS.sss", so we assume current year
        return datetime.strptime(f"{datetime.now().year}-{match1.group(1)}", "%Y-%m-%d %H:%M:%S.%f")
    elif match2:
        # Format for pattern2 is "YYYY-MM-DD HH:MM:SS.ssssss"
        return datetime.strptime(match2.group(1), "%Y-%m-%d %H:%M:%S.%f")

lines = [
    "[ 07-24 04:35:29.422  5372:32214 I/chatty   ]",
    "Timestamp : 2023-07-11 18:28:41.105968",
    "07-26 17:48:37.657"
]

for line in lines:
    t = extract_timestamp(line)
    print(t, type(t))
