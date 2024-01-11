from setuptools import setup, find_packages
# import datetime


# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
# date = datetime.datetime.now()
# aa = f'{date.year}.{date.month}.{date.day}.{date.hour}'
setup(
    name='mintools',        # 模块名称，注意不要与其他模块重名
    version='1.0.5',  # 版本号
    # version=f'{date.year}.{date.month}.{date.day}.{date.hour}',
    # description='A small example package',  # 简短介绍
    # long_description=long_description,      # 长介绍
    # long_description_content_type="text/markdown",  # 长介绍格式
    # author='qianbo',
    # author_email='ptest@qq.com',
    # url='www.github.com',          # 项目主页
    packages=find_packages(), # 需要处理的包目录(通常为包含 init.py 的文件夹)，可以用find_packages自动查找
    platforms='any',                            # 支持平台
    # license='MIT',                              # 证书
    # classifiers=[                               # 更多的元数据
    #     "Programming Language :: Python :: 3",  # python 版本
    #     "License :: OSI Approved :: MIT License",   # 证书
    #     "Operating System :: OS Independent",   # 不依赖操作系统
    # ],
    # package_dir={"": "src"},# 代码目录
    # python_requires='>=3.6'
)
