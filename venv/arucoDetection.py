import numpy as np
import time
import cv2

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


def aruco_display(corners, ids, rejected, image):
    if len(corners) > 0:

        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
            #cv2.line(image, topLeft,bottomRight,(0,0,255),2)
            #cv2.line(image, bottomLeft,topRight,(0,0,255),2)

            #====== calcul du centre de gravité du QRCode ======
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1) #Centre de G

            cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
            print("[Inference] ArUco marker ID: {}".format(markerID))

    return image


aruco_type = "DICT_4X4_100"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

cap = cv2.VideoCapture(1)  #camera 0

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():

    ret, img = cap.read()
    h, w, _ = img.shape
    width = 1000
    height = int(width * (h / w))

#On définit les IDs des markers sur le plateau
    marker_topLeft=1
    marker_topRight=2
    marker_bottomLeft=3
    marker_bottomRight=4

# On définit les dimensions du plateau
    distance_topLeft_topRight=3000 #en mm
    distance_bottomLeft_bottomRight=3000 #en mm
    distance_topLeft_bottomLeft=2000 #en mm
    distance_topRight_bottomRight=20000 #en mm

#Position des markers

    pos_marker_topLeft= (0,0)
    pos_marker_topRight = (0, 3000)
    pos_marker_bottomLeft = (2000, 0)
    pos_marker_bottomRight = (2000, 3000)


    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    corners, ids, rejected = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

    detected_markers = aruco_display(corners, ids, rejected, img)

    cv2.imshow("Image", detected_markers)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("\x1b"):
        break

cv2.destroyAllWindows()
cap.release()