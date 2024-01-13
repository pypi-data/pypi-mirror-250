import array
import math
from typing import List, Tuple
from PIL import Image
import io
import urllib.request

class ImageLoader:
   def open_image_from_url(self, image_url):
    try:
      with urllib.request.urlopen(image_url) as response:
          img = Image.open(io.BytesIO(response.read()))
      return img
    except Exception as e:
      print(f"Error opening image from URL: {e}")
      return None

class ImageProcessor:
    def __init__(self):
        pass

    def resize_image(self, img, new_width, new_height):
        try:
            resized_img = img.resize((new_width, new_height))
            return resized_img
        except Exception as e:
            print(f"Error resizing image: {e}")
            return None
            
def rotate_image(self, width, height, pixels, angle):
        angle_rad = math.radians(angle)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        center_x = width // 2
        center_y = height // 2

        rotated_pixels = array.array("B")

        for y in range(height):
            for x in range(width):
                new_x = x - center_x
                new_y = y - center_y
                
                rotated_x = round(new_x * cos_theta - new_y * sin_theta)
                rotated_y = round(new_x * sin_theta + new_y * cos_theta)

                original_x = rotated_x + center_x
                original_y = rotated_y + center_y

                if 0 <= original_x < width and 0 <= original_y < height:
                    pixel_index = (original_y * width + original_x) * 3
                    rotated_pixels.extend(pixels[pixel_index:pixel_index + 3])
                else:
                    rotated_pixels.extend([255, 255, 255])

        return width, height, rotated_pixels

class ImageSaver:
  def save_image(self, img, filename):
    try:
      img.save(filename)
      print(f"Image saved as {filename}")
    except Exception as e:
      print(f"Error saving image: {e}")