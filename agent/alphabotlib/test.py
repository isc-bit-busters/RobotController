import cv2
import numpy as np
from PIL import Image

def load_points(image_path):
    # Load the image
    img = Image.open(image_path).convert('RGBA')
    img_array = np.array(img)
    
    # Create dictionaries to store points by RGB values
    a_points = {}  # Alpha = 255
    b_points = {}  # Alpha < 255
    
    # Iterate through each pixel
    height, width = img_array.shape[:2]
    for y in range(height):
        for x in range(width):
            r, g, b, a = img_array[y, x]
            rgb_key = (r, g, b)
            
            # Skip transparent pixels (could adjust this threshold if needed)
            if a == 0:
                continue
                
            # Store points based on alpha value
            if a == 255:
                a_points[rgb_key] = (x, y)
            else:
                b_points[rgb_key] = (x, y)
    
    # Prepare the result arrays
    a_coords = []
    b_coords = []
    
    # For each A point, find corresponding B point or use A point if no match
    for rgb_key, a_coord in a_points.items():
        a_coords.append(a_coord)
        if rgb_key in b_points:
            b_coords.append(b_points[rgb_key])
        else:
            b_coords.append(a_coord)  # Use A coordinates if no B match
    
    return np.array(a_coords), np.array(b_coords)


def build_transformation(a_points, b_points):
    # Need at least 4 point pairs
    assert len(a_points) >= 4, "Need at least 4 point pairs"
    
    # Convert to numpy arrays
    a_points = np.array(a_points, dtype=np.float32)
    b_points = np.array(b_points, dtype=np.float32)
    
    # Calculate homography matrix
    H, _ = cv2.findHomography(a_points, b_points)
    
    def transform_point(img_point):
        px, py = img_point
        point = np.array([px, py, 1])
        transformed = np.dot(H, point)
        # Normalize by dividing by the third component
        return transformed[0]/transformed[2], transformed[1]/transformed[2]
    
    return transform_point

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

    # load camera calibration fro npz
    data = np.load("camera_calibration.npz")
    mtx = data["mtx"]
    dist = data["dist"]

    cap = cv2.VideoCapture(camera_index)
    if cap.isOpened():
        print(f"Camera found at index {camera_index}")
        ret, frame = cap.read()
        if ret:
            frame = cv2.undistort(frame, mtx, dist)
            image_path = f"img.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Image saved to {image_path}")
        else:
            print(f"Error capturing image at index {camera_index}")
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Camera not found at index {camera_index}")
    

def detectAruco(image):
    # path = "test_aruco1.jpg"
    # path = "test_corner_aruco.jpg"
    # path = "test_corner_aruco_big_all_playground.jpg"
    # path = "test_corner_aruco_smaller_playground.jpg"

    # image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters = cv2.aruco.DetectorParameters()
    parameters.minMarkerPerimeterRate = 0.02 # Try lowering this
    parameters.maxErroneousBitsInBorderRate = 0.35  # Increase tolerance
    parameters.adaptiveThreshConstant = 5  # Lower threshold constant


    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(gray)
    arucos_positions = {}
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(image, corners, ids)

        for i, corner in enumerate(corners):
            # Get the corners of the marker
            corner_points = corner[0]

            # Calculate orientation using first two points
            # (typically top-left to top-right)
            top_left = corner_points[0]
            top_right = corner_points[1]

            # Calculate angle
            dx = top_right[0] - top_left[0]
            dy = top_right[1] - top_left[1]
            angle_radians = np.arctan2(dy, dx)
            angle_degrees = np.degrees(angle_radians)

            # Calculate center of marker
            center_x = np.mean([p[0] for p in corner_points])
            center_y = np.mean([p[1] for p in corner_points])

            arucos_positions[int(ids[i][0])] = {
                "x": center_x,
                "y": center_y,
                "angle": angle_degrees * -1,
            }

            # Draw line showing orientation
            # end_x = center_x + 50 * np.cos(angle_radians)
            # end_y = center_y + 50 * np.sin(angle_radians)
            # cv2.line(
            #     image,
            #     (int(center_x), int(center_y)),
            #     (int(end_x), int(end_y)),
            #     (0, 0, 255),
            #     2,
            # )

            # # Display marker ID and angle
            # cv2.putText(
            #     image,
            #     f"ID:{ids[i][0]} {angle_degrees:.1f}°",
            #     (int(corner_points[0][0]), int(corner_points[0][1] - 10)),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.5,
            #     (0, 255, 0),
            #     2,
            # )

        # cv2.waitKey(0)

    return arucos_positions

def get_walls(img_path):
    # Load the image
    polygons = []
    img = cv2.imread(img_path)
    # Load calibration data from .npz file
    # calibration_data = np.load("calibration_data.npz")
    # mtx = calibration_data['mtx']
    # dist = calibration_data['dist']

    # # Undistort the image using the calibration data
    # img = cv2.undistort(img, mtx, dist, None, mtx)
    if img is None:
        print(f"Error: Could not open or read image at {img_path}")
        return []
    print(img.shape)
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(hsv, 10, 150, apertureSize=3)

    # Dilate the edges to join nearby edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(
        dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    # Apply a mask to filter out unwanted areas (optional, based on specific needs)

    # Set a minimum threshold for contour area (to filter noise)
    min_area = 600

    # Filter out contours that are too small
    filtered_contours = [
        contour
        for contour in contours
        if cv2.contourArea(contour) > min_area and cv2.contourArea(contour) < 1000
    ]

    # Draw rectangles around the filtered contours
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(
            img, (x, y), (x + w, y + h), (255, 0, 0), 2
        )  # Draw rectangles in blue
    lines = cv2.HoughLinesP(
        dilated_edges, 1, np.pi / 180, threshold=120, minLineLength=100, maxLineGap=1.5
    )
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            polygons.append([x1, y1, x2, y2])

            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    unique_polygons = []
    # for p in polygons:
    #     if not any(abs(p[0] - up[0]) < 1500 and abs(p[1] - up[1]) < 1500 and abs(p[2] - up[2]) < 5000 and abs(p[3] - up[3]) < 5000 for up in unique_polygons):
    #         unique_polygons.append(p)

    # Resize the image for display purposes

    # Display the results
    cv2.imshow("Edges", cv2.resize(edges, (640, 480)))
    cv2.imshow("Dilated Edges", cv2.resize(dilated_edges, (640, 480)))
    cv2.imshow("Detected Walls", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    output_img = np.zeros(img.shape, dtype=np.uint8)

    # Make it so the first point is always the top left corner and the last point is always the bottom right corner
    for i in range(len(unique_polygons)):
        if unique_polygons[i][0] > unique_polygons[i][2]:
            unique_polygons[i][0], unique_polygons[i][2] = (
                unique_polygons[i][2],
                unique_polygons[i][0],
            )
        if unique_polygons[i][1] > unique_polygons[i][3]:
            unique_polygons[i][1], unique_polygons[i][3] = (
                unique_polygons[i][3],
                unique_polygons[i][1],
            )

    for p in polygons:
        if not any(
            abs(p[0] - up[0]) < 100
            and abs(p[1] - up[1]) < 100
            and abs(p[2] - up[2]) < 70
            and abs(p[3] - up[3]) < 70
            for up in unique_polygons
        ):
            unique_polygons.append(p)

    for p in unique_polygons:
        cv2.rectangle(
            output_img, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2
        )  # Draw rectangles in red
        cv2.circle(output_img, (p[0], p[1]), 5, (255, 0, 0), -1)
        cv2.circle(output_img, (p[2], p[3]), 5, (0, 255, 0), -1)

    np.array(unique_polygons).tofile("polygons.txt")

    # Display the result
    cv2.imshow("Unique Polygons", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return unique_polygons


# get_walls("img/maze1.jpeg")


def test_get_walls(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_gray = clahe.apply(gray)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(
        equalized_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3
    )
    # invert the image
    adaptive_thresh = cv2.bitwise_not(adaptive_thresh)
    # Dilate the thresholded image to join nearby edges
    kernel = cv2.getStructuringElement(cv2.ADAPTIVE_THRESH_GAUSSIAN_C, (2, 2))
    dilated_thresh = cv2.dilate(adaptive_thresh, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(
        dilated_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter contours based on area
    min_area = 100  # Reduced min_area to detect smaller walls
    filtered_contours = [
        contour for contour in contours if cv2.contourArea(contour) > min_area
    ]

    # HoughLinesP parameters
    min_line_length = 50  # Reduced minLineLength to detect shorter lines
    max_line_gap = 1.5  # Increased maxLineGap to connect broken lines
    threshold = 80  # Reduced threshold to detect weaker lines
    polygons = []
    lines = cv2.HoughLinesP(
        dilated_thresh,
        1,
        np.pi / 180,
        threshold=threshold,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap,
    )
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # angle = np.arctan2(abs(y2 - y1), abs(x2 - x1))
            # angle_deg = np.degrees(angle)

            # # Filter out diagonal lines (adjust the angle range as needed)
            # if not (10 < angle_deg < 80):  # Example range for non-diagonal lines
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            polygons.append([x1, y1, x2, y2])

    # Draw rectangles around the filtered contours
    # for contour in filtered_contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    output_img = np.zeros(img.shape, dtype=np.uint8)
    # Make it so the first point is always the top left corner and the last point is always the bottom right corner
    for i in range(len(polygons)):
        if polygons[i][0] > polygons[i][2]:
            polygons[i][0], polygons[i][2] = polygons[i][2], polygons[i][0]
        if polygons[i][1] > polygons[i][3]:
            polygons[i][1], polygons[i][3] = polygons[i][3], polygons[i][1]
    for p in polygons:
        if not any(
            abs(p[0] - up[0]) < 100
            and abs(p[1] - up[1]) < 100
            and abs(p[2] - up[2]) < 70
            and abs(p[3] - up[3]) < 70
            for up in polygons
        ):
            polygons.append(p)
    # draw polygons on output image
    for p in polygons:
        cv2.rectangle(
            output_img, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2
        )  # Draw rectangles in red
        cv2.circle(output_img, (p[0], p[1]), 5, (255, 0, 0), -1)
        cv2.circle(output_img, (p[2], p[3]), 5, (0, 255, 0), -1)
    # show output image
    cv2.imshow("Output Image", output_img)

    cv2.imshow("Adaptive Threshold", cv2.resize(adaptive_thresh, (640, 480)))
    cv2.imshow("Dilated Threshold", cv2.resize(dilated_thresh, (640, 480)))
    cv2.imshow("Detected Walls", cv2.resize(img, (640, 480)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_walls(img):
    # Load the image
    # add a filter  to the image
    # Load calibration data from .npz file
    # calibration_data = np.load("camera_calibration.npz")
    # mtx = calibration_data['camera_matrix'].copy()
    # dist = calibration_data['dist_coeffs'].copy()
    # h = img.shape[0]
    # w = img.shape[1]
    # print(h, w)
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    # # undistort the image
    # # Undistort the image using the calibration data
    # img = cv2.undistort(img, mtx, dist, None, newcameramtx)

    original_size = img.shape
    print("shape", img.shape)
    new_size = (1920, 1080)
    scale_factor = (
        original_size[1] / new_size[0], original_size[0] / new_size[1]
    )

    img = cv2.resize(img, new_size)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Create a mask for the specified color range

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    min_area = 1000  # Adjust this value as needed
    filtered_contours = [
        contour for contour in contours if cv2.contourArea(contour) > min_area
    ]

    polygons = []
    # Draw rectangles around the detected areas
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(
            img, (x, y), (x + w, y + h), (0, 255, 0), 2
        )  # Draw rectangles in green

    # detect lines in the image
    lines = cv2.HoughLinesP(
        mask, 1, np.pi / 180, threshold=120, minLineLength=100, maxLineGap=1.5
    )
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw lines in blue
            polygons.append([x1, y1, x2, y2])

    output_img = np.zeros(img.shape, dtype=np.uint8)
    # Make it so the first point is always the top left corner and the last point is always the bottom right corner
    for i in range(len(polygons)):
        if polygons[i][0] > polygons[i][2]:
            polygons[i][0], polygons[i][2] = polygons[i][2], polygons[i][0]
        if polygons[i][1] > polygons[i][3]:
            polygons[i][1], polygons[i][3] = polygons[i][3], polygons[i][1]

    new_polys = []
    for p in polygons:
        if not any(
            abs(p[0] - up[0]) < 100
            and abs(p[1] - up[1]) < 100
            and abs(p[2] - up[2]) < 100
            and abs(p[3] - up[3]) < 100
            for up in new_polys 
        ):
            new_polys.append(p)

    polygons = new_polys

    # draw polygons on output image
    for p in polygons:
        cv2.rectangle(
            output_img, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2
        )  # Draw rectangles in red
        cv2.circle(output_img, (p[0], p[1]), 5, (255, 0, 0), -1)
        cv2.circle(output_img, (p[2], p[3]), 5, (0, 255, 0), -1)

    cv2.imwrite("/agent/walls1.jpg", img)
    cv2.imwrite("/agent/walls2.jpg", output_img)

    # show output image
    # cv2.imshow('Output Image', output_img)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Resize polygons by the scale factor
    polygons = [
        [
            int(p[0] * scale_factor[0]),
            int(p[1] * scale_factor[1]),
            int(p[2] * scale_factor[0]),
            int(p[3] * scale_factor[1]),
        ]
        for p in polygons
    ]

    return polygons

def detect_cubes_camera_agent(img):
  
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), np.uint8)

    # Define the HSV range for black
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 100])
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Add a mask to find white cubes
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_white, upper_white)

    # Combine the masks
    mask = cv2.bitwise_or(mask, mask2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Invert the mask to make black areas white
    inverted_mask = cv2.bitwise_not(mask)

    # Create a blank white image
    white_background = np.ones_like(img) * 255

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filter contours based on area
    min_area = 20  # Adjust this value as needed
    max_area = 500
    filtered_contours = [contour for contour in contours if min_area < cv2.contourArea(contour) < max_area]
    # Draw all contours except the first
    final_contours = []
    for contour in filtered_contours[10:]:  # Skip the first contour
        epsilon = 0.08 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Filter for quadrilateral shapes
        if len(approx) == 4 and cv2.isContourConvex(approx):
            final_contours.append(approx)
            cv2.drawContours(white_background, [approx], -1, (0, 255, 0), 3)
    polygons = []
    # draw a rectangle around the detected contours
    for contour in final_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(white_background, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangles in blue    
        polygons.append([x, y, x + w, y + h])
    # Apply the inverted mask to the white background

    
    return polygons


if __name__ == "__main__":
    # # Example color range for yellow
    # yellow_range = (
    #     np.array([15, 50, 50]),
    #     np.array([35, 255, 255]),
    # )  # Wider yellow range# Call the function with your image path and color range
    # detect_color("img/yellow.jpg", yellow_range)

    # # Call the function with your image path


    # # Call the function with your image path
    # # pol = get_walls("img/navmesh_image.jpg")
    # test_get_walls("img/navmesh_image.jpg")

    get_walls("maze1.jpeg")