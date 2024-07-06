from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import pyautogui
import math
import time

app = Flask(__name__)

# Initialize Mediapipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Get screen size for cursor control
screen_width, screen_height = pyautogui.size()

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def gen_frames():
    cap = cv2.VideoCapture(0)
    drag_active = False
    gesture_start_time = 0
    click_threshold_time = 0.2  # seconds
    drag_threshold_time = 0.5  # seconds

    while True:
        success, img = cap.read()
        if not success:
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark

                # Extract landmark positions
                x1 = int(landmarks[8].x * screen_width)  # Index finger tip
                y1 = int(landmarks[8].y * screen_height)
                x_thumb = int(landmarks[4].x * screen_width)  # Thumb tip
                y_thumb = int(landmarks[4].y * screen_height)

                # Move the cursor
                pyautogui.moveTo(screen_width - x1, y1)

                # Calculate the distance between thumb and index finger tips
                distance = calculate_distance(landmarks[4], landmarks[8])
                
                # Define a threshold for click
                click_threshold = 0.05  # Adjust this value based on your setup

                if distance < click_threshold:
                    if not drag_active:
                        if gesture_start_time == 0:
                            gesture_start_time = time.time()
                        elapsed_time = time.time() - gesture_start_time

                        if elapsed_time > drag_threshold_time:
                            pyautogui.mouseDown()
                            drag_active = True
                        elif elapsed_time > click_threshold_time:
                            pyautogui.click()
                            gesture_start_time = 0
                else:
                    if drag_active:
                        pyautogui.mouseUp()
                        drag_active = False
                    gesture_start_time = 0

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
