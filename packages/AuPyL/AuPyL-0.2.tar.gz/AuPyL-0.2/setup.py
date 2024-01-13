import os, sys

long_description = open("/storage/emulated/0/python/autopy/README.md", "r", encoding="utf-8").read()

long_description_content_type = "text/markdown"

try:
    from setuptools import setup
except ModuleNotFoundError:
    os.system("pip install setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system("pip install wheel -i https://pypi.tuna.tsinghua.edu.cn/simple")
    sys.exit()
setup(
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    # 项目名称(包名)
    name="AuPyL",
    # 版本号
    version="0.2",
    # Python版本
    python_requires=">=3.9",
    # 包的概括描述
    description="AutoPy Lite For Termux",
    # 作者
    author="None",
    # 作者邮箱
    author_email="NoneAndNone@No.com",
    # 包名列表
    packages=["AuPyL"],
)


# cd …
# python setup.py bdist_wheel sdist
#twine upload /storage/emulated/0/python/autopy/dist/*