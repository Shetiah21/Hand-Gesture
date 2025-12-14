# camera_manager.py - Handles camera operations
import cv2

class CameraManager:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
    
    def initialize_camera(self):
        "Initialize the camera"
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise Exception("Error: Could not open webcam")
        print("✓ Webcam initialized successfully!")
        return True
    
    def read_frame(self):
        """Read a frame from the camera"""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Mirror effect
        return ret, frame
    
    def release_camera(self):
        "Release camera resources"
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
    def display_frame(self, frame, window_name='Hand Gesture Volume Control'):
        "Display the frame in a window"
        cv2.imshow(window_name, frame)
    
    def check_exit_key(self):
        "Check if 'q' key is pressed to exit"
        return cv2.waitKey(1) & 0xFF == ord('q')