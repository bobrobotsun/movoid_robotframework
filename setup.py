from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='movoid_robotframework',
    version='1.4.17',
    packages=find_packages(),
    url='',
    license='',
    author='movoid',
    author_email='bobrobotsun@163.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['robotframework>=6.0,<8',
                      'movoid_function'
                      ],
)
