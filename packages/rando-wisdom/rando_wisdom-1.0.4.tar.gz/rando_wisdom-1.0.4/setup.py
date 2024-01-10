from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rando_wisdom",
    version="1.0.4",
    author="Imranqsl212",
    author_email="zakirovimran333@gmail.com",
    description="Rando-wisdom is a versatile Python library designed to inject a dose of variety and entertainment into your projects. This all-in-one library offers functionalities to generate random content, ensuring a delightful and engaging experience for users.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Imranqsl212/rando_wisdom",
    packages=find_packages(),
    install_requires=["requests"],
    package_data={"rando_wisdom": ["resource/*", "resource/*/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    include_package_data=True,
    keywords=[
        "Quotes Generator",
        "User Profile Generator",
        "Random Jokes",
        "Python Content Library",
        "Test Data Generator",
        "User Simulation Tools",
        "Python Content Library",
        "Advice Generator"
    ],
)
