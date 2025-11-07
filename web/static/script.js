let video = document.getElementById("video");
let startBtn = document.getElementById("startBtn");
let stopBtn = document.getElementById("stopBtn");
let emotionBadge = document.querySelector(".emotion");
let confBadge = document.getElementById("conf");

let stream = null;
let intervalId = null;
let canvas = document.createElement("canvas");

const SEND_INTERVAL_MS = 1000;
const WIDTH = 640;
const HEIGHT = 480;

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment", width: { ideal: WIDTH }, height: { ideal: HEIGHT } },
      audio: false
    });
    video.srcObject = stream;
    video.onloadedmetadata = () => video.play();
  } catch (e) {
    alert("Kameraya erişim reddedildi veya hata: " + e.message);
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(t => t.stop());
    stream = null;
  }
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}

function startSending() {
  canvas.width = WIDTH;
  canvas.height = HEIGHT;
  const ctx = canvas.getContext("2d");

  intervalId = setInterval(async () => {
    try {
      ctx.drawImage(video, 0, 0, WIDTH, HEIGHT);
      const blob = await new Promise(res => canvas.toBlob(res, "image/jpeg", 0.6));
      const form = new FormData();
      form.append("frame", blob, "frame.jpg");

      const resp = await fetch("/analyze", { method: "POST", body: form });
      const data = await resp.json();

      if (!data.face) {
        emotionBadge.textContent = "No face";
        confBadge.textContent = "0.00";
      } else {
        const dom = data.dominant;
        const conf = (data.confidence || 0).toFixed(2);
        emotionBadge.textContent = dom.toUpperCase();
        confBadge.textContent = conf;
        let color = "#10B981";
        if (dom === "sad") color = "#3B82F6";
        else if (dom === "angry") color = "#EF4444";
        else if (dom === "surprise") color = "#F59E0B";
        else if (dom === "neutral") color = "#6B7280";
        document.querySelector(".badge.emotion").style.background = color;
      }
    } catch (e) {
      console.error("analyze error", e);
    }
  }, SEND_INTERVAL_MS);
}

startBtn.onclick = async () => {
  await startCamera();
  startSending();
};
stopBtn.onclick = () => {
  stopCamera();
  emotionBadge.textContent = "Stopped";
  confBadge.textContent = "0.00";
};
