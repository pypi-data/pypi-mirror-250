from setuptools import setup, find_packages

setup(
    name='ecies_xmr',
    version='0.1',
    packages=find_packages(),
    description='ECIES implementation for the Monero Edwards25519 curve',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexander Klein',
    author_email='alexanderjamesklein@gmail.com',
    url='https://github.com/mewmix/monero_ecies',
    install_requires=[
        'pycryptodome',  # Add other dependencies as needed
    ],
    python_requires='>=3.6',
)
