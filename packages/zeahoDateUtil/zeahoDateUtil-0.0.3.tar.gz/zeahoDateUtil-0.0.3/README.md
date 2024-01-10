# 安装上传工具
```bash
pip install twine
```
# 发布依赖包
#### 打包
```bash
python setup.py sdist
```

#### 上传
```bash
twine upload dist/*
```
#### username
```bash
__token__
```
#### api token
```bash
pypi-AgEIcHlwaS5vcmcCJDY2ZTg0ZmEwLWJhYzktNDAwYy04ZmE4LTAxMWZlZDRlYmI5NwACKlszLCIxOWE5YjM1MS0zYjU0LTRmZTctYjliNi0zOGVjNmIwMDczOGIiXQAABiAfH5Wdpr-k8dPYWqm8XKCH2EhmvgY00I5Dcy6RWqYVSQ
```

# 安装依赖
```bash
pip install zeahoDateUtil
```

# 使用依赖
```bash
from zeahoDateUtil import parse_datetime
```