from setuptools import setup, find_packages

setup(
    name='streamline-cwf',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
    author='Shu-Ha-Ri',
    description='Custom Web Framework',
    url='https://github.com/Triston-TL/streamline'
)