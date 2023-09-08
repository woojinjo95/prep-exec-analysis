from scripts.analysis.macroblock.worker import Worker
import cv2

worker = Worker()

video_path = '/app/data/videos/2020-11-11_16-00-00.mp4'
cap = cv2.VideoCapture(video_path)

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    result = worker.process_image(frame)
    print(f'{index}: {result}')
    index += 1
