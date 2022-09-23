from cvzone.HandTrackingModule import HandDetector
from pynput.mouse import Button, Controller
import cv2

mouse = Controller()


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

lastX, lastY = None, None
lastYScroll = None
delayCounter = 0
onPress = False

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    scale_percent = 60  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    img = cv2.resize(img, dim)

    hands, img = detector.findHands(img, flipType=False)

    rightHand = list(filter(lambda val: val["type"] == "Right", hands))
    leftHand = list(filter(lambda val: val["type"] == "Left", hands))

    if len(rightHand) > 0:
        rightHand = rightHand[0]

        thumbFinger = rightHand["lmList"][4]
        indexFinger = rightHand["lmList"][8]

        x, y, _ = indexFinger

        if not lastX or not lastY:
            lastX = x
            lastY = y

        xTotal, yTotal = (x - lastX) * 1.8, (y - lastY) * 1.8
        lastX = x
        lastY = y

        # mouse.position = (
        #     mouse.position[0] + xTotal,
        #     mouse.position[1] + yTotal,
        # )

        mouse.move(xTotal * 1.2, yTotal * 1.2)

        if len(leftHand) > 0:
            leftHandPack = leftHand[0]

            thumbFinger2 = leftHandPack["lmList"][4]
            indexFinger2 = leftHandPack["lmList"][8]
            middleFinger2 = leftHandPack["lmList"][11]

            lengthOne, _ = detector.findDistance(thumbFinger, thumbFinger2)
            lengthTwo, _ = detector.findDistance(thumbFinger, indexFinger2)

            lengthPress, _ = detector.findDistance(thumbFinger2, indexFinger2)

            # print(img)
            # print(length)

            if lengthOne < 10 and delayCounter == 0:
                mouse.click(Button.left, 1)

            elif lengthTwo < 10 and delayCounter == 0:
                mouse.click(Button.left, 2)

            elif lengthPress < 10 and delayCounter == 0:
                mouse.press(Button.left)
                onPress = True

            if lengthPress > 10 and onPress:
                mouse.release(Button.left)
                onPress = False

    else:
        lastX, lastY = None, None

    if len(leftHand) > 0:
        leftHandPack = leftHand[0]

        indexFinger2 = leftHandPack["lmList"][8]
        middleFinger2 = leftHandPack["lmList"][11]

        lengthThree, _ = detector.findDistance(middleFinger2, indexFinger2)

        if lengthThree < 10:
            _, yScroll, _ = middleFinger2

            if not lastYScroll:
                lastYScroll = yScroll

            yScrollMin = yScroll - lastYScroll

            print(yScrollMin)

            if yScrollMin > 10 and delayCounter == 0:
                mouse.scroll(0, -1)

            elif yScrollMin < -10 and delayCounter == 0:
                mouse.scroll(0, 1)

        else:
            yScrollMin = None

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 20:
            delayCounter = 0

    # display
    key = cv2.waitKey(1)
    cv2.imshow("Image", img)
    if key == ord("c"):
        myEquation = ""
