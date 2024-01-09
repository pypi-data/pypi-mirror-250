"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: setup.py
@Time: 2023/12/9 18:00
"""

from setuptools import setup, find_packages

setup(
    name="SteamedBun",
    author="馒头",
    author_email="neihanshenshou@163.com",
    packages=find_packages(),
    version="0.1.0",
    description="馒头的第三方库",
    install_requires=[
        "allure-pytest==2.10.0",
        "colorama==0.4.6",
        "func_timeout==4.3.5",
        # "matplotlib==3.7.1",  version 0.08 版本废弃画图工具
        "openpyxl==2.6.4",
        "pandas==1.4.4",
        "Pillow==9.5.0",
        "python-dateutil==2.8.2",
        "pytest==7.1.2",
        "PyYAML==6.0",
        "requests==2.30.0",
        "selenium==4.4.3",
        "urllib3==1.26.12",
    ],
    license="MIT",
    platforms=["MacOS、Window"],
    fullname="馒头大人",
    url="https://github.com/neihanshenshou/SteamedBun.git"
)
