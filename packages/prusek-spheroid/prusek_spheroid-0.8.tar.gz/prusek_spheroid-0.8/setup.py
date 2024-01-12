from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="prusek_spheroid",
    version="0.8",
    description="Your package description",
    author="Michal Prusek",
    author_email="prusemic@cvut.cz",
    url="https://github.com/michalprusek/Spheroid-segmentation",
    packages=["prusek_spheroid"],
    install_requires=[
        'numpy',
        'opencv-python',
        'scikit-image',
        'scikit-learn',
        'shapely',
        'threadpoolctl',
        'matplotlib',
        'rasterio'
    ],
)
