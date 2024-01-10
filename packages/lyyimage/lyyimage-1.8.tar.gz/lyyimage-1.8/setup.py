from setuptools import setup

setup(
    name='lyyimage',
    version='1.8',
    author='lyy',
    author_email='',
    description='lyyimagetools for lyy',
    #packages=find_packages(),
    license="MIT",
    install_requires=[
        'numpy',
        'Pillow',
        'pdf2image',
        'io',
    ],
)
