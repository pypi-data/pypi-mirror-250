from setuptools import setup, find_packages

setup(
    name='DDMongoLogger',
    version='0.1.1',
    author='Alex Pavlov',
    author_email='apavlov@datadimensions.com',
    packages=find_packages(),
    install_requires=[
        'pymongo',
    ],
    license='MIT',
    description='simple mongoDb logger',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
)
