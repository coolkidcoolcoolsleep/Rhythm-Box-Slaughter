import cv2
import numpy as np


# Camera
cap_cam = cv2.VideoCapture(0)
if not cap_cam.isOpened():
    print('Cannot open camera')
    exit()
ret, frame_cam = cap_cam.read()
if not ret:
    print('Cannot open camera stream')
    cap_cam.release()
    exit()

# Image
img = cv2.imread('circular-sunglasses.png')
img = cv2.resize(img, dsize=(266, 126))

height = 126
width = 266

while True:
    ret, frame_cam = cap_cam.read()
    if not ret:
        print('Cannot receive frame from camera')
        break
    frame_cam = cv2.resize(frame_cam, (width, height), interpolation = cv2.INTER_AREA)

    # Blend the two images and show the result
    tr = 0.3    # transparency between 0-1, show camera if 0
    frame = ((1-tr) * frame_cam.astype(np.float) + tr * img.astype(np.float)).astype(np.uint8)
    cv2.imshow('Transparent result', frame)
    if cv2.waitKey(1) == 27:    # press ESC to quit
        break

cap_cam.release()
cv2.destroyAllWindows()
