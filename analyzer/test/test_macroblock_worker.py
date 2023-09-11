from scripts.analysis.macroblock.detector import MacroblockDetector
import cv2
import time

detector = MacroblockDetector()

# video_path = '/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T172921F075886+0900_1800.mp4'
video_path = '/app/workspace/macroblock_sparse.mp4'
cap = cv2.VideoCapture(video_path)

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()
    frame = cv2.resize(frame, (960, 540))
    result = detector.update(frame)
    delay = time.time() - start_time

    print(f'{index}: {result}, delay: {delay}')
    index += 1
