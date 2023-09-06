import cv2
from scripts.control.image import get_snapshot


image = get_snapshot()
cv2.imwrite('/app/workspace/snapshot.jpg', image)

