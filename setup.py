from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="py-speccy",
    version="1.0.0",
    author="Daniel Sendula",
    description="Python/Pygame implementation ZX Spectrum Emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natdan/py-speccy",
    zip_safe=False, # Doesn't create an egg - easier to debug and hack on
    packages=['pyros', 'pyroslib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygame',
    ],
    python_requires='>=3.9',
)
