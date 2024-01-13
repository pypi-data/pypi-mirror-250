from skimage import transform

def redimensionar_imagem(imagem, proporção):
    """
    Resizes an image according to a specified proportion.

    Parameters:
        imagem (numpy.ndarray): The input image to be resized.
        proporção (float): The proportion by which to resize the image. Must be between 0 and 1.

    Returns:
        numpy.ndarray: The resized image.

    Raises:
        AssertionError: If the proportion is not between 0 and 1.
    """
    assert  0 <= proporção <=1, " Proporção invalida, tente um valor entre 0 e 1"
    altura  =  imagem.shape[0]*proporção
    largura =  imagem.shape[1]*proporção
    nova_imagem = transform.resize(imagem, (altura,largura))
    return nova_imagem  