导入模块
```python
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../cut.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
>>> sepal_length = iris["Sepal.Length"]
```

变量等距分组
```python
>>> res = cut(sepal_length, bins=5)
>>> print(res)
```

变量不等距分组
```python
>>> res = cut(sepal_length, bins=[4, 5.5, 6.5, 7, 8])
>>> print(res)
```

变量不等距分组，给定标签
```python
>>> res = cut(sepal_length, bins=[4, 6.5, 7.5, 8], labels=["低", "中", "高"])
>>> print(res)
```

变量不等距分组，给定标签，不包括右边
```python
>>> res = cut(sepal_length, bins=[4, 6.5, 7.5, 8], right=0)
>>> print(res)
```

变量不等距分组，给定标签，第一个区间包括左边端点
```python
>>> res = cut(sepal_length, bins=[4, 6.5, 7.5, 8], include_lowest=1)
>>> print(res)
```

变量分位数分组
```python
>>> res = cut(sepal_length, cutbyquantile=1, bins=[0, 0.1, 0.5, 0.9, 1])
>>> print(res)
```

变量分位数分组，指定标签
```python
>>> res = cut(sepal_length, cutbyquantile=1, bins=[0, 0.1, 0.5, 0.9, 1], labels=["低", "中低", "中高", "高"])
>>> print(res)
```
