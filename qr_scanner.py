import cv2
import numpy as np
from pyzbar.pyzbar import decode

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # width
    cap.set(4, 480)  # height

    print("?? QR Code Scanner started. Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("?? Failed to capture video frame.")
            break

        for code in decode(frame):
            data = code.data.decode('utf-8')
            points = code.polygon

            # get convex hull if needed
            if len(points) > 4:
                hull = cv2.convexHull(np.array([p for p in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            # draw bounding box
            n = len(hull)
            for j in range(n):
                pt1 = (hull[j][0], hull[j][1])
                pt2 = (hull[(j + 1) % n][0], hull[(j + 1) % n][1])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

            x, y, w, h = code.rect
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 0), 2)
            print(f"? QR Code Detected: {data}")

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("?? Scanner closed.")

if __name__ == "__main__":
    main()
