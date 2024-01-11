import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
PACKAGE_NAME="cp_mex"
VERSION = '0.0.1' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
DESCRIPTION = 'Permite migrar los codigos postales de México' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'django'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True
)