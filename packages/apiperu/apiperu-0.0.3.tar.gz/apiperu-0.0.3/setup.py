import setuptools

with open("./README.md", "r", encoding="utf-8") as description_file:
    description = description_file.read()

setuptools.setup(
    name="apiperu",
    version="0.0.3",
    description="API de los 24 departamentos del Perú",
    long_description=description,
    long_description_content_type='text/markdown',
    install_requires=['unidecode'],
    packages=setuptools.find_packages(),
    url='https://github.com/brianinhu/apiperu',
    include_package_data=True
)
