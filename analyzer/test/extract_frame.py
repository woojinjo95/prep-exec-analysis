import cv2
import os

image_dir = './images'
os.makedirs(image_dir, exist_ok=True)

video_path = '/home/jade-m32-05/projects/prep-exec-analysis/data/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-22T172921F075886+0900_1800.mp4'
cap = cv2.VideoCapture(video_path)
index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imwrite(f'{image_dir}/frame_{index}.jpg', frame)
    index += 1
cap.release()
