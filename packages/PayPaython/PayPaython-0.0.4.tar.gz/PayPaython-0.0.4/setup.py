from setuptools import setup, find_packages

setup(
    name='PayPaython',
    version='0.0.4',
    keywords = "paypay",
    author='taka4602',
    author_email='shun4602@gmail.com',
    url='https://github.com/taka-4602/PayPaython',
    description='A API wrapper for the PayPayAPI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)