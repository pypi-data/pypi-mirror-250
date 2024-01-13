import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colloquy",
    version="0.1.0",
    author="Your Name",
    author_email="benwhalley@gmail.com",
    description="A package to faciliate conversations with LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benwhalley/conversation",
    project_urls={
        "Bug Tracker": "https://github.com/benwhalley/conversation/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "colloquy"},
    packages=setuptools.find_packages(where="colloquy"),
    python_requires=">=3.9",
)
