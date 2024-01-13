import matplotlib.pyplot as plt

def plot_img(imagem, title="", tamanho=(12,4), mostra_eixos='off' ):
    """
        Plot de uma unica imagem com um tiulo e tamanho definido

        Args:
            imagem: The image to be plotted.
            title: Optional title for the plot (default is an empty string).
            tamanho: Optional tuple specifying the size of the plot (default is (12,4)).
            mostra_eixos: Optional parameter specifying whether to show the axes of the plot (default is 'off').

        Returns:
            imagem
    """
    plt.figure(figsize=tamanho)
    plt.title(title)
    plt.imshow(imagem)
    plt.axis(mostra_eixos)
    plt.show()
    
    
def plot_resultados(*args):
    """
        Plot de varias imagem com um tiulo e tamanho definido.
        
        Parameters:
            *args: Variable number of images to be plotted.

        Returns:
            None
    """
    numero_img = len(args)
    fig, eixo = plt.subplots(nrows=1, ncols=numero_img,figsize=(12,4))
    nome_lista = ['Imagem {}'.format(i+1) for i in range(numero_img)]
    nome_lista.append('Resultado')
    
    for ax,nome,imagem in zip(eixo,nome_lista,args):
        ax.set_title(nome)
        ax.imshow(imagem,cmap='gray')
        ax.axis('off') 
    
    fig.tight_layout()
    plt.show()   
    
def plot_hist(imagem):
    fig,axis = plt.subplots(nrows=1 , ncols=3, figsize=(12,4), sharex=True, sharey=True)
    
    col_lista = ['gray', 'red', 'green']
    for index, (ax, col) in enumerate(zip(axis, col_lista)): 
        ax.set_title('{} histograma'.format(col.title()))
        ax.hist(imagem[:,:,index].ravel(), bins=256, color=col, alpha=0.8)
    fig.tight_layout()
    plt.show()
