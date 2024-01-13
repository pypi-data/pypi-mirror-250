from setuptools import setup, find_packages

setup(
    name='schedule-sdk',
    version='3.0.7',
    packages=find_packages(),
    install_requires=[
        "requests",
        "redis"
    ],
)