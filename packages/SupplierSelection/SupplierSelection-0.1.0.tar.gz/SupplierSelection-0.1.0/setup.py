from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='SupplierSelection',
    version='0.1.0',
    description='Supplier Selection Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Md Bakhtiar Chowdhury',
    author_email='joyinfo.bd@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pyodbc==4.0.30',
        'sqlalchemy==1.4.3',
        'numpy==1.20.1',
        'cryptography==3.4.7',
        'pandas==1.2.2',
        'seaborn==0.11.1',
        'statsmodels==0.12.2',
        'matplotlib==3.3.4',
        'scikit-learn==0.24.1',
    ],
)
