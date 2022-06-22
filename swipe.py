import cv2
import cvzone.HandTrackingModule
import mysql.connector

cap = cv2.VideoCapture(0)
detector = cvzone.HandTrackingModule.HandDetector(maxHands=2, detectionCon=0.8)

canSwipe = 1
saveX = 0

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="py"
)

mycursor = db.cursor()

class treshhold():
    def getTreshhold(self):
        threshholdMax = self + (self * 0.1)
        threshholdMin = self - (self * 0.1)
        th = [int(threshholdMin), int(threshholdMax)]
        return th

    def modifyTreshhold(self):
        print("wip")

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
        if fingers1[1] == 1 & canSwipe == 1:
            saveX = lmList1[8][0]
            canSwipe = 0
            print("swipe initiated")
        if fingers1:
            if canSwipe == 0:
                compareX = lmList1[8][0]
                value = treshhold.getTreshhold(saveX)
                if compareX < value[0]:
                    print("right")
                    mycursor.execute("update swipe set swipeWhere=0")
                    db.commit()
                elif compareX > value[1]:
                    print("left")
                    mycursor.execute("update swipe set swipeWhere=2")
                    db.commit()
                else:
                    print("inside idle treshhold")
                    mycursor.execute("update swipe set swipeWhere=1")
                    db.commit()
                if (fingers1[0]==0 & fingers1[1]==0 & fingers1[2]==0 & fingers1[3]==0 & fingers1[4]==0):
                    print("pressed")
                    mycursor.execute("update press set isPressed=1")
                    db.commit()
                else:
                    mycursor.execute("update press set isPressed=0")
                    db.commit()
                #if (fingers1[0]==0 & fingers1[1]==0 & fingers1[2]==1 & fingers1[3]==0 & fingers1[4]==0):
                    #print("fuck you too")
    else:
        canSwipe = 1
        saveX = 0
        print("swipe off")
        mycursor.execute("update swipe set swipeWhere=3")
        db.commit()
        mycursor.execute("update press set isPressed=0")
        db.commit()
    mycursor.execute("select * from swipe")
    for x in mycursor:
        print(x[0])
    cv2.imshow("Image", img)
    cv2.waitKey(1)