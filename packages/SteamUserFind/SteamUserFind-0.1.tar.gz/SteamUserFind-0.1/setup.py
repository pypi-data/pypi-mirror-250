from setuptools import setup, find_packages

setup(
    name='SteamUserFind',
    version='0.1',
    packages=find_packages(),
    description='A simple web crawler for steamcommunity.com',
    url='https://github.com/LordPoc/SteamUserFinder_API',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)