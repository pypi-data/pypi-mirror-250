from setuptools import setup, find_packages

setup(
    name='doods',
    version='1.1',
    packages=find_packages(),
    install_requires=[
    'requests',
    'PySocks'],
    description="read docs in https://github.com/Kaii-Devv/ds2play",
    author='Tamsis X Code',
    author_email='ceeskamu@gmail.com',
    entry_points={
        'console_scripts': [
            'module = ds2play.ds:main',
        ],
    },
)
