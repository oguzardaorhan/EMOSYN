import gradio as gr
from fer import FER
import cv2

detector = FER(mtcnn=True)

def analyze_emotion(frame):

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    result = detector.detect_emotions(frame)
    if result:
        emotions = result[0]["emotions"]
        dominant_emotion = max(emotions, key=emotions.get)
        confidence = emotions[dominant_emotion]
        return {dominant_emotion: confidence}
    else:
        return {"No Face Detected": 0.0}

iface = gr.Interface(
    fn=analyze_emotion,
    inputs=gr.Image(sources="webcam", streaming=True),
    outputs=gr.Label(num_top_classes=3),
    live=True,
    title="🎭 EmoSync Web",
    description="Gerçek zamanlı yüz ifadesi analizi (FER + OpenCV)"
)

iface.launch()
