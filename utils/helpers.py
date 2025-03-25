import io
import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def get_img_bits(image):
    """
    Converts PIL Image it to bits
    """
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    return bio.getvalue()


def plot_image(image, title=None):
    """
    Displays an image using matplotlib
    """
    plt.figure(figsize=(8,8))
    if title is not None:
        plt.title(title)
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    
def load_numpy(path, device):
    """
    Loads numpy array and converts it to torch tensor
    """
    data = np.load(path)
    data = torch.from_numpy(data).to(device)
    return data


def convert_image(image, size):
    """
    Converts a generated image to a displayable format suitable for visualization.
    
    Parameters:
    image (torch.Tensor): A generated image of shape [N, H, W] in range [-1, 1].
    size (tuple): The desired output size as a tuple (width, height).
    
    Returns:
    PIL.Image: A postprocessed image in shape [H, W, N] in range [0, 255] (dtype=uint8).
    """
    # Change the image shape from [N, H, W] to [H, W, N]
    image = image.permute(1, 2, 0)
    
    # Rescale the pixel values from [-1, 1] to [0, 255]
    image = (image + 1) * 127.5
    image = image.clamp(0, 255).to(torch.uint8).cpu().numpy()
    
    # Convert the NumPy array to a PIL Image
    image = Image.fromarray(image, 'RGB')
    
    # Resize the image to the specified size
    image = image.resize(size)
    
    return image
