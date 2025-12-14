# main.py - Volume + CONTINUOUS Scroll Control

from camera_manager import CameraManager
from hand_tracker import HandTracker
from Volume_Control import VolumeController
import pyautogui
import cv2

pyautogui.FAILSAFE = False


def main():
    
    camera = CameraManager()
    hand_tracker = HandTracker()
    volume_controller = VolumeController()

    try:
        
        camera.initialize_camera()
        
        print("✓ Show your hand to the camera...")

        while True:
            
            ret, frame = camera.read_frame()
            if not ret:
                break

            frame_h, frame_w, _ = frame.shape
            center_y = frame_h // 2        # screen center
            DEAD_ZONE = 40                 # no scroll zone
            SCROLL_SPEED = 30              # smooth continuous speed

            results = hand_tracker.detect_hands(frame)

            if results.multi_hand_landmarks:
                
                for hand_landmarks in results.multi_hand_landmarks:

                    # Draw hand landmarks
                    hand_tracker.draw_hand_landmarks(frame, hand_landmarks)

                    # Finger positions
                    thumb_pos, index_pos = hand_tracker.get_finger_positions(
                        hand_landmarks, frame.shape
                    )

                    # ---------- VOLUME CONTROL ----------
                    distance = hand_tracker.calculate_distance(thumb_pos, index_pos)
                    volume_percent = volume_controller.set_volume(distance)
                    # -----------------------------------

                    # ---------- CONTINUOUS SCROLL ----------
                    index_y = hand_tracker.get_index_finger_y(
                        hand_landmarks, frame.shape
                    )

                    # Finger above center → scroll up
                    if index_y < center_y - DEAD_ZONE:
                        pyautogui.scroll(SCROLL_SPEED)

                    # Finger below center → scroll down
                    elif index_y > center_y + DEAD_ZONE:
                        pyautogui.scroll(-SCROLL_SPEED)
                    # ---------------------------------------

                    # Visualization
                    hand_tracker.draw_finger_visualization(
                        frame, thumb_pos, index_pos, distance
                    )

                    # UI info
                    cv2.putText(
                        frame,
                        f"Volume: {volume_percent}%",
                        (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

            # UI text
            cv2.putText(
                frame,
                "Continuous Hand Scroll + Volume Control",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Finger up/down = scroll | Pinch = volume",
                (50, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            camera.display_frame(frame)

            if camera.check_exit_key():
                break

    except Exception as e:
        print("Error:", e)

    finally:
        
        camera.release_camera()
        print("✓ Application closed successfully!")


if __name__ == "__main__":
    main()
