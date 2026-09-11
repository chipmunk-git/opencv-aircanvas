import cv2

# 웹캠 열기
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("카메라가 잡혔어요!")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Air Canvas", frame)

        if cv2.waitKey(30) == 27:  # ESC 키
            break

else:
    print("카메라가 안 잡혔어요ㅠㅠ")

cap.release()
cv2.destroyAllWindows()