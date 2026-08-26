# import cv2
# import mediapipe as mp

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()

# mp_draw = mp.solutions.drawing_utils


# cap = cv2.VideoCapture(0)

# while True:
#     success, frame = cap.read()


#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     result = hands.process(rgb)

#     if result.multi_hand_landmarks:
#         for hand in result.multi_hand_landmarks:
#             mp_draw.draw_landmarks(
#                 frame,
#                 hand,
#                 mp_hands.HAND_CONNECTIONS
#             )

#     cv2.imshow("Hand Tracking", frame)

#     if cv2.waitKey(1) == 27: 
#         break

# cap.release()
# cv2.destroyAllWindows()

# from ursina import *

# app = Ursina()

# cube = Entity(
#     model='cube',
#     color=color.azure,
#     scale=2
# )

# EditorCamera()

# app.run()

import cv2
import mediapipe as mp
from ursina import *

# =========================
# MEDIA PIPE
# =========================

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


# =========================
# URSINA
# =========================

app = Ursina()

cube = Entity(
    model='cube',
    color=color.azure,
    scale=2
)

EditorCamera()


# =========================
# UPDATE
# =========================

def update():

    success, frame = cap.read()

    if not success:
        return

    # Membalik kamera agar seperti cermin
    frame = cv2.flip(frame, 1)

    # BGR -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Deteksi tangan
    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            # Landmark ujung jari telunjuk
            index_finger = hand.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_TIP
            ]

            # Nilai X MediaPipe = 0 sampai 1
            x = index_finger.x

            # Ubah 0-1 menjadi posisi Ursina
            cube.x = (x - 0.5) * 10

            # Gambar landmark tangan
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    # Tampilkan kamera
    cv2.imshow("Hand Tracking", frame)

    # ESC untuk keluar
    if cv2.waitKey(1) == 27:
        application.quit()


# =========================
# RUN
# =========================

app.run()

cap.release()
cv2.destroyAllWindows()