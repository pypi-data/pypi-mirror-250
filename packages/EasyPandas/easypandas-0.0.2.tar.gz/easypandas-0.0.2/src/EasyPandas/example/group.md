导入模块
```python
>>> import numpy as np
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../group.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx", excelfileparamsdict={"index_col": 0})
```

不给func，只分组
```python
>>> res = group(iris, by="Species")
>>> print(res)
```

不给func，只分组，给定组别名称
```python
>>> res = group(iris, by="Species", groupname="virginica")
>>> print(res)
```

单变量分组，给定单个func
```python
>>> res = group(iris, by="Species", func="sum")
>>> print(res)
```

单变量分组，给定多个func
```python
>>> res = group(iris, by="Species", func=["mean", "std"])
>>> print(res)
```

单变量分组，给定多个func，自定义函数
```python
>>> res = group(iris, by="Species", func=["mean", lambda x: x.max()-x.min()])
>>> print(res)
```

多变量分组，给定单个func
```python
>>> df = pd.DataFrame({"A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"], "B": ["one", "one", "two", "three", "two", "two", "one", "three"], "C": np.random.randn(8), "D": np.random.randn(8)})
>>> print(df)
>>> res = group(df, by=["A", "B"], func="mean")
>>> print(res)
```

多变量分组，给定多个func
```python
>>> df = pd.DataFrame({"A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"], "B": ["one", "one", "two", "three", "two", "two", "one", "three"], "C": np.random.randn(8), "D": np.random.randn(8)})
>>> print(df)
>>> res = group(df, by=["A", "B"], func=["mean", "sum", lambda x: x.min()/x.max()])
>>> print(res)
```

单变量分组，给定单个func，改名称
```python
>>> res = group(iris, by="Species", func=["sum"], renamedict={"sum": "求和"})
>>> print(res)
```

单变量分组，给定多个func，改名称
```python
>>> res = group(iris, by="Species", func=["sum", "mean"], renamedict={"sum": "求和", "mean": "平均值"})
>>> print(res)
```

多个变量分组，给定一个func，改名称
```python
>>> df = pd.DataFrame({"A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"], "B": ["one", "one", "two", "three", "two", "two", "one", "three"], "C": np.random.randn(8), "D": np.random.randn(8)})
>>> print(df)
>>> res = group(df, by=["A", "B"], func=["mean"], renamedict={"mean": "均值"})
>>> print(res)
```

多个变量分组，给定多个func，改名称
```python
>>> df = pd.DataFrame({"A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"], "B": ["one", "one", "two", "three", "two", "two", "one", "three"], "C": np.random.randn(8), "D": np.random.randn(8)})
>>> print(df)
>>> res = group(df, by=["A", "B"], func=["sum", "mean"], renamedict={"sum": "求和", "mean": "平均值"})
>>> print(res)
```

单变量分组，给定func，字典形式
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": "sum"})
>>> print(res)
```

单变量分组，给定func，字典形式，改名
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": "sum"}, renamedict={"sum": "求和"})
>>> print(res)
```

单变量分组，给定func，字典形式
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": ["sum", "mean"], "Sepal.Width": ["max", "var"]})
>>> print(res)
```

单变量分组，给定func，字典形式，改名
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": ["sum", "mean"], "Sepal.Width": ["mean", "var"]}, renamedict={"sum": "求和", "mean": ["Length均值", "Width均值"], "var": "方差"})
>>> print(res)
```

单变量分组，给定func，字典形式，改名
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": "mean", "Sepal.Width": "sum"}, renamedict={"mean": "均值", "sum": "求和"})
>>> print(res)
```

单变量分组，给定func，字典形式，改名
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": ["sum", "mean"], "Sepal.Width": "mean"}, renamedict={"sum": "求和", "mean": ["Length均值", "Width均值"]})
>>> print(res)
```

单变量分组，给定func，字典形式，改名
```python
>>> res = group(iris, by="Species", func={"Sepal.Length": "mean", "Sepal.Width": "mean"}, renamedict={"mean": ["Length均值", "Width均值"]})
>>> print(res)
```
