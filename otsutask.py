import cv2

image = cv2.imread('backg.jpg',-1)
cv2.imshow("image", image)
cv2.waitKey(0)
