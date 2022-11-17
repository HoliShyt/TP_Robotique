
import cv2

capt = cv2.VideoCapture(0)

#tracker = cv2.legacy.TrackerMOSSE_create() #Plus rapide mais moins précis
tracker = cv2.legacy.TrackerCSRT_create() #plus précis mais plus lent
success, img = capt.read()
bbox=cv2.selectROI("Tracking", img,False)
tracker.init(img,bbox)


def drawBox(img,bbox):
    x,y,w,h=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img, "Tracking", (75, 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

while True:
    timer=cv2.getTickCount()
    success, img = capt.read()
    #flipImg=cv2.flip(img,1) #On retourne l'image
    succes,bbox=tracker.update(img)
    if succes:
        drawBox(img,bbox)
    else:
        cv2.putText(img, "Tracking" , (75, 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)


    #fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    #cv2.putText(flipImg, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('\x1b'):
        break

