# hand_tracker.py - Handles hand detection and tracking
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
        "Detect hands in the frame and return landmarks"
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results
    
    def draw_hand_landmarks(self, frame, hand_landmarks):
        "Draw hand landmarks and connections on the frame"
        self.mp_drawing.draw_landmarks(
            frame, 
            hand_landmarks, 
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )
    
    def get_finger_positions(self, hand_landmarks, frame_shape):
        "Get thumb and index finger positions in pixel coordinates"
        # Landmark indices: 4=thumb tip, 8=index finger tip
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        
        h, w, c = frame_shape
        thumb_x = int(thumb_tip.x * w)
        thumb_y = int(thumb_tip.y * h)
        index_x = int(index_tip.x * w)
        index_y = int(index_tip.y * h)
        
        return (thumb_x, thumb_y), (index_x, index_y)
    
    def calculate_distance(self, point1, point2):
        "Calculate Euclidean distance between two points"
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    
    def draw_finger_visualization(self, frame, thumb_pos, index_pos, distance):
        "Draw visualization for fingers and distance"
        # Draw circles on finger tips
        cv2.circle(frame, thumb_pos, 10, (0, 0, 255), -1)  # Red for thumb
        cv2.circle(frame, index_pos, 10, (255, 0, 0), -1)  # Blue for index
        
        # Draw line between fingers
        cv2.line(frame, thumb_pos, index_pos, (0, 255, 255), 3)
        
        # Display distance
        cv2.putText(frame, f"Distance: {int(distance)}", (50, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)