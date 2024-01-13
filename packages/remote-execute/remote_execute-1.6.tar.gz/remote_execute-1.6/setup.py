from setuptools import setup, find_packages
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='remote_execute',
    version='1.6',
    description='Execute remote code fetched from a URL',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ZynoSoftware/remote-execute',
    author='WavaDev',
    packages=find_packages(),
    py_modules=['remote_execute'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'remote-execute = remote_execute.executor:main',
        ],
    },
)