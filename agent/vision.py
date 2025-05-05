import torch
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoModelForDepthEstimation, AutoImageProcessor

# ===================== CONFIGURATION =====================
DEPTH_MODEL_NAME = "depth-anything/Depth-Anything-V2-Small-hf"

# ===================== MODEL INITIALIZATION =====================
processor = AutoImageProcessor.from_pretrained(DEPTH_MODEL_NAME)
depth_model = AutoModelForDepthEstimation.from_pretrained(DEPTH_MODEL_NAME)

# ===================== DEPTH ESTIMATION =====================
def estimate_depth_map(image, visualize=False, threshold=0.7):
    """
    Estimates depth and returns obstacle detection info by zone.

    Args:
        image (PIL.Image): RGB input image.
        visualize (bool): If True, displays the depth map.
        threshold (float): Depth threshold to classify obstacles.

    Returns:
        dict: Obstacle presence per zone {'left': bool, 'center': bool, 'right': bool}
    """
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = depth_model(**inputs)
        depth = outputs.predicted_depth

    # Resize to original image size
    depth_resized = torch.nn.functional.interpolate(
        depth.unsqueeze(1),
        size=image.size[::-1],
        mode="bicubic",
        align_corners=False,
    ).squeeze().cpu().numpy()

    # Normalize
    depth_normalized = (depth_resized - depth_resized.min()) / (depth_resized.max() - depth_resized.min())

    h, w = depth_normalized.shape
    left = depth_normalized[:, :w//3]
    center = depth_normalized[:, w//3:2*w//3]
    right = depth_normalized[:, 2*w//3:]

    mean_left = np.mean(left)
    mean_center = np.mean(center)
    mean_right = np.mean(right)

    if visualize:
        plt.imshow(depth_normalized, cmap="inferno")
        plt.title("Depth Map")
        plt.axis("off")
        plt.show()

    return {
        "left": mean_left > threshold,
        "center": mean_center > threshold,
        "right": mean_right > threshold
    }
