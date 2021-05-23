
import cv2
import numpy as np

webcam = cv2.VideoCapture("lane.mp4")


while(True):
	ret, imageFrame = webcam.read()
    
	height = imageFrame.shape[1]
	width = imageFrame.shape[0]
    
# 	height = int(height/2)
# 	width = int(width/2)
    
	#print(height)
	#print(width)
    
	upp_width = int(1*(width/3))
	low_width = int(2*(width/3))
    
	imageFrame = imageFrame[upp_width : low_width, 0: height]

	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

	yellow_lower = np.array([0,100,100], np.uint8)
	yellow_upper = np.array([50,255,255], np.uint8)
	yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)  

	kernal = np.ones((5,5), "uint8")

	yellow_mask = cv2.dilate(yellow_mask, kernal)
	res_yellow = cv2.bitwise_and(imageFrame, imageFrame, mask = yellow_mask)

	contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#print(len(contours))
	#print(contours.shape)

	new_contours = []
# 	cl_contours = []

# 	for i in range(len(contours)):
#   		#print(contours[i].shape)
# 		if contours[i].shape[0] > 10:
# 			cl_contours.append(contours[i])

	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		#print(area)
		if(area > 1000):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x,y), (x+w,y+h),(0,0,255),2)
			imageFrame = cv2.circle(imageFrame, (int(x+w//2),int(y+h//2)), 10, (255,0,0), 2)
			imageFrame = cv2.circle(imageFrame, (int(height/2),int(upp_width/2)), 10, (255,255,0), 2)
			new_contours.append(contour)
			print("contour")
# 			print(new_contour)
			#print(contour.mean())
			imageFrame = cv2.circle(imageFrame, (int(contour.mean()),int(upp_width/2)), 10, (255,0,255), 2)

	cv2.putText(imageFrame, "Yellow Colour", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))


	cv2.imshow("Multiple color detection in real time", imageFrame)

	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

webcam.release()

cv2.destroyAllWindows()


# for i in range(len(contour)):
#     print(contour[i][0])