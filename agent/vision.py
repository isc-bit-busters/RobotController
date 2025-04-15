import cv2
import numpy as np
import onnxruntime as ort

# ===================== CONFIGURATION =====================
MODEL_PATH = "yolov5n.onnx"
IMG_SIZE = 640
CONF_THRESHOLD = 0.1
IOU_THRESHOLD = 0.5
REAL_WIDTH_CM = 2.0
CALIBRATION_PATH = "camera_calibration.npz"

# ===================== INITIALISATION =====================
def load_model(model_path=MODEL_PATH):
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    return session, input_name

def load_calibration(path=CALIBRATION_PATH):
    calibration = np.load(path)
    camera_matrix = calibration["camera_matrix"]
    dist_coeffs = calibration["dist_coeffs"]
    focal_length = camera_matrix[0, 0]  # fx
    return camera_matrix, dist_coeffs, focal_length

# ===================== PRÉ-TRAITEMENT =====================
def preprocess_image(img, size):
    img_resized = cv2.resize(img, (size, size))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_input = img_rgb.transpose((2, 0, 1)) / 255.0
    img_input = np.expand_dims(img_input.astype(np.float32), axis=0)
    return img_input, img.shape, img_resized.shape

# ===================== POST-TRAITEMENT =====================
def postprocess(outputs, original_shape, resized_shape, focal_length):
    predictions = outputs[0]
    boxes, confidences, class_ids, results = [], [], [], []

    for pred in predictions[0]:
        pred = pred.astype(np.float32)
        if pred[4] < CONF_THRESHOLD:
            continue
        scores = pred[5:]
        class_id = np.argmax(scores)
        conf = scores[class_id]
        if conf < CONF_THRESHOLD:
            continue

        cx, cy, w, h = pred[:4]
        x = int((cx - w / 2) * original_shape[1] / resized_shape[1])
        y = int((cy - h / 2) * original_shape[0] / resized_shape[0])
        w = int(w * original_shape[1] / resized_shape[1])
        h = int(h * original_shape[0] / resized_shape[0])

        boxes.append([x, y, w, h])
        confidences.append(float(conf))
        class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, IOU_THRESHOLD)
    if isinstance(indices, tuple) or len(indices) == 0:
        return results

    for i in np.array(indices).flatten():
        x, y, w, h = boxes[i]
        distance = (REAL_WIDTH_CM * focal_length) / w
        aspect_ratio = float(min(w, h)) / max(w, h)
        if aspect_ratio > 0.5:
            results.append({
                "class_id": class_ids[i],
                "confidence": confidences[i],
                "position": (x, y, w, h),
                "distance_cm": distance
            })

    return results

# ===================== DÉTECTION =====================
def detect_cubes(image, session, input_name, camera_matrix, dist_coeffs, focal_length):
    # image peut être un chemin ou un tableau numpy
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise FileNotFoundError(f"❌ Image not found: {image}")

    # Undistortion
    image = cv2.undistort(image, camera_matrix, dist_coeffs)
    img_input, original_shape, resized_shape = preprocess_image(image, IMG_SIZE)
    outputs = session.run(None, {input_name: img_input})
    results = postprocess(outputs, original_shape, resized_shape, focal_length)
    return results
