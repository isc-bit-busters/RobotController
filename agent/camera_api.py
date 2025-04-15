from picamera2 import Picamera2
import cv2
import sys
import time

try:
    picam2 = Picamera2()

    camera_info = picam2.global_camera_info()
    if not camera_info:
        print("❌ Aucune caméra détectée !")
        sys.exit(1)

    print(f"✅ Caméra(s) détectée(s) : {camera_info}")

    # Libère d'abord toute ancienne instance (important dans Docker !)
    try:
    	picam2.stop()  # Juste au cas où, pas de souci si elle n'est pas encore démarrée
    except Exception as e:
    	print(f"ℹ️ Aucune instance active à arrêter : {e}")


    # Configuration
    picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
    picam2.start()
    time.sleep(1)

    # Capture
    frame = picam2.capture_array()
    cv2.imwrite("captured_image.jpg", frame)
    print("✅ Image capturée et enregistrée sous 'captured_image.jpg'.")

    # Clean exit
    picam2.stop()

except RuntimeError as e:
    print(f"❌ Erreur d'accès à la caméra : {e}")
    print("💡 Vérifie qu'aucun autre processus ne bloque la caméra dans Docker.")
    sys.exit(1)

except Exception as e:
    print(f"❌ Erreur : {e}")
    sys.exit(1)
