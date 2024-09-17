from setuptools import setup, find_packages

setup(
    name='streamline',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
    author='Shu-Ha-Ri',
    description='Custom Web Framework',
    url='https://'
)