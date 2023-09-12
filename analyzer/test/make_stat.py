import json
import cv2
import time

video_path = '/home/jade-m32-05/projects/prep-exec-analysis/data/workspace/macroblock_sparse.mp4'
output_path = 'test.mp4_stat'

cap = cv2.VideoCapture(video_path)
timestamps = []

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    timestamps.append(time.time())

cap.release()

with open(output_path, 'w') as f:
    json.dump({
        'data': {
            'timestamps': timestamps,
        }
    }, f, indent=4)
