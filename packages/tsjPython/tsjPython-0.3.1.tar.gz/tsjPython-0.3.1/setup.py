from setuptools import setup, find_packages

setup(
    name='tsjPython',  # 打包后的包文件名
    version='0.3.1',  # 版本号
    keywords=("tsj"),    # 关键字
    description='personal code for tsj',  # 说明
    long_description="none",  # 详细说明
    license="MIT Licence",  # 许可
    url='https://github.com/Kirrito-k423/tsjPython',
    author='Shaojie Tan',
    author_email='shaojiemike@mail.ustc.edu.cn',
    # packages=find_packages(),     #这个参数是导入目录下的所有__init__.py包
    include_package_data=True,
    platforms="any",
    install_requires=['termcolor',
                      'plotille', 'regex',
                      'openpyxl',
                      'numpy',
                      'plotly',
                      'matplotlib',
                      "tqdm",
                      ],    # 引用到的第三方库
    # py_modules=['pip-test.DoRequest', 'pip-test.GetParams', 'pip-test.ServiceRequest',
    #             'pip-test.ts.constants', 'pip-test.ac.Agent2C',
    #             'pip-test.ts.ttypes', 'pip-test.ac.constants',
    #             'pip-test.__init__'],  # 你要打包的文件，这里用下面这个参数代替
    packages=['tsjPython']  # 这个参数是导入目录下的所有__init__.py包
)
