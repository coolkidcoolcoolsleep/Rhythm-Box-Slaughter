import cv2


img = cv2.imread('blue_ball/blue_ball-001.jpeg')
height, width, channels = img.shape

if img is None:
    print('이미지 불러오기 실패')
    exit()

cv2.namedWindow('Rhythm Box Slaughter')
cv2.imshow('Rhythm Box Slaughter', img)

cv2.waitKey()
cv2.destroyAllWindows()

