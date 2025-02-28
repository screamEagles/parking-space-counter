import cv2
import pickle
import cvzone  # cvzone version: 1.5.3
import numpy as np

cap = cv2.VideoCapture("car_park.mp4")


with open("car_park_position", "rb") as f:
    positions_list = pickle.load(f)

width, height = 107, 48


def check_parking_space(img_process):
    space_counter = 0

    for position in positions_list:
        x, y = position
        img_crop = img_process[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), img_crop)
        count = cv2.countNonZero(img_crop)

        if count < 900:
            colour = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            colour = (0, 0, 255)
            thickness = 2
    
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), colour, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=colour)

    cvzone.putTextRect(img, f"Available Spaces: {space_counter}/{len(positions_list)}", (100, 50), scale=2.5, thickness=5, offset=20, colorR=(0, 200, 0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_grey, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    check_parking_space(img_dilate)
    # for position in positions_list:
    #     cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 255, 0), 2)
    
    cv2.imshow("Image", img)
    # cv2.imshow("Image Blur", img_blur)
    # cv2.imshow("Image Threshold", img_threshold)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
