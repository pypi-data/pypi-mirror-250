from setuptools import setup, find_packages
from pathlib import Path

directory = Path(__file__).parent

long_description = (directory / "README.md").read_text()
requirements = (directory / "requirements.txt").read_text()

setup(
    name='flesk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Kristian',
    author_email='krispetter+flesk@gmail.com',
    description='The simplest static site generator in the (python) world',
    url='https://github.com/kristus123/flesk',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)

