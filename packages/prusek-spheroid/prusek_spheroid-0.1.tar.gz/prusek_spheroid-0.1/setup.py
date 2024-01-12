from setuptools import setup

setup(
    name="prusek_spheroid",
    version="0.1",
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
        'matplotlib'
    ],
)
