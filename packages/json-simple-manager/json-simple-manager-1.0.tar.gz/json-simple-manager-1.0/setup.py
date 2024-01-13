from setuptools import setup

with open("./README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(name='json-simple-manager',
    version='1.0',
    license='GPL 3.0',
    author='Alan Reis Anjos',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='alanreisanjo@gmail.com',
    keywords='JSON Simple Manager',
    description='Pequena biblioteca para validação e manipulação de JSONs',
    packages=['jsonSimpleManager'])