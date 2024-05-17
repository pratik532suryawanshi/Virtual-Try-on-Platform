import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector
import time
import matplotlib.pyplot as plt

cap = cv2.VideoCapture("Resources/Videos/1.mp4")
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Data collection variables
shirtSwitchCount = 0
startTime = time.time()
shirtSwitchTimestamps = []

while True:
    success, img = cap.read()
    if not success:
        break
    
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    
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
                    shirtSwitchCount += 1
                    shirtSwitchTimestamps.append(time.time() - startTime)
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
                    shirtSwitchCount += 1
                    shirtSwitchTimestamps.append(time.time() - startTime)
        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Plotting the data
plt.figure(figsize=(10, 5))

# Plotting shirt switch counts over time
plt.subplot(1, 2, 1)
plt.plot(shirtSwitchTimestamps, range(1, shirtSwitchCount + 1), marker='o')
plt.xlabel('Time (s)')
plt.ylabel('Shirt Switch Count')
plt.title('Shirt Switches Over Time')

# Plotting a pie chart of shirt switch directions
switchDirections = ['Right Switch', 'Left Switch']
switchCounts = [shirtSwitchTimestamps.count('right'), shirtSwitchTimestamps.count('left')]
plt.subplot(1, 2, 2)
plt.pie(switchCounts, labels=switchDirections, autopct='%1.1f%%')
plt.title('Shirt Switch Directions')

plt.tight_layout()
plt.show()
