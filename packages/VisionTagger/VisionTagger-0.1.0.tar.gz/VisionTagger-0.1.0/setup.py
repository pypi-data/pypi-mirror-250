from setuptools import setup, find_packages

setup(
    name="VisionTagger",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "VisionTagger": ["*.png"],
    },
    install_requires=[
        "pillow",
        "opencv-python",
        "tk"
    ],
    entry_points={
        'console_scripts': [
            'visiontagger=vision_tagger.main:main',
        ],
    },
)
