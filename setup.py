__author__ = 'mkaplenko'
from setuptools import setup, find_packages

setup_args = dict(
    name='containers',
    version='0.1',
    author='mkaplenko',
    author_email='mkaplenko@gmail.com',
    url='',
    description='Containers document system',
    long_description=open('README').read(),
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=True
)

if __name__ == '__main__':
    setup(**setup_args)