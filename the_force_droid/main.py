# -*- coding: utf-8 -*-
"""
Created on Sun May 23 21:51:05 2021

@author: nkele
"""

import numpy as np
import cv2

webcam = cv2.VideoCapture(0)


while(1):
	
	_, imageFrame = webcam.read()
    
	width = int(imageFrame.shape[1] * 0.25)
	height = int(imageFrame.shape[0] * 0.25)

	cv2.resize(imageFrame, (width, height), interpolation =cv2.INTER_AREA)
    
	imageFrame = cv2.flip(imageFrame, flipCode=-1)

	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

# 	red_lower = np.array([136, 87, 111], np.uint8)
# 	red_upper = np.array([180, 255, 255], np.uint8)
# 	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

# 	green_lower = np.array([25, 52, 72], np.uint8)
# 	green_upper = np.array([102, 255, 255], np.uint8)
# 	green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    
# 	green_lower = np.array([40,100,100], np.uint8)
# 	green_upper = np.array([60,255,255], np.uint8)
# 	green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)    

	blue_lower = np.array([80, 80, 2], np.uint8)
	blue_upper = np.array([100, 255, 255], np.uint8)
	blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
	
	kernal = np.ones((5, 5), "uint8")
	
	# For red color
 	# red_mask = cv2.dilate(red_mask, kernal)
 	# res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
 	
 	# # For green color
 	# green_mask = cv2.dilate(green_mask, kernal)
 	# res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)
	
	# For blue color
	blue_mask = cv2.dilate(blue_mask, kernal)
	res_blue = cv2.bitwise_and(imageFrame, imageFrame,
							mask = blue_mask)

# 	# Creating contour to track red color
# 	contours, hierarchy = cv2.findContours(red_mask,
# 										cv2.RETR_TREE,
# 										cv2.CHAIN_APPROX_SIMPLE)
# 	
# 	for pic, contour in enumerate(contours):
# 		area = cv2.contourArea(contour)
# 		if(area > 300):
# 			x, y, w, h = cv2.boundingRect(contour)
# 			imageFrame = cv2.rectangle(imageFrame, (x, y),
# 									(x + w, y + h),
# 									(0, 0, 255), 2)
# 			
# 			cv2.putText(imageFrame, "Red Colour", (x, y),
# 						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
# 						(0, 0, 255))	

# 	# Creating contour to track green color
# 	contours, hierarchy = cv2.findContours(green_mask,
# 										cv2.RETR_TREE,
# 										cv2.CHAIN_APPROX_SIMPLE)
# 	
# 	for pic, contour in enumerate(contours):
# 		area = cv2.contourArea(contour)
# 		if(area > 300):
# 			x, y, w, h = cv2.boundingRect(contour)
# 			imageFrame = cv2.rectangle(imageFrame, (x, y),
# 									(x + w, y + h),
# 									(0, 255, 0), 2)
# 			
# 			cv2.putText(imageFrame, "Green Colour", (x, y),
# 						cv2.FONT_HERSHEY_SIMPLEX,
# 						1.0, (0, 255, 0))

	# Creating contour to track blue color
	contours, hierarchy = cv2.findContours(blue_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 100):
			#print(len(contour))
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(255, 0, 0), 2)
			
			cv2.putText(imageFrame, "Blue Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (255, 0, 0))
			

            
	# Program Termination
	cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		#cap.release()
		#cv2.destroyAllWindows()
		break
webcam.release()

cv2.destroyAllWindows()
