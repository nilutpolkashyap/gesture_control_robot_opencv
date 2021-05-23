# -*- coding: utf-8 -*-
"""
Created on Sat May 22 12:04:55 2021

@author: nkele
"""

import cv2
import numpy as np


# def average_slope_intercept(frame, intercept):
#     lane_lines = []
#     avg_height, avg_width, _ = frame.shape
#     left_fit = []
#     right_fit = []
    
#     boundary = 1/3
#     left_region_boundary = width * (1-boundary)
#     right_region_boundary = width * boundary
    
#     for line_segment in line_segments:
#         for x1, y1, x2, y2 in line_segment:
#             if x1 == x2:
#                 print("skipping vertical line segment")
#                 continue
#             fit = np.polyfit((x1,x2),(y1, y2),1)
#             slope = fit[1]
            
#             if slope < 0:
#                 if x1 < left_region_boundary and x2 < left_region_boundary:
#                     left_fit.append((slope, intercept))
#             else:
#                 if x1 > right_region_boundary and x2 > right_region_boundary:
#                     right_fit.append((slope, intercept))
                    
#     left_fit_avergae = np.average(left_fit, axis = 0)
#     if len(left_fit)
    

webcam  = cv2.VideoCapture("lane.mp4")

while(True):
    ret, imageFrame = webcam.read()
    
    height = imageFrame.shape[0]
    width = imageFrame.shape[1]
    
    upper_width = int(3*(width/5))
    lower_width = int(5*(width/5))
    
    #imageFrame = imageFrame[upper_width: lower_width, 0: height]
    
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    
    yellow_lower = np.array([0,60,60], np.uint8)
    yellow_upper = np.array([55,255,255], np.uint8)
    
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    
    kernal = np.ones((5,5), "uint8")
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    
    edges = cv2.Canny(yellow_mask, 200, 400)
    
    edge_height, edge_width = edges.shape
    
    mask = np.zeros_like(edges)
    
    polygon = np.array([[(0, height * 1 / 2),(width, height * 1 / 2),(width, height),(0, height),]], np.int32)
    
    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(yellow_mask, mask)
    
    # rho =1
    # angle = np.pi / 180
    # min_threshold = 10
    # line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]), minLineLength=8, maxLineGap=4)
    
    
    ret, thresh = cv2.threshold(cropped_edges, 150, 255, cv2.THRESH_BINARY)
    
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    
    image_copy = imageFrame.copy()
    
    print(len(contours))
    
    cv2.drawContours(imageFrame, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1000):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x,y), (x+w,y+h),(0,0,255),2)
    
    
    cv2.imshow("original",imageFrame)
    cv2.imshow("output",thresh)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    
webcam.release()

cv2.destroyAllWindows()
    
    
    