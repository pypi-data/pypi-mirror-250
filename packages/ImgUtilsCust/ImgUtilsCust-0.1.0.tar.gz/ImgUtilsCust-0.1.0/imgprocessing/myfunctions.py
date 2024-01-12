
from PIL import Image, ImageOps
import os
import matplotlib.pyplot as plt
import seaborn as sns


class ImgUtilsCust:
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
    
    @staticmethod
    def rotate_image(image, angle):
        """
        Rotate the input image by the specified angle.

        Parameters:
        - image (Image object): Input image.
        - angle (float): Rotation angle in degrees.

        Returns:
        - Image object: Rotated image.
        """
        return image.rotate(angle)

    @staticmethod
    def invert_image(image):
        """
        Invert colors in the input image.

        Parameters:
        - image (Image object): Input image.

        Returns:
        - Image object: Inverted color image.
        """
        return ImageOps.invert(image)
    
    @staticmethod
    def analyze_image_dataset(dataset_path):
        """
        Perform basic analysis on an image dataset.

        Parameters:
        - dataset_path (str): Path to the image dataset directory.
        """
        total_images = 0
        unique_dimensions = set()
        file_types = set()
        unique_color_profiles = set()

        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_path = os.path.join(root, file)

                    with Image.open(image_path) as img:
                        dimensions = img.size
                        unique_dimensions.add(dimensions)

                       
                        file_type = img.format.lower()
                        file_types.add(file_type)

                
                        color_profile = img.mode
                        unique_color_profiles.add(color_profile)

                    total_images += 1

        print(f"Dataset: {dataset_path}")
        print(f"Total number of images: {total_images}")
        print(f"Number of unique dimensions: {len(unique_dimensions)}")
        print(f"Unique dimensions: {list(unique_dimensions)}")
        print(f"Number of unique file types: {len(file_types)}")
        print(f"Unique file types: {list(file_types)}")
        print(f"Number of unique color profiles: {len(unique_color_profiles)}")
        print(f"Unique color profiles: {list(unique_color_profiles)}")
        print()

    @staticmethod
    def analyze_and_visualize_images(dataset_path):
        """
        Analyze and visualize image sizes and aspect ratios in the specified dataset.

        Parameters:
        - dataset_path (str): Path to the image dataset directory.
        """
        
        width_list, height_list = [], []
        color_profiles = []
        file_types = []

        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(root, file)

                    with Image.open(file_path) as img:
                        width, height = img.size
                        width_list.append(width)
                        height_list.append(height)
                        
                        color_profile = img.mode
                        color_profiles.append(color_profile)

                        file_type = img.format.lower()
                        file_types.append(file_type)

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 16))

        sns.histplot(width_list, color='blue', ax=axes[0, 0], label='Width')
        sns.histplot(height_list,  color='orange', ax=axes[0, 0], label='Height')
        axes[0, 0].set_title('Distribution of Image Sizes')
        axes[0, 0].legend()

        aspect_ratios = [width / height for width, height in zip(width_list, height_list)]
        sns.histplot(aspect_ratios, color='green', ax=axes[0, 1])
        axes[0, 1].set_title('Distribution of Aspect Ratios')

        # Plot color profiles
        sns.barplot(x=list(set(color_profiles)), y=[color_profiles.count(profile) for profile in set(color_profiles)], color='purple', ax=axes[1, 0])
        axes[1, 0].set_title('Distribution of Color Profiles')

        # Plot file types
        sns.barplot(x=list(set(file_types)), y=[file_types.count(file_type) for file_type in set(file_types)], color='red', ax=axes[1, 1])
        axes[1, 1].set_title('Distribution of File Types')

        plt.tight_layout()
        plt.show()

