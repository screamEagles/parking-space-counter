import cv2
import pickle


width, height = 107, 48

try:
    with open("car_park_position", "rb") as f:
        positions_list = pickle.load(f)
except:
    positions_list = []


def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        positions_list.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(positions_list):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positions_list.pop(i)

    with open("car_park_position", "wb") as f:
        pickle.dump(positions_list, f)


while True:
    img = cv2.imread('car_park_img.png')
    for position in positions_list:
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 255, 0), 2)


    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break