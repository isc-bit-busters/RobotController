import cv2
def takePicture(camera_index):
    #check camera indexes
    for i in range(10):
        cap = cv2.VideoCapture(i) 
        if cap.isOpened():
            print(f"Camera found at index {i}")
            cap.release()
        else:
            print(f"Camera not found at index {i}")
    #take picture

    cap = cv2.VideoCapture(camera_index)
    if cap.isOpened():
        print(f"Camera found at index {camera_index}")
        ret, frame = cap.read()
        if ret:
            image_path = f"captured_image_{camera_index}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Image saved to {image_path}")
        else:
            print(f"Error capturing image at index {camera_index}")
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Camera not found at index {camera_index}")
    

def detectAruco(path):
    takePicture(4)

    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    centers = []
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters = cv2.aruco.DetectorParameters()

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
        for i, corner in enumerate(corners):
            center_x = int((corner[0][0][0] + corner[0][2][0]) / 2)
            center_y = int((corner[0][0][1] + corner[0][2][1]) / 2)
            centers.append((center_x, center_y))
            print(center_x, center_y)
            cv2.circle(image, (center_x, center_y), 5, (0, 255, 0), -1)

    cv2.imshow("Detected Markers", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return centers


takePicture(4)
detectAruco("captured_image_4.jpg")