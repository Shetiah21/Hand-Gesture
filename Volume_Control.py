from pycaw.pycaw import AudioUtilities
import numpy as np


class VolumeController:
    def __init__(self):
        # Get default speakers
        device = AudioUtilities.GetSpeakers()

        # Access the volume interface
        self.volume = device.EndpointVolume

        # Store previous volume for smoothing
        self.prev_volume = 0.0

        # Get min and max system volume
        self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()

        print("✓ Volume controller initialized!")

    def map_distance_to_volume(self, distance, min_dist=30, max_dist=200):
        """
        Convert finger distance to volume level (0.0 - 1.0)
        """
        vol = (distance - min_dist) / (max_dist - min_dist)
        return np.clip(vol, 0.0, 1.0)

    def set_volume(self, distance):
        """
        Smooth and apply volume to Windows OS
        """
        vol_level = self.map_distance_to_volume(distance)

        # Smooth volume changes
        vol_level = 0.8 * self.prev_volume + 0.2 * vol_level
        self.prev_volume = vol_level

        # Convert normalized volume to Windows volume range
        win_vol = np.interp(vol_level, [0, 1], [self.min_vol, self.max_vol])
        self.volume.SetMasterVolumeLevel(win_vol, None)

        return int(vol_level * 100)

    # ✅ MUTE FUNCTIONS (FIXED)

    def mute_volume(self):
        """Mute the system volume"""
        self.volume.SetMute(True, None)

    def unmute_volume(self):
        """Unmute the system volume"""
        self.volume.SetMute(False, None)
