from setuptools import setup, find_packages

setup(
    name="zaide",
    version="1.6",
    packages=find_packages(),
    install_requires=["datetime", "time", "os", "json", "socket", "inspect"],
    author="zaide",
    author_email="zhstack@163.com",
    description="A useless model",
    license="MIT",
    keywords="rst",
    url="https://github.com/zhstack/zaide.git"
)
