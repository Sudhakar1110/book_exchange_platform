from setuptools import setup, find_packages


with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")


from book_exchange import __version__ as version


setup(
    name="book_exchange",
    version=version,
    description="A simple book exchange and donation platform",
    author="Your Company",
    author_email="info@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
