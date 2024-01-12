import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='dftools-snowflake',
    packages=setuptools.find_namespace_packages(include=['dftools']),
    version='0.1.1',
    description='DF-Tools Snowflake',
    author='Data Flooder',
    author_email="lirav.duvshani@dataflooder.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache',
    install_requires=[
        'snowflake-connector-python'
        , 'dftools-core>=0.1.1'
    ],
    python_requires=">=3.7.9",
)