# tsjPython

View package at [Pypi](https://pypi.org/project/tsjPython), develop package on desktop win10 at Dormitory.

## use

```python
from tsjPython.tsjCommonFunc import *
passPrint(a)

from tsjPython import tsjCommonFunc
tsjCommonFunc.passPrint(OSACAError)
```

### Install

```python
pip install tsjPython
pip install --upgrade tsjPython
```

### Development

```bash
#执行此命令后，会生成上面图片中build的目录，目录层级是  build/lib/pip-test,  pip-test目录下就是你打包文件解压后的结果，可以在此查看打包的代码是否完整
python setup.py build  　　
# 执行此命令后，就会在dist目录下生成压缩包文件 .tar.gz
python setup.py sdist　　  
# 上传你刚刚打包好的压缩包
twine upload dist/XXXXX-0.1.0.tar.gz   
```

## reference

https://www.cnblogs.com/weisunblog/p/13307174.html
