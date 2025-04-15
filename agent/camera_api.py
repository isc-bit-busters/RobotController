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

            camera_info = self.picam2.global_camera_info()
            if not camera_info:
                raise RuntimeError("Aucune caméra détectée !")

            print(f"Caméra(s) détectée(s) : {camera_info}")

            try:
                self.picam2.stop()
            except Exception as e:
                print(f"Aucune instance active à arrêter : {e}")

            self.picam2.configure(self.picam2.create_still_configuration(main={"size": self.resolution}))
            self.picam2.start()
            time.sleep(1)

        except RuntimeError as e:
            print(f"Erreur d'accès à la caméra : {e}")
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
