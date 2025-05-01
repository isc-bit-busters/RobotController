from transformers import pipeline
from PIL import Image

pipe = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")
image = Image.open('image.jpeg')
depth = pipe(image)["depth"]

# Save the depth map
depth.save("depth_map.png")
