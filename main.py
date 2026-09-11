import cv2
import numpy as np

# 웹캠 열기
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("카메라가 잡혔어요!")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 웹캠 이미지를 HSV로 변환
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 빨간색 범위
        lower_red1 = np.array([0, 150, 100])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 150, 100])
        upper_red2 = np.array([179, 255, 255])

        # 빨간색 영역 검출
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # 빨간색으로 검출된 부분만 남기기
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Air Canvas", frame)
        cv2.imshow("Red Mask", mask)
        cv2.imshow("Red Detection", result)

        if cv2.waitKey(30) == 27:  # ESC 키
            break

else:
    print("카메라가 안 잡혔어요ㅠㅠ")

cap.release()
cv2.destroyAllWindows()