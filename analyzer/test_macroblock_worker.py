from scripts.analysis.macroblock.worker import Worker
import cv2

worker = Worker()

video_path = '/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T172921F075886+0900_1800.mp4'
cap = cv2.VideoCapture(video_path)

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    result = worker.process_image(frame)
    print(f'{index}: {result}')
    index += 1
