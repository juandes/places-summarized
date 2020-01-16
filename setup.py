import os
import setuptools

base_packages = ["googlemaps>=3.1.4"]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="places-summarized",
    version="0.1.0",
    author="Juan De Dios Santos",
    author_email="author@example.com",
    description="Summarizing the Google Maps attributes of places within a specified area",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/juandes/places-summarized",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    install_requires=base_packages,
    include_package_data=True
)
