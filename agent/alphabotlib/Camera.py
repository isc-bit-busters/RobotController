import cv2
import asyncio
import base64
import aiofiles

async def get_picture_base64():
    print("Capturing image...")
    camera = cv2.VideoCapture(0)

    await asyncio.sleep(2)

    ret, frame = camera.read()

    if not ret:
        print("Failed to capture image.")
        return

    filename = "photo.jpg"
    cv2.imwrite(filename, frame)

    async with aiofiles.open(filename, "rb") as img_file:
        img_data = await img_file.read()
        encoded_img = base64.b64encode(img_data).decode("utf-8")

    return encoded_img
