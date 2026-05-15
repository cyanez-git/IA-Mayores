"""
Feed de cámara IP vía RTSP + detección de postura con MediaPipe.
MOCK_MODE=true devuelve poses simuladas sin cámara.
"""
import os
import random
import threading
import time
from dataclasses import dataclass

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
RTSP_URL = os.getenv("RTSP_URL", "rtsp://admin:admin@192.168.1.100:554/stream1")
MOCK_INTERVAL = 2


@dataclass
class PoseReading:
    person_detected: bool
    is_standing: bool      # True=de pie, False=en el suelo
    confidence: float      # 0.0 - 1.0
    timestamp: float


_latest: PoseReading | None = None
_lock = threading.Lock()


def get_latest() -> PoseReading | None:
    with _lock:
        return _latest


def _set_latest(reading: PoseReading):
    global _latest
    with _lock:
        _latest = reading


def _mock_loop():
    while True:
        scenario = random.choices(
            ["standing", "fallen", "absent"],
            weights=[80, 5, 15]
        )[0]

        if scenario == "standing":
            reading = PoseReading(
                person_detected=True,
                is_standing=True,
                confidence=round(random.uniform(0.80, 0.99), 2),
                timestamp=time.time(),
            )
        elif scenario == "fallen":
            reading = PoseReading(
                person_detected=True,
                is_standing=False,
                confidence=round(random.uniform(0.75, 0.95), 2),
                timestamp=time.time(),
            )
        else:
            reading = PoseReading(
                person_detected=False,
                is_standing=False,
                confidence=0.0,
                timestamp=time.time(),
            )

        _set_latest(reading)
        time.sleep(MOCK_INTERVAL)


def _real_loop():
    """Captura RTSP y analiza postura con MediaPipe."""
    try:
        import cv2
        import mediapipe as mp
    except ImportError:
        print("[Cámara] cv2 o mediapipe no instalados. Usando mock.")
        _mock_loop()
        return

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        print(f"[Cámara] No se pudo abrir {RTSP_URL}. Usando mock.")
        _mock_loop()
        return

    print(f"[Cámara] Conectado a {RTSP_URL}")

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # Hombros vs caderas: si caderas están al nivel de hombros → caído
            left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
            is_standing = (left_hip_y - left_shoulder_y) > 0.15

            reading = PoseReading(
                person_detected=True,
                is_standing=is_standing,
                confidence=round(results.pose_landmarks.landmark[0].visibility, 2),
                timestamp=time.time(),
            )
        else:
            reading = PoseReading(
                person_detected=False,
                is_standing=False,
                confidence=0.0,
                timestamp=time.time(),
            )

        _set_latest(reading)
        time.sleep(0.5)


def start(background: bool = True):
    target = _mock_loop if MOCK_MODE else _real_loop
    mode = "MOCK" if MOCK_MODE else f"RTSP {RTSP_URL}"
    print(f"[Cámara] Iniciando en modo {mode}")
    t = threading.Thread(target=target, daemon=True)
    t.start()
    if not background:
        t.join()
