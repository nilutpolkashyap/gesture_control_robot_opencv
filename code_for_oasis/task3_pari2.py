import cv2
import numpy as np
import imutils

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from pprint import pprint

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time
import imutils

#Stop_Color 

SERVICE_ACCOUNT_FILE='ieee-project-314311-ef43f3c722d0.json'

SCOPES=['https://www.googleapis.com/auth/spreadsheets']

creds= None
creds= service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID='1SKYEpBvyTHFHN1gkgFnJHA5r-KK72Gj_nmS6Z5BBwMU'
service = build('sheets','v4',credentials=creds)

sheet=service.spreadsheets()

result=sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='sheet1!A1:B2').execute()

values=result.get('values',[])

stop_color=values[0][0]

#stop_color = "Red"

print("STOP COLOR FROM SHEET : ", stop_color)

if(stop_color=="Red"):
    stop_val=1
elif(stop_color=="Blue"):
    stop_val=2
elif(stop_color=="Green"):
    stop_val=3
else:
    stop_val=1
    print("Invalid Stop Color")
    
    
    
    
    
    
cap1 = cv2.VideoCapture("qr_code3.mp4")
cap1.set(3, 640)
cap1.set(4, 480)

val = False

while(True):
    ret, img = cap1.read()
#     img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img= cv2.flip(img, 1)
    for qr_msg in pyzbar.decode(img):
        my_msg = qr_msg.data.decode("utf-8")
        if my_msg == "start robot":
            val = True
            print("Message : ", my_msg)
            break
        
        pts = np.array([qr_msg.polygon], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img, [pts], True, (255,255,0),5)
        #print(my_msg)
        
    if val == True:
        time.sleep(0.5)
        break
             
    cv2.imshow('result', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cv2.destroyAllWindows()
cap1.release()
print("QR Code detected!!!")
    
    
    


print("\nRobot starting in 5 seconds!!!")
time.sleep(2)


# cap =cv2.VideoCapture("Track-vid.mp4")
cap =cv2.VideoCapture("lane_red.mp4")

cap.set(3,640)
cap.set(4,480)

while(True):
    try: 
        ret, frame= cap.read()
        
        cv2.imshow("original", frame)
        
        height = frame.shape[1]
        width = frame.shape[0]
        
        counter=0
        
        frame = frame[int(width/2) : width, 0: height]
        
        hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_yellow = np.array([0,70,70], np.uint8)
        upper_yellow = np.array([50,255,255], np.uint8)
        
        
        
        #RGB
        lower_red= np.array([0,50,120], np.uint8)
        upper_red= np.array([10,255,255], np.uint8)
        
        lower_green= np.array([40,70,80], np.uint8)
        upper_green= np.array([70,255,255], np.uint8)
        
        lower_blue= np.array([90,60,0], np.uint8)
        upper_blue= np.array([121,255,255], np.uint8)
        
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_green, upper_green)
        mask3 = cv2.inRange(hsv, lower_blue, upper_blue)
        
                            
        
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)  
        
        kernal = np.ones((5,5), "uint8")
        
        mask = cv2.dilate(mask, kernal)
        #res_yellow = cv2.bitwise_and(frame, frame, mask = mask)
    
        
        cnts= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)
        
#         print(len(cnts))
        
        crd_list = []
        
        if(stop_val==1):
            conts= cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            conts=imutils.grab_contours(conts)
        elif(stop_val==2):
            conts= cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            conts=imutils.grab_contours(conts)
        elif(stop_val==3):
            conts= cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            conts=imutils.grab_contours(conts)
        else:
            print("No valid stop color defined!!!")
            break
            
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
        
        for i in conts:
            area1= cv2.contourArea(i)
            if area>10000:
                cv2.drawContours(frame,[i],-1,(0,255,0),3)
                M = cv2.moments(i)
                ix= int(M["m10"]/M["m00"])
                iy= int(M["m01"]/M["m00"])
                cv2.circle(frame,(ix,iy),7,(255,255,255),-1)
                counter=counter+1
            else:
                pass
        
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
        
        if(counter>1):
            break
        
        
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