# -*- coding: utf-8 -*-
"""
Created on Fri May 21 01:04:49 2021

@author: nkele
"""

import cv2
import numpy as np

img = cv2.imread('lane2.jpeg')

ORANGE_MIN = np.array([10, 50, 50],np.uint8)
ORANGE_MAX = np.array([25, 255, 255],np.uint8)

hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
#cv2.imwrite('output2.jpg', frame_threshed)


cv2.imshow("output", frame_threshed)

cv2.waitKey(0)
cv2.destroyAllWindows()

