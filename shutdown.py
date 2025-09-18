import os
import cv2
import mediapipe as mp
from collections import deque

# Fungsi Untuk Shutdown Komputer
def shutdown_computer():
    try:
        if os.name == "nt":  # Windows
            os.system("shutdown /s /t 1")
        else:  # Linux atau Mac
            os.system("shutdown now")
    except Exception as e:
        print(f"Error saat shutdown: {e}")

# === Setup Mediapipe untuk deteksi tangan ===
mp_hand = mp.solutions.hands
hand_detector = mp_hand.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)
mp_drawer = mp.solutions.drawing_utils

# Buffer untuk menyimpan beberapa hasil gesture terakhir
history_gesture = deque(maxlen=5)

# Mengecek apakah jari (selain jempol) dalam posisi terbuka
def is_finger_extended(tip, pip):
    return tip.y < pip.y - 0.02

# Mengecek posisi jempol (berdasarkan sumbu X)
def is_thumb_extended(tip, ip, is_right=True):
    return tip.x > ip.x + 0.05 if is_right else tip.x < ip.x - 0.05

# ===== Fungsi utama pengenalan gesture =====
def detect_gesture(landmarks, hand_label="Right"):#Right sebagai pembeda tangan kanan/kiri
    lm = landmarks.landmark

    fingers_status = [
        is_thumb_extended(lm[mp_hand.HandLandmark.THUMB_TIP], lm[mp_hand.HandLandmark.THUMB_IP], hand_label == "Right"),
        is_finger_extended(lm[mp_hand.HandLandmark.INDEX_FINGER_TIP], lm[mp_hand.HandLandmark.INDEX_FINGER_PIP]),
        is_finger_extended(lm[mp_hand.HandLandmark.MIDDLE_FINGER_TIP], lm[mp_hand.HandLandmark.MIDDLE_FINGER_PIP]),
        is_finger_extended(lm[mp_hand.HandLandmark.RING_FINGER_TIP], lm[mp_hand.HandLandmark.RING_FINGER_PIP]),
        is_finger_extended(lm[mp_hand.HandLandmark.PINKY_TIP], lm[mp_hand.HandLandmark.PINKY_PIP])
    ]

    # Aturan deteksi gesture berdasarkan kombinasi jari
    gesture_map = {
        (False, False, True, False, False): "Fuck you",
        (False, True, True, True, True): "Halooo",
        (True, False, False, False, False): "Bagussss",
        (False, False, True, True, True): "Oke"
    }

    return gesture_map.get(tuple(fingers_status), "Gesture tidak diketahui")

# =============================
# Fungsi utama untuk memproses frame
# =============================
def process_frame(frame, detector):
    # Ubah gambar ke RGB karena Mediapipe bekerja dengan format RGB
    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = detector.process(rgb_img)

    if results.multi_hand_landmarks:
        for idx, lm in enumerate(results.multi_hand_landmarks):
            # Tentukan apakah tangan kanan atau kiri
            label = "Right"
            if results.multi_handedness:
                label = results.multi_handedness[idx].classification[0].label

            # Deteksi gesture
            gesture_detected = detect_gesture(lm, label)
            history_gesture.append(gesture_detected)

            # Pilih gesture mayoritas dari buffer (stabilisasi)
            final_gesture = max(set(history_gesture), key=history_gesture.count)

            # Jika gesture adalah "Fuck you", shutdown komputer
            if final_gesture == "Fuck you":
                # Tambahan keamanan: pastikan terdeteksi setidaknya 3 kali dalam buffer
                if history_gesture.count("Fuck you") >= 3:
                    print("Gesture 'Fuck you' terdeteksi konsisten! Komputer akan shutdown...")
                    shutdown_computer()

            # Gambar landmark tangan di frame
            mp_drawer.draw_landmarks(frame, lm, mp_hand.HAND_CONNECTIONS)

            # Tampilkan teks nama gesture
            cv2.putText(frame, final_gesture, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    return frame

# ===== MAIN LOOP =====
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Kamera tidak dapat diakses.")
    exit()

while True:
    ret, frame = camera.read()
    if not ret:
        print("Tidak bisa membaca frame dari kamera.")
        break

    frame = process_frame(frame, hand_detector)
    cv2.imshow("Deteksi Gesture Tangan", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
