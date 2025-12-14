# main.py - Main application that uses all modules
from camera_manager import CameraManager
from hand_tracker import HandTracker
import cv2

def main():
    # Initialize components
    camera = CameraManager()
    hand_tracker = HandTracker()
    
    try:
        # Start camera
        camera.initialize_camera()
        
        print("✓ Show your hand to the camera...")
        
        # Main loop
        while True:
            # Read frame from camera
            ret, frame = camera.read_frame()
            if not ret:
                break
            
            # Detect hands
            results = hand_tracker.detect_hands(frame)
            
            # Process hand detection
            if results.multi_hand_landmarks:
                #loop through each hand and process them 
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    hand_tracker.draw_hand_landmarks(frame, hand_landmarks)
                    
                    # Get finger positions
                    thumb_pos, index_pos = hand_tracker.get_finger_positions(
                        hand_landmarks, frame.shape
                    )
                    
                    # Calculate distance
                    distance = hand_tracker.calculate_distance(thumb_pos, index_pos)
                    
                    # Draw visualization
                    hand_tracker.draw_finger_visualization(
                        frame, thumb_pos, index_pos, distance
                    )
            
            # Display UI
            cv2.putText(frame, "Hand Gesture Volume Control", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", (50, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show frame
            camera.display_frame(frame)
            
            # Check for exit
            if camera.check_exit_key():
                break
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        camera.release_camera()
        print("✓ Application closed successfully!")

if __name__ == "__main__":
    main()