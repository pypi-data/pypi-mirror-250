from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='EFCrud',
    version='1.0.4.1',
    description='API client for EFCrud',
    author='Devi Prakash',
    author_email='dprakash@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dprakash2101/EFCrudPython.git',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
