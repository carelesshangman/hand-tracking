import cv2
import cvzone.HandTrackingModule

cap = cv2.VideoCapture(0)
detector = cvzone.HandTrackingModule.HandDetector(maxHands=2, detectionCon=0.8)
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    # Hand - dict (-lmList - bbox - center - type)

    if hands:
        # hand 1
        hand1 = hands[0]
        # 21 tock na roki
        lmList1 = hand1["lmList"]
        # bound box x,y,w,h
        bbox1 = hand1["bbox"]
        # sredina
        centerpoint1 = hand1["center"]
        # leva al desna
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)

        if fingers1[1] == 1:
            lastX = lmList1[8][0]

    cv2.imshow("Image", img)
    cv2.waitKey(1)