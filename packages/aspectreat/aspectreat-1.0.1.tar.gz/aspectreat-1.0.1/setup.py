# -*- coding = utf-8 -*-
from setuptools import setup, find_packages, find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    my_long_description = f.read()
# my_long_description = "desp"
install_requires = [
    "passlib >= 1.7.4",
    "pathspec >= 0.12.1",
    "pefile >= 2023.2.7",
    "pillow >= 10.1.0",
    "face_recognition == 1.3.0",
    "rsa == 4.9",
    "scipy == 1.11.4",
    "setuptools >= 68.0.0",
    "six >= 1.16.0",
]
setup(
    # 关于classifiers的描述详见如下
    # https://pypi.org/search/?q=&o=&c=Topic+%3A%3A+Software+Development+%3A%3A+Build+Tools
    classifiers=[
        # 属于什么类型
        "Topic :: Software Development :: Libraries :: Python Modules",
        # 发展时期,常见的如下
        # Development Status:: 1 - Planning
        # Development Status:: 2 - Pre - Alpha
        # Development Status:: 3 - Alpha
        # Development Status:: 4 - Beta
        # Development Status:: 5 - Production / Stable
        # Development Status:: 6 - Mature
        # Development Status:: 7 - Inactive
        "Development Status :: 4 - Beta",
        # 许可证信息
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        # 目标编程语言
        # Programming Language :: C
        # Programming Language :: C++
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        # 自然语言
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],

    # 如果上传时出现ERROR：The user '' isn't allowed to upload to project ''，换个名字，长一点无所谓，不能跟别人重复
    name="aspectreat",
    version="1.0.1",
    author="lylake",
    # author_email="736946693@qq.com",
    description="This is a project template.",
    long_description=my_long_description,

    # 存放源码的地址，填入gitee的源码网址即可
    # url="https://gitee.com/UnderTurrets/",
    install_requires=install_requires,
    include_package_data=True,
    # packages=["aspectreat"],
    # packages=find_packages("aspectreat"),
    packages=find_packages(exclude=["aspectreat_pcs"]),
    # exclude_package_data={
    #     'aspectreat_pcs': ['/'],  # 排除my_package下的unwanted_folder
    # },
    # README.md文本的格式，如果希望使用markdown语言就需要下面这句话
    long_description_content_type="text/markdown",


)
