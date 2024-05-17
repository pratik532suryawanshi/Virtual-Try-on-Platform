# Virtual-Try-on-Platform
A virtual try-on platform uses computer vision to allow users to see how clothing, accessories, or makeup will look on them in real-time. By analyzing images or videos, it overlays virtual items onto the user's body or face, enhancing the shopping experience by providing a realistic preview.

A virtual try-on platform is an advanced application that allows users to visualize how clothing or accessories would look on them without physically trying them on. This technology leverages computer vision, augmented reality (AR), and machine learning to create a realistic experience for users. Here's a detailed explanation of how such a platform typically works and the role of the code provided in creating a basic version of a virtual try-on system.

Key Components of a Virtual Try-On Platform

Input Acquisition:

Camera Feed: Captures real-time video or images of the user.
Pre-recorded Video: Uses existing videos for the try-on process.

Pose Detection:

Utilizes pose detection algorithms to identify key body points. In the provided code, the PoseDetector from the cvzone library is used to detect body landmarks.

Garment Mapping:

Garment Images: Preloaded images of clothing items to be overlaid on the user's image.
Overlay Techniques: Uses image processing techniques to correctly position and size the clothing item over the user's detected body points.

User Interaction:

Allows users to select different garments or accessories to try on. Interaction can be facilitated through gesture recognition or UI buttons.

Detailed Explanation of the Provided Code

Libraries and Initialization

import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture("Resources/Videos/1.mp4")
detector = PoseDetector()

cv2 for video capture and image processing.
cvzone for simplified computer vision tasks, including pose detection.
PoseDetector to identify and track body landmarks in the video.

Loading Resources

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
fixedRatio = 262 / 190
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

Loads available shirt images.
Defines ratios for resizing shirts based on body landmark distances.
Loads button images for user interaction (next and previous shirt).


Main Loop for Video Processing

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

Captures each frame from the video.
Detects pose and landmarks using PoseDetector.

Shirt Overlay Logic

    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

Calculates the shirt's width based on the distance between shoulder landmarks (lm11 and lm12).
Resizes the shirt image accordingly.
Uses cvzone.overlayPNG to overlay the shirt image onto the video frame at the calculated position.

User Interaction for Shirt Selection
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

Overlays navigation buttons for shirt selection.
Checks for hand positions to increase counters for shirt selection.
Changes the shirt image based on user interaction (hand positions).

Displaying the Result
    cv2.imshow("Image", img)
    cv2.waitKey(1)

Displays the processed video frame with the overlaid shirt and interaction buttons.


This code demonstrates the basic functionality of a virtual try-on system using pose detection and image overlay techniques. The user can see how different shirts look on them in real-time, and interact with the system to change the shirts. Advanced versions of such platforms may include more sophisticated pose detection, 3D modeling, better user interaction methods, and integration with e-commerce systems for a complete virtual shopping experience.






