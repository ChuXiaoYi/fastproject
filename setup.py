# -*- coding: utf-8 -*-
# ---------------------------------------------
#       @Time    : 2020/8/4 11:33 上午
#       @Author  : cxy =.=
#       @File    : setup.py
#       @Software: PyCharm
#       @Desc    :
# ---------------------------------------------
from setuptools import setup, find_packages

GFICLEE_VERSION = '2020.8.4.1'

setup(
    name='cfastproject',
    version=GFICLEE_VERSION,
    packages=find_packages(),
    entry_points={
        "console_scripts": ['cfastproject = fastproject.main:main']
    },
    install_requires=[],
    url='https://github.com/ChuXiaoYi/fastproject',
    license='GNU General Public License v3.0',
    author='Xiaoyi Chu',
    author_email='895706056@qq.com',
    description='More convenient to create fastapi project'
)
