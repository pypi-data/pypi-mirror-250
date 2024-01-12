from setuptools import setup

setup(
    name="prusek_spheroid_segmentation",
    version="0.2",
    description="Your package description",
    author="Michal Prusek",
    author_email="prusemic@cvut.cz",
    url="https://github.com/michalprusek/Spheroid-segmentation",
    packages=["prusek_spheroid_segmentation"],
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
