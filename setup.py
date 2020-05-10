import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='data_usage',
    version='1.0.0',
    author='Carles Pina i Estany',
    author_email='carles@pina.cat',
    description='Shows Pepephone used and available data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cpina/pepephone-data',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
    scripts=['bin/data_usage']
)
