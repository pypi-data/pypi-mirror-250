from skimage.io import imread, imsave

def Ler_img(caminho,e_cinza=False):
    """
        Ler uma imagem em um caminho especificado.

        Parameters:
            caminho (str): The path to the image file.
            e_cinza (bool, optional): Whether to read the image in grayscale. Defaults to False.

        Returns:
            ndarray: The image read from the file.
    """
    imagem = imread(caminho,as_grey=e_cinza)
    return imagem

def Gravar_img(caminho,imagem):
    """
        Salvar a imagem em um caminho especificado.

        Parameters:
            imagem (ndarray): The image to be saved.
            caminho (str): The path to save the image to.

        Returns:
            None
    """
    imsave(caminho,imagem)