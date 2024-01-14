from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Presenting additional features for Data Analysis.'
LONG_DESCRIPTION = 'New functionalities for Data Analysis, leveraging the capabilities of Numpy, Pandas, Matplotlib, and Seaborn libraries.'

# Setting up
setup(
    name="Plunge",
    version=VERSION,
    author="Gustavo Ortiz",
    author_email="<gstvortiz@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'seaborn', 'scikit-learn'],
    keywords=['python', 'data analysis', 'data visualization', 'data science'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)