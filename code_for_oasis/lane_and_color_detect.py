
import cv2
import numpy as np
import imutils



red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8) 

green_lower = np.array([35,100,100], np.uint8)
green_upper = np.array([70,255,255], np.uint8)  

blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)

lower_yellow = np.array([0,70,70], np.uint8)
upper_yellow = np.array([50,255,255], np.uint8)


cap =cv2.VideoCapture("lane.mp4")

cap.set(3,640)
cap.set(4,480)

while(True):
    ret, frame= cap.read()
    
    cv2.imshow("original", frame)
    
    height = frame.shape[1]
    width = frame.shape[0]
    
    
    
    crp_frame = frame[int(width/2) : width, 0: height]
    
    hsv= cv2.cvtColor(crp_frame, cv2.COLOR_BGR2HSV)
    
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(frame, imageFrame,mask = red_mask)
    
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(frame, imageFrame,mask = green_mask)
	
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(frame, imageFrame,mask = blue_mask)
    
    
	contours, hierarchy = cv2.findContours(red_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			frame = cv2.rectangle(frame, (x, y),
									(x + w, y + h),
									(0, 0, 255), 2)
			
			cv2.putText(frame, "Red Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 0, 255))
            
	contours, hierarchy = cv2.findContours(green_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			frame = cv2.rectangle(frame, (x, y),
									(x + w, y + h),
									(0, 255, 0), 2)
			
			cv2.putText(frame, "Green Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (0, 255, 0))
            
	contours, hierarchy = cv2.findContours(blue_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			frame = cv2.rectangle(frame, (x, y),
									(x + w, y + h),
									(255, 0, 0), 2)
			
			cv2.putText(frame, "Blue Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (255, 0, 0))
            
    
    
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
            cv2.drawContours(crp_frame,[c],-1,(0,255,0),3)
            M=cv2.moments(c)

            cx= int(M["m10"]/M["m00"])
            cy= int(M["m01"]/M["m00"])
            print("centroid is at: ",cx,cy)
            
            crd_list.append(cx)

            cv2.circle(crp_frame,(cx,cy),7,(255,255,255),-1)

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
        
cap.release()
cv2.destroyAllWindows()