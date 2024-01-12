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

class ImageSaver:
  def save_image(self, img, filename):
    try:
      img.save(filename)
      print(f"Image saved as {filename}")
    except Exception as e:
      print(f"Error saving image: {e}")