import cv2
from fer import FER

detector = FER(mtcnn=True)
cap = cv2.VideoCapture(0)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    if frame_count % 10 == 0:
        emotions = detector.detect_emotions(frame)
        if emotions:
            emotion_data = emotions[0]["emotions"]
            dominant_emotion = max(emotion_data, key=emotion_data.get)
            confidence = emotion_data[dominant_emotion]

            print(f"🧠 Dominant Emotion: {dominant_emotion.upper()} ({confidence:.2f})")

            cv2.putText(
                frame,
                f"{dominant_emotion.upper()} ({confidence:.2f})",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3,
                cv2.LINE_AA
            )

    frame_count += 1
    cv2.imshow("EmoSync - Real Time Emotion", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
