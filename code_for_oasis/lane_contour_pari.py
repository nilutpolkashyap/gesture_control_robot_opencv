# -*- coding: utf-8 -*-
"""
Created on Sat May 22 18:46:12 2021

@author: nkele
"""

import cv2
import numpy as np
import imutils

cap =cv2.VideoCapture("lane_red3.mp4")

cap.set(3,640)
cap.set(4,480)

while(True):
    try:
        
        ret, frame= cap.read()
        
        cv2.imshow("original", frame)
        
        height = frame.shape[1]
        width = frame.shape[0]
        
        
        
        frame = frame[int(width/2) : width, 0: height]
        
        hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_yellow = np.array([0,70,70], np.uint8)
        upper_yellow = np.array([50,255,255], np.uint8)
        
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)  
        
        kernal = np.ones((5,5), "uint8")
        
        mask = cv2.dilate(mask, kernal)
    	#res_yellow = cv2.bitwise_and(frame, frame, mask = mask)
    
        
        cnts= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)
        print(len(cnts))
        
        crd_list = []
        
        for c in cnts:
            area = cv2.contourArea(c)
            if area>1000:
                cv2.drawContours(frame,[c],-1,(0,255,0),3)
                M=cv2.moments(c)
    
                cx= int(M["m10"]/M["m00"])
                cy= int(M["m01"]/M["m00"])
                print("centroid is at: ",cx,cy)
                
                crd_list.append(cx)
    
                cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
    
                #cv2.imshow("frame",frame)
                
        print(crd_list)  
        
        crd_avg = int((crd_list[0] + crd_list[1])/2)
        
        frame_centre = int(height/2)
        
        print(crd_avg)
        print(frame_centre)
        
        frame = cv2.circle(frame, (crd_avg, int(1*(width/4))), 10, (0,0,255), 2)
        frame = cv2.circle(frame, (int(height/2), int(1*(width/4))), 10, (255,0,0), 2)
              
        cv2.imshow("frame",frame)
        
        #print("centroids")
        #print("centroid is at: ",cx,cy)
        
        if (frame_centre - crd_avg) > 5:
            print("DRIVE RIGHT!!")
        elif (crd_avg - frame_centre) > 5:
            print("DRIVE LEFT!!")
        elif (((frame_centre - crd_avg) <= 5) and ((crd_avg - frame_centre) <= 5)):
            print("MOVE ALONG CENTRE!!")
    
        
        if(cv2.waitKey(40) & 0xFF == ord('q')):
            break
        
    except:
        break
        
cap.release()
cv2.destroyAllWindows()