from setuptools import setup, find_packages

setup(
    name='ezsn',
    version='0.2.0',
    author='Ezhilarasan',
    author_email='nec0914014@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'ezsn = ezsn.iot:iot',
        ],
    },
)
