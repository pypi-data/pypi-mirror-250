from setuptools import setup, find_packages

setup(
    name='automated_machineLearning_methods',
    version='0.1.0',
    author='Sepehr Goodarzi',
    author_email='sepehrgoodarzi6@gmail.com',
    description='A small example package for machine learning operations',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'tensorflow',
        'matplotlib',
        'sklearn',
        'seaborn',
        'statsmodels',
        'scikit-learn',
        'numpy',
        'keras'
    ]
)