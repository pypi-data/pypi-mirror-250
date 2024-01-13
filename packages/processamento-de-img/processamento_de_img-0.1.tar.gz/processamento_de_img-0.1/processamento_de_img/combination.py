import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity
from skimage.exposure import match_histograms


def img_gray(img):
    """
    Convert an image to grayscale.

    Args:
        img (ndarray): The input image array.

    Returns:
        ndarray: The grayscale image array.
    """
    # Convert the image array to grayscale
    gray_array = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    # Convert the array to uint8 data type
    gray_array = gray_array.astype(np.uint8)
    
    return gray_array


def Encontrando_diferença(img1,img2):
    """
    Calculates the difference between two images and returns the 
    normalized difference between two images.

    Parameters:
        img1 (numpy.ndarray): The first image.
        img2 (numpy.ndarray): The second image.

    Returns:
        numpy.ndarray: The normalized difference between the two images.
    """
    # primeiro comparar se os tamanhos sao iguais
    assert img1.shape == img2.shape , "as imagens devem ter o mesmo tamanho"
    # convertenso para a escala de siza
    img1 = img_gray(img1)
    img2 = img_gray(img2)
    
    score, diff = structural_similarity(img1,img2 ,full=True)
    print("A similaridade entre as imagens e: ", score)
    
    diff_normalizado  = (diff - np.min(diff)) / ( np.max(diff) - np.min(diff) )
    return diff_normalizado

def Mix_imagens(img1,img2,number=-1):
    """
    Generate a function comment for the given function body.

    :param img1: The first image to be mixed.
    :param img2: The second image to be mixed.
    :param number: The channel axis used for matching histograms, defaults to -1.

    :return: The image resulting from mixing img1 and img2 with matched histograms.
    """
    match_img = match_histograms(img1,img2,channel_axis=number)
    return match_img