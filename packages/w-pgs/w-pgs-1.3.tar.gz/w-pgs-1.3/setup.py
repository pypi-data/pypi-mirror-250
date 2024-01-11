from setuptools import setup, find_packages

setup(
    name="w-pgs",
    version="1.3",
    packages=find_packages(),
    install_requires=[
        "datetime",
    ],
    author="zzt",
    author_email="zzt@qq.com",
    description="A useless database connection based on psycopg2",
    license="MIT",
    keywords="wpgs",
    url="https://github.com/zzt/w-rst.git"
)
