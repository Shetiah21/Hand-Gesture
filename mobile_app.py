import socket
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import accelerometer

# Configuration
THRESHOLD_RAISE = 8
THRESHOLD_WAVE = 2
WINDOW_SIZE = 10
PC_IP = " 192.168.1.14" # <--- IMPORTANT: Update this to your PC's IP
PORT = 5000

class MotionApp(App):
    def build(self):
        self.x_values = []
        self.label = Label(text="Waiting for motion...", font_size='20sp')
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.update, 0.1)
        except:
            self.label.text = "Accelerometer Error"
        return self.label

    def send_command(self, command):
        try:
            print(f"Sending {command} to {PC_IP}") # ADD THIS
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((PC_IP, PORT))
            s.send(command.encode())
            print(f"Successfully sent {command} to PC!") # ADD THIS
            s.close()
            
        except:
            print("Could not connect to PC")
            print(f"Error sending: {e}") # ADD THIS

    def update(self, dt):
        val = accelerometer.acceleration
        if val and val != (None, None, None):
            x, y, z = val
            if y > THRESHOLD_RAISE:
                self.label.text = "Hand Raised!"
            else:
                self.x_values.append(x)
                if len(self.x_values) > WINDOW_SIZE:
                    self.x_values.pop(0)
                    diffs = [abs(self.x_values[i] - self.x_values[i-1]) for i in range(1, len(self.x_values))]
                    if sum(d > THRESHOLD_WAVE for d in diffs) > 3:
                        self.label.text = "Wave detected! -> NEXT"
                        self.send_command("NEXT")
                        self.x_values = []

if __name__ == "__main__":
    MotionApp().run()