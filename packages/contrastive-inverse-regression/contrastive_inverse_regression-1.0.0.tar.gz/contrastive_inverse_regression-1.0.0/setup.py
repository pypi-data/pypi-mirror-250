from setuptools import setup, find_packages

setup(
    name='contrastive_inverse_regression',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.3',
        'pandas>=2.1.4',
        'scipy>=1.9.3'
    ],
)
