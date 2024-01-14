导入模块
```python
>>> import pandas as pd
>>> with open("../totime.py", "rt", encoding="utf8") as fp: exec(fp.read())
```

基本测试
```python
>>> timestr = "Jul 31, 2009"
>>> res = totime(timestr)
>>> print(res)
```

基本测试
```python
>>> timestr = "2005/11/23"
>>> res = totime(timestr)
>>> print(res)
```

基本测试
```python
>>> timestr = None
>>> res = totime(timestr)
>>> print(res)
```

基本测试
```python
>>> timestr = "04-14-2012 10:00"
>>> res = totime(timestr)
>>> print(res)
```

基本测试
```python
>>> timestr = "2018-01-01"
>>> res = totime(timestr)
>>> print(res)
```

基本测试，定制格式
```python
>>> timestr = "2018*01||01"
>>> res = totime(timestr, format="%Y*%m||%d")
>>> print(res)
```

基本测试，将数字转为时间
```python
>>> timestr = [2018, 2020, 10000]
>>> res = totime(timestr, unit="D")
>>> print(res)
```

基本测试，将数字转为时间，给定原始时间
```python
>>> timestr = [2018, 2020, 10000]
>>> res = totime(timestr, unit="D", origin="2000-01-01")
>>> print(res)
```
