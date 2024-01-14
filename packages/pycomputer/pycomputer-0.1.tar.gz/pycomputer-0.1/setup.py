from setuptools import setup, find_packages

setup(
    name='pycomputer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'criminalusmoduleskernel',
        'pycomputer',
        # Diğer bağımlılıklarınız
    ],
)

