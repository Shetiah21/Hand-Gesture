import cv2
import mediapipe as mp
import math


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✓ Hand tracking initialized!")

    def detect_hands(self, frame):
        """Detect hands in the frame and return landmarks"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results

    def get_index_finger_y(self, hand_landmarks, frame_shape):
        """Get the y-coordinate of the index finger tip"""
        index_tip = hand_landmarks.landmark[8]
        h, w, c = frame_shape
        index_y = int(index_tip.y * h)
        return index_y

    def draw_hand_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks and connections on the frame"""
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

    def get_finger_positions(self, hand_landmarks, frame_shape):
        """Get thumb and index finger positions in pixel coordinates"""
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]

        h, w, c = frame_shape
        thumb_x = int(thumb_tip.x * w)
        thumb_y = int(thumb_tip.y * h)
        index_x = int(index_tip.x * w)
        index_y = int(index_tip.y * h)

        return (thumb_x, thumb_y), (index_x, index_y)

    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt(
            (point2[0] - point1[0]) ** 2 +
            (point2[1] - point1[1]) ** 2
        )

    def draw_finger_visualization(self, frame, thumb_pos, index_pos, distance):
        """Draw visualization for fingers and distance"""
        cv2.circle(frame, thumb_pos, 10, (0, 0, 255), -1)
        cv2.circle(frame, index_pos, 10, (255, 0, 0), -1)
        cv2.line(frame, thumb_pos, index_pos, (0, 255, 255), 3)

        cv2.putText(
            frame,
            f"Distance: {int(distance)}",
            (50, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # ✅ NEW FUNCTION (CORRECT PLACE)
    def is_hand_closed(self, hand_landmarks):
        """
        Detect if the hand is closed (fist)
        """
        finger_tips = [8, 12, 16, 20]    # index, middle, ring, pinky
        finger_bases = [6, 10, 14, 18]   # base joints

        closed_fingers = 0

        for tip, base in zip(finger_tips, finger_bases):
            if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[base].y:
                closed_fingers += 1

        return closed_fingers == 4
