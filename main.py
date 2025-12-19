# main.py - Hand Gesture + Mobile Control System

from camera_manager import CameraManager
from hand_tracker import HandTracker
from Volume_Control import VolumeController

import cv2
import time
import socket
import threading
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController


# ================= MOBILE SERVER =================
def socket_server_thread():
    keyboard = KeyboardController()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5000))
    server.listen(5)

    print("✓ Mobile Server running on port 5000")

    while True:
        try:
            conn, addr = server.accept()
            request = conn.recv(1024).decode()

            if "GET /next" in request:
                print("✓ Phone Command: NEXT")
                keyboard.press(Key.right)
                keyboard.release(Key.right)

            response = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Remote</title>
</head>
<body style="background:#222;color:white;text-align:center;
font-family:sans-serif;display:flex;flex-direction:column;
justify-content:center;align-items:center;height:100vh;margin:0;">

<h1>SHAKE OR TAP</h1>
<a href="/next"
style="padding:40px 80px;background:#28a745;color:white;
font-size:30px;text-decoration:none;border-radius:15px;">
NEXT PAGE</a>

<script>
let lastX = 0;
let threshold = 15;

window.addEventListener('devicemotion', (event) => {
    let x = event.accelerationIncludingGravity.x;
    if (Math.abs(x - lastX) > threshold) {
        fetch('/next');
    }
    lastX = x;
});
</script>

</body>
</html>
"""
            conn.send(response.encode())
            conn.close()

        except Exception as e:
            print("Server Error:", e)


# ================= MAIN SYSTEM =================
def main():
    # Start mobile server
    mobile_thread = threading.Thread(
        target=socket_server_thread, daemon=True
    )
    mobile_thread.start()

    # Initialize components
    camera = CameraManager()
    hand_tracker = HandTracker()
    volume_controller = VolumeController()
    mouse = MouseController()

    DEAD_ZONE = 40
    SCROLL_SPEED = 1

    try:
        camera.initialize_camera()
        print("✓ System started successfully")

        while True:
            
            ret, frame = camera.read_frame()
            if not ret:
                break

            frame_h, frame_w, _ = frame.shape
            center_y = frame_h // 2
            

            results = hand_tracker.detect_hands(frame)

            if results and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    
                    hand_tracker.draw_hand_landmarks(frame, hand_landmarks)

                    thumb_pos, index_pos = hand_tracker.get_finger_positions(
                        hand_landmarks, frame.shape
                    )

                    distance = hand_tracker.calculate_distance(
                        thumb_pos, index_pos
                    )

                    # -------- MUTE / VOLUME --------
                    if hand_tracker.is_hand_closed(hand_landmarks):
                        volume_controller.mute_volume()
                        
                        cv2.putText(
                            frame, "MUTED", (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 3
                        )
                    else:
                        volume_controller.unmute_volume()
                        volume_controller.set_volume(distance)

                        # -------- CONTINUOUS SCROLL --------
                        index_y = hand_tracker.get_index_finger_y(
                            hand_landmarks, frame.shape
                        )

                        if index_y < center_y - DEAD_ZONE:
                            mouse.scroll(0, SCROLL_SPEED)
                        elif index_y > center_y + DEAD_ZONE:
                            mouse.scroll(0, -SCROLL_SPEED)

                    hand_tracker.draw_finger_visualization(
                        frame, thumb_pos, index_pos, distance
                    )

            # -------- UI --------
            cv2.line(
                frame, (0, center_y),
                (frame_w, center_y),
                (120, 120, 120), 1
            )

            cv2.putText(
                frame,
                "Gesture + Mobile Control Active",
                (50, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255), 2
            )

            cv2.imshow("Hand Control System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("Error:", e)

    finally:
        camera.release_camera()
        cv2.destroyAllWindows()
        print("✓ Application closed safely")


if __name__ == "__main__":
    main()
