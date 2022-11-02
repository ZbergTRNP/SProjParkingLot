import cvzone
import numpy as np
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from vidstab import VidStab

image_file = 'carParkImg.png'
@@ -19,11 +20,17 @@
stabilizer.stabilize(input_path=filepath, output_path='Output.mp4')

# Caps Video and Sets it to Cap with "CarParkPos" as the position list for spots
video_file = 'Output.mp4'
start_frame = 1
while True:
    with open(data_file, "r") as data:
        points = yaml.safe_load(data)
        detector = MotionDetector(video_file, points, int(start_frame))
        detector.detect_motion()

def empty(a):
    pass

# Creates and Handles Options Window, First Number is Starting Num
cv2.namedWindow("Options")
cv2.resizeWindow("Options", 640, 240)
cv2.createTrackbar("Val1", "Options", 34, 50, empty)
cv2.createTrackbar("Val2", "Options", 16, 50, empty)
cv2.createTrackbar("Val3", "Options", 5, 50, empty)


def checkSpaces():
    spaces = 0
    for pos in posList:
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 200, 0)
            thic = 5
            spaces += 1

        else:
            color = (0, 0, 200)
            thic = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)

    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=10,
                       colorR=(40, 40, 40))


while True:

    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # img = cv2.imread('img.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Sets up Trackbars for Calibration
    val1 = cv2.getTrackbarPos("Val1", "Options")
    val2 = cv2.getTrackbarPos("Val2", "Options")
    val3 = cv2.getTrackbarPos("Val3", "Options")

    # Makes sure values are set correctly
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    # Uses Vals to do Thresholding on the Video For Calibration
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    checkSpaces()
    # Display Output

    cv2.imshow("Output", img)
    # cv2.imshow("ImageGray", imgThres)
    # cv2.imshow("ImageBlur", imgBlur)
    key = cv2.waitKey(1)
    if key == ord('r'):
        pass
