导入模块
```python
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../index.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
>>> sepal_length = iris["Sepal.Length"]
```

测试Series参数
```python
>>> res = index(sepal_length, index=[i**2 for i in range(150)])
>>> print(res)
```

测试Series参数，修改原始数据
```python
>>> res = index(sepal_length, index=[i**2 for i in range(150)], indexgdata=1)
>>> print(res)
```

测试Series参数，将index转为一列
```python
>>> res = index(sepal_length)
>>> print(res)
```

测试DataFrame参数，修改行名
```python
>>> res = index(iris, index=[i**2 for i in range(150)])
>>> print(res)
```

测试DataFrame参数，原数据修改
```python
>>> res = index(iris, index=[i**2 for i in range(150)], indexgdata=1)
>>> print(res)
```

测试DataFrame参数，修改列名
```python
>>> res = index(iris, columns=iris.columns.tolist()[:-1] + ["A"])
>>> print(res)
```

测试DataFrame参数，修改列名，原数据修改
```python
>>> res = index(iris, columns=iris.columns.tolist()[:-1] + ["A"], columngdata=1)
>>> print(res)
```

测试DataFrame参数，修改列名和列名
```python
>>> res = index(iris, columns=iris.columns.tolist()[:-1] + ["A"], index=[i**2 for i in range(150)])
>>> print(res)
```

测试DataFrame参数，修改列名和列名，原数据修改
```python
>>> res = index(iris, columns=iris.columns.tolist()[:-1] + ["A"], index=[i**2 for i in range(150)], indexgdata=1, columngdata=1)
>>> print(res)
```

测试DataFrame参数，将某列作为行名
```python
>>> res = index(iris, index="Sepal.Length")
>>> print(res)
```

测试DataFrame参数，将某列作为行名，从原数据中删除那一列
```python
>>> res = index(iris, index="Sepal.Length", drop=1)
>>> print(res)
```

测试DataFrame参数，将index转为列数据
```python
>>> res = index(iris, reset=1)
>>> print(res)
```
