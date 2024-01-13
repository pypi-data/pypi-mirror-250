from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()
with open("requirements.txt", "r") as f:
    requerimentos = f.read().splitlines()


setup(
    name    = "processamento_de_img",
    version = "0.1.1",
    author  = "Nick: Oibug/Nome:Gubio Gomes De Lima",
    author_email    = 'gubiojogo@gmail.com',
    description     = " pacote simples para Processamento de imagem em Python",
    long_description    = long_description,
    long_description_content_type   = "text/markdown",
    packages    = find_packages(),
    url =    "https://github.com/GubioGL/BootCampDIO",
    install_requires = requerimentos,
    python_requires = '>=3.10',  
    )