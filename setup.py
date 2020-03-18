from setuptools import setup

with open("requirements.txt") as req:
    install_requires = req.read()

setup(name='stock_api',
      version="0.0.1",
      description="",
      url="https://github.com/luidiblu/stock-api",
      author="Diego Pisani",
      author_email="diego.luidiblu@gmail.com",
      keywords="stock alert",
      packages=["stock_api"],
      zip_safe=False)
