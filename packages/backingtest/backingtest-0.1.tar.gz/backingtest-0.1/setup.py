from setuptools import setup, find_packages

setup(
    name='backingtest',
    version='0.1',
    author='peedroca',
    author_email='phm1080@icloud.com',
    description='A lib to help you backing test your results and get some insights.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/peedroca/exchange_backingtest',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
