from setuptools import setup

setup(
    name='thinkst-zippy',
    version='0.1.2',
    packages=['zippy'],
    package_data={"": ["*.txt"]},
    entry_points={
        'console_scripts': [
            'zippy=zippy.zippy:main',
        ]
    },
    install_requires=[
        'numpy',
        'brotli'
    ]
)
