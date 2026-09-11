import cv2
import numpy as np

# 웹캠 열기
cap = cv2.VideoCapture(0)

previous_point = None
canvas = None

# 그리기 색상
colors = [
    (0, 255, 0),    # 초록
    (255, 0, 0),    # 파랑
    (0, 0, 255),    # 빨강
    (0, 255, 255)   # 노랑
]

color_index = 0
draw_color = colors[color_index]

# 선 굵기
thicknesses = [3, 5, 10]
thickness_index = 1
line_thickness = thicknesses[thickness_index]

if cap.isOpened():
    print("카메라가 잡혔어요!")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 그린 선을 저장할 캔버스 만들기
        if canvas is None:
            canvas = np.zeros_like(frame)

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

        # 빨간색 영역의 윤곽선 찾기
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # 가장 큰 빨간색 영역의 중심점 찾기
        if contours:
            contour = max(contours, key=cv2.contourArea)
            moments = cv2.moments(contour)

            if moments["m00"] != 0:
                center_x = int(moments["m10"] / moments["m00"])
                center_y = int(moments["m01"] / moments["m00"])

                current_point = (center_x, center_y)

                # 이전 중심점과 현재 중심점을 선으로 연결
                if previous_point is not None:
                    cv2.line(
                        canvas,
                        previous_point,
                        current_point,
                        draw_color,
                        line_thickness
                    )

                previous_point = current_point

                # 현재 중심점 표시
                cv2.circle(
                    frame,
                    current_point,
                    10,
                    draw_color,
                    -1
                )
            else:
                previous_point = None

        else:
            previous_point = None

        # 빨간색으로 검출된 부분만 남기기
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # 웹캠 화면과 그린 선 합치기
        air_canvas = cv2.add(frame, canvas)

        cv2.imshow("Air Canvas", air_canvas)
        cv2.imshow("Red Mask", mask)
        cv2.imshow("Red Detection", result)

        key = cv2.waitKey(30)

        if key == 27:  # ESC 키
            break

        if key == ord('c') or key == ord('C'):  # C 키
            canvas = np.zeros_like(frame)
            previous_point = None

        if key == ord('p') or key == ord('P'):  # P 키
            color_index = (color_index + 1) % len(colors)
            draw_color = colors[color_index]

        if key == ord('t') or key == ord('T'):  # T 키
            thickness_index = (thickness_index + 1) % len(thicknesses)
            line_thickness = thicknesses[thickness_index]

else:
    print("카메라가 안 잡혔어요ㅠㅠ")

cap.release()
cv2.destroyAllWindows()