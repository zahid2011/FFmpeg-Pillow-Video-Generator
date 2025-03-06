from PIL import Image, ImageDraw, ImageFont
import os

# Input Image
image_path = "input.jpg" 

# Loading Image
image = Image.open(image_path)

# Applying Transformation (Grayscale)
gray_image = image.convert("L")
draw = ImageDraw.Draw(gray_image)

# Overlaying Text
overlay_text = "TESTING SAMPLE TEXT"
font = ImageFont.truetype("arial.ttf", 140) # Loading a Larger Font (Arial, 140px)

# Getting the Image Dimensions
image_width, image_height = gray_image.size

# Get Text Size using textbbox()
bbox = draw.textbbox((0, 0), overlay_text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Positioning the Text Lower 
text_x = (image_width - text_width) // 2
text_y = int(image_height * 0.85) 

# Drawing Text with black Shadow for Better Visibility
draw.text((text_x - 2, text_y - 2), overlay_text, font=font, fill=0)  # Shadow (Black)
draw.text((text_x, text_y), overlay_text, font=font, fill=255)  # Main Text (White)

# Generating Output Filename Dynamically
base_name, ext = os.path.splitext(image_path)  # Splits 'input.jpg' into ('input', '.jpg')
output_image_path = f"{base_name}_processed{ext}"  # Creates 'input_processed.jpg'

# Saving Updated Image
gray_image.save(output_image_path)

print(f"Image processing complete. Processed image saved as: {output_image_path}")
