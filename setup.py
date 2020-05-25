import setuptools

with open("README.org", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monad",
    version="0.0.1",
    author="Adam Berger",
    author_email="bergerab@icloud.com",
    description="Several monad implementations",
    long_description=long_description,
    long_description_content_type="text/org",
    url="https://github.com/bergerab/monads-py",
    packages=setuptools.find_packages(),
    python_requires='>=3.6')
