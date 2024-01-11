from setuptools import setup, find_packages

setup(
    name='redwing-vector',  # Replace with your package's name
    version='0.1.2',  # Your package's version
    author='Hello Redwing',  # Company Nickname
    author_email='hello@redwing.ai',  # Your email
    description='Python client to interface with Redwing Vector gRPC Service.',  # Short description
    long_description=open('README.md').read(),  # Long description read from the the readme file
    long_description_content_type='text/markdown',  # Type of the long description
    url='https://github.com/redwing-os/client/tree/master/python',  # Link to your package's repository
    packages=find_packages(),  # Automatically find your package's subpackages
    install_requires=[
        # List your project's dependencies here
        # e.g., 'requests>=2.25.1',
    ],
    classifiers=[
        # Choose classifiers from https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
)