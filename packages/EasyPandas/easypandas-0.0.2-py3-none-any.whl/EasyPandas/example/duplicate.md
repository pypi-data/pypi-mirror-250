导入模块
```python
>>> with open("../duplicate.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
```

Series标记重复值
```python
>>> res = duplicate(iris["Sepal.Length"])
>>> print(res)
```

Series标记重复值，keep=last
```python
>>> res = duplicate(iris["Sepal.Length"], keep="last")
>>> print(res)
```

Series标记重复值，keep=False
```python
>>> res = duplicate(iris["Sepal.Length"], keep=False)
>>> print(res)
```

DataFrame标记重复值
```python
>>> res = duplicate(iris)
>>> print(res)
```

DataFrame标记重复值，指定变量
```python
>>> res = duplicate(iris, subset="Species")
>>> print(res)
```

Series删除重复值
```python
>>> res = duplicate(iris["Sepal.Length"], action="drop")
>>> print(res)
```

DataFrame删除重复值
```python
>>> res = duplicate(iris, action="drop", subset="Species")
>>> print(res)
```
