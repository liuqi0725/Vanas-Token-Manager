# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : setup.py.py
# @Created  : 2020/10/25 2:22 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 打包文件
# -------------------------------------------------------------------------------

from setuptools import setup,find_packages

# Readme
with open('README.rst') as f:
    LONG_DESC = f.read()

setup(name='VanasTokenDealer',                  # 包名
      version='1.0.0',                          # 项目版本号，符合 PEP 440 定义
      url='https://github.com/liuqi0725/vanas-token-manager',  # 项目 URL，可以是代码库或者项目主页
      description="This is a token manager microservice for alexliu Vanas Project.",     # 描述项目的一句话
      long_description=LONG_DESC,               # 一个 reStucturedText 格式的文档
      author='liu.qi',                          # 作者
      author_email='liuqi_0725@aliyun.com',     # 作者邮箱
      license='MIT',                            # 项目使用的许可信息 （MIT Apache2 GPL 等）
      classifiers=[                             # 从固定列表中选取的分类器列表，需要符合 PEP 301 定义
          'Development Status :: 3 - Alpha ',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      keywords=['flask','microservice','vanas','token'],    # 描述项目标签
      packages=find_packages(),                 # 项目包含的包列表，通过 setuptools 的 find_packages() 方法自动获取
      include_package_data=True,                # 一个标识，简化了包含的非 python 文件
      zip_safe=False,                           # 一个标识，他阻止 setuptools 将项目安装为 ZIP 文件，是旧标准（可执行的 eggs）
      # setuptools 勾子列表，如添加控制台脚本
      entry_points="""                          
      [console_scripts]
      tokenmanager = service.app:main
      """,
      # 依赖项列表（一个 setuptools 参数）
      # 与 requirements.txt 冲突，在社区中推荐后者
      # 一般来说：
      # 1. python 库 使用 install_requires 来添加依赖
      # 2. python 应用 使用 requirements.txt 来添加依赖
      #
      # 推荐使用 install_requires 填写然后用 pip-tools 生成依赖，自动同步 2 个地方
      # install_requires 使用未锁定版本的库名称，    requirements.txt则是当前项目锁定能运行正常的对应版本（锁定版本）
      # CLI(命令行)  `pip install pip-tools` 安装 pip-tools，然后使用  CLI pip-compile 生成 requirements.txt
      install_requires=['Flask','PyYAML','Werkzeug','PyJWT']
      )