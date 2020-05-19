import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kmeans", # Replace with your own username
    version="0.0.1",
    author="David Graves",
    author_email="dgravesdev@gmail.com",
    description="Baylor College of Medicine Scientific Programmer I Assignment",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davgra04/kmeans",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
    ],
)