import cv2

image_path = './frame_cold.jpg'
image = cv2.imread(image_path)

# draw roi
roi = (840, 750, 250, 80)
cv2.rectangle(image, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)
cv2.imwrite('./frame_roi.png', image)
