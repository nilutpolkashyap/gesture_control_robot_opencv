# -*- coding: utf-8 -*-
"""
Created on Tue May 25 02:30:02 2021

@author: nkele
"""

import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture("vid1.mp4")

# url = 'http://192.168.43.108:8080/video'
# cap = cv2.VideoCapture(url)

while True:
    try:
        ret, frame = cap.read()
        
        cv2.imshow("original", frame)
        # print("frame",frame)
            
        height = frame.shape[1]
        width = frame.shape[0]
            
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
        blue_lower = np.array([80, 80, 2], np.uint8)
        blue_upper = np.array([100, 255, 255], np.uint8)
        mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
        kernal = np.ones((5,5), "uint8")
            
        mask = cv2.dilate(mask, kernal)
            
        cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
            
        # print(len(cnts))
            
        crdx_list = []
        crdy_list = []
            
        for c in cnts:
            area = cv2.contourArea(c)
                
            if area > 1000:
                cv2.drawContours(frame, [c],-1, (0,255,0),3)
                M = cv2.moments(c)
                    
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                    
                crdx_list.append(cx)
                crdy_list.append(cy)
                    
                cv2.circle(frame, (cx,cy), 7, (255,255,255), -1)
                
        print("cx = ", crdx_list, " cy = ", crdy_list)   
        
        midx = height/2
        midy = width/2
        
        print("midx = ", midx, " midy = ", midy)
        
                    
        cv2.imshow("frame", frame)
            
        if(cv2.waitKey(40) & 0xFF == ord('q')):
            break
                
    except:
        break
    
cap.release()
cv2.destroyAllWindows()
            
            
        
        

































    
