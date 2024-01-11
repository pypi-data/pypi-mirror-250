from setuptools import setup, find_packages

setup(
    name='PayPaython',
    version='0.0.1',
    author='taka4602',
    author_email='shun4602@gmail.com',
    description='A API wrapper for the PayPayAPI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)