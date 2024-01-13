from setuptools import setup, find_packages

setup(
    name='cairogen',
    version='0.1',
    description='cairo for genArt',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    license='CC-BY-NC-SA',
    keywords=['pycairo',
              'drawing'],
    packages=find_packages(),
    install_requires=["pycairo"],
    python_requires='>3.6'
)
