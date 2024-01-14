导入模块
```python
>>> import numpy as np
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../sort.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.csv")
```

对DataFrame按照index排序
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris, by="index")
>>> print(sortdf)
```

对DataFrame按照index排序，降序
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris, by="index", isincreasing=0)
>>> print(sortdf)
```

对DataFrame按照index排序，重新设置index
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris, by="index", isincreasing=0, isreindex=1)
>>> print(sortdf)
```

对DataFrame按照index排序，重新设置index，在原数据上修改
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris, by="index", isincreasing=0, isreindex=1, isinplace=1)
>>> print(sortdf)
>>> print(iris)
```

对DataFrame按照colname排序
```python
>>> sortdf = sort(iris, by="Sepal.Length")
>>> print(sortdf)
```

对DataFrame按照colname排序，降序
```python
>>> sortdf = sort(iris, by="Sepal.Length", isincreasing=0)
>>> print(sortdf)
```

对DataFrame按照colname排序，重新设置index
```python
>>> sortdf = sort(iris, by="Sepal.Length", isincreasing=0, isreindex=1)
>>> print(sortdf)
```

对DataFrame按照colname排序，重新设置index，在原数据上修改
```python
>>> sortdf = sort(iris, by="Sepal.Length", isincreasing=0, isreindex=1, isinplace=1)
>>> print(sortdf)
>>> print(iris)
```

对DataFrame按照多个colname排序
```python
>>> sortdf = sort(iris, by=["Sepal.Width", "Sepal.Length"])
>>> print(sortdf)
```

对DataFrame按照多个colname排序，一个升序，一个降序
```python
>>> sortdf = sort(iris, by=["Sepal.Width", "Sepal.Length"], isincreasing=[1,0])
>>> print(sortdf)
```

对DataFrame按照多个colname排序，一个升序，一个降序，一个升序，一个降序
```python
>>> sortdf = sort(iris, by=["Sepal.Width", "Sepal.Length", "Petal.Length", "Petal.Width"], isincreasing=[1,0,1,0])
>>> print(sortdf)
```

对Series按照index排序
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris["Sepal.Length"], by="index")
>>> print(sortdf)
```

对Series按照index排序，降序
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris["Sepal.Length"], by="index", isincreasing=0)
>>> print(sortdf)
```

对Series按照index排序，降序，重新设置index
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris["Sepal.Length"], by="index", isincreasing=0, isreindex=1)
>>> print(sortdf)
```

对Series按照index排序，降序，重新设置index，在原数据上修改
```python
>>> idx = iris.index.tolist()
>>> np.random.shuffle(idx)
>>> iris.index = idx
>>> sortdf = sort(iris["Sepal.Length"], by="index", isincreasing=0, isreindex=1, isinplace=1)
>>> print(sortdf)
>>> print(iris)
```

对Series按照value排序
```python
>>> sortdf = sort(iris["Sepal.Length"])
>>> print(sortdf)
```

对Series按照value排序，降序
```python
>>> sortdf = sort(iris["Sepal.Length"], isincreasing=0)
>>> print(sortdf)
```

对Series按照value排序，降序，重新设置索引
```python
>>> sortdf = sort(iris["Sepal.Length"], isincreasing=0, isreindex=1)
>>> print(sortdf)
```

对DataFrame的列名进行排序
```python
>>> sortdf = sort(iris, by="index", issortcol=1)
>>> print(sortdf)
```
