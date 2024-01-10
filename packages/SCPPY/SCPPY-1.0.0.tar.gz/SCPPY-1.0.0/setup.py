from setuptools import setup, find_packages

setup(
    name='SCPPY',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    author='FlipFlapsRU',
    description='Symbolic huylo',
    long_description="",
    long_description_content_type='text/markdown',
    url='https://link-to-your-repository',
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
