import cv2
import numpy as np
import copy
import math
method = cv2.TM_SQDIFF
bgModel = cv2.createBackgroundSubtractorMOG2()
MPx=0
MPy=0
found=found2=False
posprev=posprev2=None
def calculateDistance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist
def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=-1)
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)[1]
    res = cv2.bitwise_and(thresh, thresh, mask=fgmask)
    return res  
cap = cv2.VideoCapture('sentry3.mkv')
im1=cv2.imread("One.png")
im2=cv2.imread("Two.png")
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1440,810))
while(cap.isOpened()):   
    ret,frame=cap.read()
    if found==False:
        #print("None1")
        result = cv2.matchTemplate(frame,im1, method)
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        MPx,MPy = mnLoc
    if found2==False:
        #print("None2")
        result2 = cv2.matchTemplate(frame,im2, method)
        mn2,_,mnLoc2,_ = cv2.minMaxLoc(result2)
        MPx2,MPy2 = mnLoc2
    image = removeBG(frame)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #res = max(contours, key=cv2.contourArea)
    nearest1 = nearest2 = 1000000000        
    point1=point2=(0,0)
    #contours = sorted(contours,key=cv.contourArea)
    for cnt in contours:
        # If current element is smaller than first then 
        # update both first and second 
        M=cv2.moments(cnt)
        cX=cY=0
        if(M["m00"]!=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        centre=(cX,cY)
        if posprev is not None:
            dist1=calculateDistance(posprev[0],posprev[1],cX,cY)
            if(dist1<nearest1):
                nearest1=dist1
                point1=centre
        if posprev2 is not None:
            dist2=calculateDistance(posprev2[0],posprev2[1],cX,cY)
            if(dist2<nearest2):
                nearest2=dist2
                point2=centre
    cv2.circle(frame, point1, 3, (255,0,0), 10)
    cv2.circle(frame, point2, 3, (0,0,255), 10)
    cv2.putText(frame, 'ONE',point1, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
    cv2.putText(frame, 'TWO',point2, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
    if(point1!=(0,0)):
        posprev=point1             
    if(point2!=(0,0)):
        posprev2=point2
    try:
        if found==False:
            if mn==0.0:        
                cv2.circle(frame, mnLoc, 3, (255,0,0), 10)
                posprev=mnLoc
                found=True
        if found2==False:
            if mn2==0.0:        
                cv2.circle(frame, mnLoc2, 3, (0,0,255), 10)
                posprev2=mnLoc2
                found2=True        
            #cv2.imshow('clip',pic)        
    except:
        continue    
    out.write(frame)    	
    cv2.imshow('bgr',frame)    
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()			
