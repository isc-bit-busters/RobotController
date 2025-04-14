import math

def compute_distance_to_camera_axis(dist):
    """
    Compute the distance of the distance between.

    :param dist: Distance sensor reading
    :return: Computed distance to the robot
    """
    cam_len = 40
    cam_axis_offset = 10
    axis_height = 95

    try:
        value_under_sqrt = cam_axis_offset**2 + (dist + cam_len)**2 - axis_height**2
        if value_under_sqrt < 0:
            raise ValueError(f"Invalid geometry: sqrt of negative number ({value_under_sqrt})")
        return math.sqrt(value_under_sqrt)
    except ValueError as e:
        print(f"Error computing distance: {e}")
        return None

def convert_distance_to_robot_centre(dist, angle):
    offset = 42
    angle_radians = math.radians(angle)
    return math.sqrt(dist**2 + offset**2 + 2 * dist * offset * math.cos(angle_radians))


def compute_distance_to_robot(dist, angle):
    """
    Compute the distance from the camera reading to the robot's center in the ground plane.

    :param dist: Distance sensor reading
    :param angle: Angle of the robot in degrees
    """
    d = compute_distance_to_camera_axis(dist)

    print(f"Distance to camera axis: {d:.2f}")

    return convert_distance_to_robot_centre(d, angle)

# Example usage

if __name__ == "__main__":
    dist = 190
    angle = 0
    print(f"input distance: {dist}")
    print(f"input angle: {angle} degrees")

    distance_to_robot = compute_distance_to_robot(dist, angle)
    print(f"Distance to robot: {distance_to_robot:.2f}")


