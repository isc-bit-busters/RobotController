def adjust_time_ema(measured_distance, target_distance, previous_time,
                    alpha=0.7, max_factor=1.5, min_factor=0.5):
    """
    Adjusts the movement time using EMA (Exponential Moving Average),
    based on previous actual movement and target distance.

    :param measured_distance: Distance actually traveled by the robot
    :param target_distance: Desired distance to travel in the next move
    :param previous_time: The time that was used in the last movement
    :param alpha: Smoothing factor for EMA (0 < alpha <= 1). Closer to 1 = more reactive.
    :param max_factor: Maximum allowed multiplier of time change (e.g. 1.5 means max +50%)
    :param min_factor: Minimum allowed multiplier of time change (e.g. 0.5 means min -50%)
    :return: Adjusted time for the next movement
    """

    # Prevent division by zero
    if previous_time == 0:
        return previous_time

    # Estimate current speed (distance per second)
    estimated_speed = measured_distance / previous_time

    # If robot didn’t move (possibly stuck), keep same time
    if estimated_speed == 0:
        return previous_time

    # Estimate the ideal time to travel the target distance at the current speed
    raw_time = target_distance / estimated_speed

    # Apply EMA to smooth the transition
    filtered_time = alpha * raw_time + (1 - alpha) * previous_time

    # Clamp the change in time to avoid sudden large jumps, especially if the robot is stuck
    min_time = previous_time * min_factor
    max_time = previous_time * max_factor
    filtered_time = max(min(filtered_time, max_time), min_time)

    return filtered_time


next_time = adjust_time_ema(
    measured_distance=30.0,
    target_distance=35.0,
    previous_time=2.0,
    alpha=0.6,
    max_factor=1.4,
    min_factor=0.7
)

print(f"Next movement time: {next_time:.2f} seconds")