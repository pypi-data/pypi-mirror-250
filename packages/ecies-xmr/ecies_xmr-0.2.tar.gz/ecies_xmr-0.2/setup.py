from setuptools import setup, find_packages

setup(
    name='ecies_xmr',
    version='0.2',
    packages=find_packages(),
    description='ECIES implementation for the Monero Edwards25519 curve',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexander Klein',
    author_email='alexanderjamesklein@gmail.com',
    url='https://github.com/mewmix/ecies-xmr',
    install_requires=[
        'pycryptodome',  # Add other dependencies as needed
    ],
    python_requires='>=3.6',
)
