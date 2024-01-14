导入模块
```python
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
```

基本用法
```python
>>> df = read("../data/iris.csv")
>>> print(df.head())
```

读取其他分隔符
```python
>>> df = read("../data/iris.csv", textfileparamsdict={"sep": ","})
>>> print(df.head())
```

不指定任何行作为列名
```python
>>> df = read("../data/iris.csv", textfileparamsdict={"header": None})
>>> print(df.head())
```

指定列名
```python
>>> df = read("../data/iris.csv", textfileparamsdict={"names": ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]})
>>> print(df.head())
```

指定索引
```python
>>> df = read("../data/iris.csv", textfileparamsdict={"index_col": 1})
>>> print(df.head())
```

指定读取的列名
```python
>>> df = read("../data/iris.csv", textfileparamsdict={"usecols": ["Sepal.Length", "Sepal.Width", "Species"]})
>>> print(df.head())
```

指定读取的文件行数
```python
>>> df = read("../data/iris.csv", textfileparamsdict={"names": ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"], "nrows": 3})
>>> print(df.head())
```

将第一列作为行名
```python
>>> df = read("../data/iris.xlsx", excelfileparamsdict={"index_col": 0})
>>> print(df.head())
```

不将第一列作为行名
```python
>>> df = read("../data/iris.xlsx")
>>> print(df.head())
```

不将第一行作为列名
```python
>>> df = read("../data/iris.xlsx", excelfileparamsdict={"header": None})
>>> print(df.head())
```

将第一列作为行名且指定列名
```python
>>> df = read("../data/iris.xlsx", excelfileparamsdict={"index_col": 0, "names": ["v1", "v2", "v3", "v4", "v5"]})
>>> print(df.head())
```

指定要读取的列
```python
>>> df = read("../data/iris.xlsx", excelfileparamsdict={"usecols": ["Sepal.Length", "Sepal.Width", "Species"], "index_col": 0})
>>> print(df.head())
```

指定读取的行数
```python
>>> df = read("../data/iris.xlsx", excelfileparamsdict={"usecols": ["Sepal.Length", "Sepal.Width", "Species"], "nrows": 50})
>>> print(df.head())
```

读取xls文件
```python
>>> df = read("../data/womenexport.xls")
>>> print(df.head())
```

测试pkl参数
```python
>>> df = read("../data/iris.pkl")
>>> print(df.head())
```

测试dta参数
```python
>>> df = read("../data/auto.dta")
>>> print(df.head())
```

测试xpt参数
```python
>>> df = read("../data/hh.xpt")
>>> print(df.head())
```

测试sav参数
```python
>>> df = read("../data/iris.sav")
>>> print(df.head())
```