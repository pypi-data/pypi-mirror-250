# from PIL import Image

# class ImageProcessor:
#     def __init__(self, image_path=None):
#         if image_path:
#             self.load_image(image_path)

#     def load_image(self, image_path):
#         """
#         Load an image from the specified path.
        
#         Parameters:
#         - image_path (str): Path to the image file.
#         """
#         try:
#             self.image = Image.open(image_path)
#             return self.image.getdata()
#         except Exception as e:
#             raise ValueError(f"Error loading image: {str(e)}")
        

#     def resize(self, width=None, height=None):
#         """
#         Resize the image.

#         Args:
#             width (int): The new width of the image.
#             height (int): The new height of the image.
#         """
#         if not hasattr(self, 'image'):
#             raise ValueError("Please load an image before performing operations.")
#         self.image = self.image.resize((width, height))
#         return self.image
        

#     def to_grayscale(self):
#         """Convert the image to grayscale."""
#         if not hasattr(self, 'image'):
#             raise ValueError("Please load an image before performing operations.")

#         self.image = self.image.convert('L')
#         return self.image

#     def crop(self, left, top, right, bottom):
#         """
#         Crop the image.

#         Args:
#             left (int): The left edge of the crop box.
#             top (int): The upper edge of the crop box.
#             right (int): The right edge of the crop box.
#             bottom (int): The lower edge of the crop box.
#         """
#         if not hasattr(self, 'image'):
#             raise ValueError("Please load an image before performing operations.")

#         self.image = self.image.crop((left, top, right, bottom))
#         return self.image

#     def save(self, output_path):
#         """
#         Save the processed image to a file.

#         Args:
#             output_path (str): The path to save the processed image.
#         """
#         if not hasattr(self, 'image'):
#             raise ValueError("Please load an image before performing operations.")

#         try:
#             self.image.save(output_path)
#         except Exception as e:
#             raise ValueError(f"Error saving image: {str(e)}")




from PIL import Image

class ndUtils:
    @staticmethod
    def load_image(file_path):
        """
        Load an image from the specified file path.

        Parameters:
        - file_path (str): Path to the image file.

        Returns:
        - Image object: Loaded image.
        """
        return Image.open(file_path)

    @staticmethod
    def resize_image(image, size):
        """
        Resize the input image to the specified size.

        Parameters:
        - image (Image object): Input image.
        - size (tuple): Target size (width, height).

        Returns:
        - Image object: Resized image.
        """
        return image.resize(size)

    @staticmethod
    def convert_to_grayscale(image):
        """
        Convert the input image to grayscale.

        Parameters:
        - image (Image object): Input image.

        Returns:
        - Image object: Grayscale image.
        """
        return image.convert("L")

    @staticmethod
    def crop_image(image, box):
        """
        Crop the input image using the specified bounding box.

        Parameters:
        - image (Image object): Input image.
        - box (tuple): Bounding box coordinates (left, upper, right, lower).

        Returns:
        - Image object: Cropped image.
        """
        return image.crop(box)

