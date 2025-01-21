from setuptools import setup
setup(
    name = 'sutomax',
    version = '0.1.0',
    packages = ['sutomax'],
    entry_points = {
        'console_scripts': [
            'sutomax = sutomax.__main__:main'
        ]
    })