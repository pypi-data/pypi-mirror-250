from setuptools import setup, find_packages

setup(
    name='schedule-sdk',
    version='3.0.5',
    packages=find_packages(),
    install_requires=[
        "requests",
        "redis"
    ],
)