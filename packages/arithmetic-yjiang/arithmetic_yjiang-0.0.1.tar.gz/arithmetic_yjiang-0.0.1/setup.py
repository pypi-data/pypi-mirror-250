from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='arithmetic_yjiang',
    version='0.0.1',
    author='yjiang',
    author_email='1900812907@qq.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitee.com/Eason596/py-package-release-test',
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.3"
    ],
    python_requires='>=3.8',

    # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    # data_files=[
    #     ('', ['conf/*.conf']),
    #     ('/usr/lib/systemd/system/', ['bin/*.service']),
    #            ],

    # 希望被打包的文件
    # package_data={
    #     '':['*.txt'],
    #     'bandwidth_reporter':['*.txt']
    #            },

    # 不打包某些文件
    # exclude_package_data={
    #     'bandwidth_reporter':['*.txt']
    #            }

    # install_requires 在安装模块时会自动安装依赖包
    # 而 extras_require 不会，这里仅表示该模块会依赖这些包
    # 但是这些包通常不会使用到，只有当你深度使用模块时，才会用到，这里需要你手动安装
    # extras_require={
    #     'PDF':  ["ReportLab>=1.2", "RXP"],
    #     'reST': ["docutils>=0.3"],
    # }

)