import numpy as np


def calc_color_entropy(image: np.ndarray) -> float:
    """_summary_
    Calculate image color entropy
    entropy: the amount of information within pixel value 
    Args:
        image (np.ndarray): image array
    Returns:
        float: entropy value
    """
    _, counts = np.unique(image, return_counts=True)  # unique: occured pixel value(0~255), counts: count of appearance
    pixel_num = np.prod(image.shape)
    probabilities = counts / pixel_num  # array of appearance probability about each pixel value
    entropy = -np.sum(probabilities * np.log2(probabilities))  # Shannon entropy formula (maximum=8)
    return entropy
