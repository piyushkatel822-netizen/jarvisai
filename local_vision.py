from PIL import Image
import os

def analyze_image(image_path):
    try:
        img = Image.open(image_path)

        width, height = img.size
        image_format = img.format or "Unknown"
        mode = img.mode

        size_kb = os.path.getsize(image_path) / 1024

        if width > height:
            orientation = "Landscape"
        elif height > width:
            orientation = "Portrait"
        else:
            orientation = "Square"

        return (
            "JARVIS Local Vision Report:\n\n"
            f"Image format: {image_format}\n"
            f"Image size: {width} x {height} pixels\n"
            f"Orientation: {orientation}\n"
            f"Color mode: {mode}\n"
            f"File size: {size_kb:.1f} KB\n\n"
            "Image Google Gemini ko nahi bheji gayi. "
            "Ye information JARVIS ne locally process ki hai."
        )

    except Exception as e:
        return "JARVIS Local Vision Error: " + str(e)
