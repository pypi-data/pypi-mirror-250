from setuptools import setup, find_packages

setup(
    name="fdk-flutter",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mycolorlogger==0.8"
        ],
    entry_points={
        'console_scripts': [
            'fdk = fdk.fdk:main',
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
