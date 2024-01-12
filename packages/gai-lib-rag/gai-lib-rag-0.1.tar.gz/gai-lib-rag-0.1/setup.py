from setuptools import setup, find_packages
import os

def parse_requirements(filename):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)) as f:
        required = f.read().splitlines()
    return required

setup(
    name='gai-lib-rag',
    version="0.1",
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    packages=find_packages(exclude=["tests*","gai.rag.api"]),
    description = """Gai/Rag is the extension to the popular Gai/Gen Library for Retrieval Augmented Generation.""",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        "Development Status :: 3 - Alpha",        
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",        
        'Operating System :: OS Independent',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",        
        "Topic :: Scientific/Engineering :: Artificial Intelligence",        
    ],
    python_requires='>=3.10',        
    install_requires=[
        parse_requirements("requirements.txt")
    ],
)