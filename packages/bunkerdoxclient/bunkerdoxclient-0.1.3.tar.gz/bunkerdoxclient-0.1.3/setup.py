from setuptools import setup

setup(
    name='bunkerdoxclient',
    version='0.1.3',
    author='BunkerDox',
    author_email='bunkerdox@bunkerdox.com',
    description='Defines Python types and functions for the BunkerDox REST API.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    py_modules=['bunkerdoxclient'],
    install_requires=[
        'pydantic',
    ]
)
