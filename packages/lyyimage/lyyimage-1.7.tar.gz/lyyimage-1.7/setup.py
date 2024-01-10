from setuptools import setup

setup(
    name='lyyimage',
    version='1.7',
    author='lyy',
    author_email='',
    description='lyyimagetools for lyy',
    #packages=find_packages(),
    license="MIT",
    install_requires=[
        'numpy',
        'PIL',
        'pdf2image',
        'io',
    ],
)
