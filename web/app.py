from flask import Flask, render_template, request, jsonify
from fer import FER
import numpy as np
from PIL import Image
import io
import cv2

app = Flask(__name__)
detector = FER(mtcnn=False)

def read_image_from_bytes(file_bytes):
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = np.array(image)  # RGB
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "frame" not in request.files:
        return jsonify({"error": "No frame part"}), 400

    file = request.files["frame"]
    img = read_image_from_bytes(file.read())

    img = cv2.resize(img, (640, 480))

    results = detector.detect_emotions(img)

    if not results:
        return jsonify({"face": False, "emotions": {}, "dominant": None})

    emotions = results[0]["emotions"]
    emotions = {k: float(v) for k, v in emotions.items()}
    dominant = max(emotions, key=emotions.get)

    return jsonify({
        "face": True,
        "emotions": emotions,
        "dominant": dominant,
        "confidence": emotions[dominant]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
