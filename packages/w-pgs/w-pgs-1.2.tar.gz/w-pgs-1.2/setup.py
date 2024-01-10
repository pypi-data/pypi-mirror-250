from setuptools import setup, find_packages

setup(
    name="w-pgs",
    version="1.2",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    author="zzt",
    author_email="zzt@qq.com",
    description="A useless database connection tool based on psycopg2",
    license="MIT",
    keywords="wpgs",
    url="https://github.com/zzt/w-pgs.git"
)
