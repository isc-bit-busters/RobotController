from picamera2 import Picamera2
import cv2
import time
import sys


class CameraHandler:
    def __init__(self, resolution=(640, 480)):
        self.resolution = resolution
        self.picam2 = None
        
    def initialize_camera(self):
        try:
            self.picam2 = Picamera2()
            
            # Sensor mode selection (prioritize 1080p)
            config = self.picam2.create_video_configuration(
                main={
                    "size": (1920, 1080),  # Optimal for OV5647
                    "format": "BGR888",     # OpenCV-compatible
                },
                controls={
                    "FrameRate": 30,        # Target 30fps
                    "AwbEnable": True,      # Auto white balance  
                    "AnalogueGain": 1.0,    # Reduce noise
                },
                queue=False,                # Reduce latency
                buffer_count=4,             # Balance performance/memory
            )
            
            self.picam2.configure(config)
            self.picam2.start()
            time.sleep(2)  # Warm-up for AWB/exposure
            
        except Exception as e:
            print(f"Camera error: {e}")
            raise
        
    def capture_image(self, convert_rgb=True):
        if self.picam2 is None:
            raise RuntimeError("Caméra non initialisée.")

        frame = self.picam2.capture_array()
        if convert_rgb:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        print("✅ Image capturée.")
        return frame

    def save_image(self, frame, output_path="captured_image.jpg"):
        cv2.imwrite(output_path, frame)
        print(f"Image enregistrée sous '{output_path}'.")

    def close(self):
        if self.picam2:
            self.picam2.stop()
            print("Caméra arrêtée proprement.")


# Exemple d’utilisation si exécuté directement
if __name__ == "__main__":
    try:
        cam = CameraHandler()
        cam.initialize_camera()
        img = cam.capture_image()
        cam.save_image(img)
        cam.close()

    except Exception as e:
        print(f"❌ Erreur dans le script principal : {e}")
        sys.exit(1)
