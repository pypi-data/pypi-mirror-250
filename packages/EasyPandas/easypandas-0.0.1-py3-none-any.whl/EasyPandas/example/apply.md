导入模块
```python
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../apply.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
>>> sepal_length = iris["Sepal.Length"]
```

测试Series参数，applytowhat为obj，func为str=any
```python
>>> res = apply(sepal_length, "any")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=all
```python
>>> res = apply(sepal_length, "all")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=count
```python
>>> res = apply(sepal_length, "count")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=idxmax
```python
>>> res = apply(sepal_length, "idxmax")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=idxmin
```python
>>> res = apply(sepal_length, "idxmin")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=max
```python
>>> res = apply(sepal_length, "max")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=min
```python
>>> res = apply(sepal_length, "min")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=mean
```python
>>> res = apply(sepal_length, "mean")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=median
```python
>>> res = apply(sepal_length, "median")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=sum
```python
>>> res = apply(sepal_length, "sum")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=nunique
```python
>>> res = apply(sepal_length, "unique")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=prod
```python
>>> res = apply(sepal_length, "prod")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=quantile
```python
>>> res = apply(sepal_length, "quantile", q=0.9)
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=sem
```python
>>> res = apply(sepal_length, "sem")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=size
```python
>>> res = apply(sepal_length, "size")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=skew
```python
>>> res = apply(sepal_length, "skew")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=std
```python
>>> res = apply(sepal_length, "std")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=var
```python
>>> res = apply(sepal_length, "var")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=bfill
```python
>>> res = apply(sepal_length, "bfill")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=cumsum
```python
>>> res = apply(sepal_length, "cumsum")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=cumprod
```python
>>> res = apply(sepal_length, "cumprod")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=cummax
```python
>>> res = apply(sepal_length, "cummax")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=cummin
```python
>>> res = apply(sepal_length, "cummin")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=diff
```python
>>> res = apply(sepal_length, "diff")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=ffill
```python
>>> res = apply(sepal_length, "ffill")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=fillna
```python
>>> res = apply(sepal_length, "fillna", value=100)
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=rank
```python
>>> res = apply(sepal_length, "rank")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=shift
```python
>>> res = apply(sepal_length, "shift", periods=1)
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=head
```python
>>> res = apply(sepal_length, "head")
>>> print(res)
```

测试Series参数，applytowhat为obj，func为str=tail
```python
>>> res = apply(sepal_length, "tail")
>>> print(res)
```

测试Series参数，applytowhat为element，func为lambda x: str(x).split(".")[1]
```python
>>> res = apply(sepal_length, lambda x: str(x).split(".")[1], applytowhat="element")
>>> print(res)
```

测试DataFrame参数，func为str=any
```python
>>> res = apply(iris, "any")
>>> print(res)
```

测试DataFrame参数，func为str=all
```python
>>> res = apply(iris, "all")
>>> print(res)
```

测试DataFrame参数，func为str=count
```python
>>> res = apply(iris, "count")
>>> print(res)
```

测试DataFrame参数，func为str=idxmax
```python
>>> res = apply(iris, "idxmax")
>>> print(res)
```

测试DataFrame参数，func为str=idxmin
```python
>>> res = apply(iris, "idxmin")
>>> print(res)
```

测试DataFrame参数，func为str=max
```python
>>> res = apply(iris, "max")
>>> print(res)
```

测试DataFrame参数，func为str=min
```python
>>> res = apply(iris, "min")
>>> print(res)
```

测试DataFrame参数，func为str=mean
```python
>>> res = apply(iris.iloc[:,:-1], "mean")
>>> print(res)
```

测试DataFrame参数，func为str=median
```python
>>> res = apply(iris.iloc[:,:-1], "median")
>>> print(res)
```

测试DataFrame参数，func为str=sum
```python
>>> res = apply(iris.iloc[:,:-1], "sum")
>>> print(res)
```

测试DataFrame参数，func为str=prod
```python
>>> res = apply(iris.iloc[:,:-1], "prod")
>>> print(res)
```

测试DataFrame参数，func为str=quantile
```python
>>> res = apply(iris.iloc[:,:-1], "quantile", q=0.9)
>>> print(res)
```

测试DataFrame参数，func为str=sem
```python
>>> res = apply(iris.iloc[:,:-1], "sem")
>>> print(res)
```

测试DataFrame参数，func为str=size
```python
>>> res = apply(iris.iloc[:,:-1], "size")
>>> print(res)
```

测试DataFrame参数，func为str=skew
```python
>>> res = apply(iris.iloc[:,:-1], "skew")
>>> print(res)
```

测试DataFrame参数，func为str=std
```python
>>> res = apply(iris.iloc[:,:-1], "std")
>>> print(res)
```

测试DataFrame参数，func为str=var
```python
>>> res = apply(iris.iloc[:,:-1], "var")
>>> print(res)
```

测试DataFrame参数，func为str=bfill
```python
>>> res = apply(iris.iloc[:,:-1], "bfill")
>>> print(res)
```

测试DataFrame参数，func为str=cumsum
```python
>>> res = apply(iris.iloc[:,:-1], "cumsum")
>>> print(res)
```

测试DataFrame参数，func为str=cumprod
```python
>>> res = apply(iris.iloc[:,:-1], "cumprod")
>>> print(res)
```

测试DataFrame参数，func为str=cummax
```python
>>> res = apply(iris.iloc[:,:-1], "cummax")
>>> print(res)
```

测试DataFrame参数，func为str=cummin
```python
>>> res = apply(iris.iloc[:,:-1], "cummin", axis=1)
>>> print(res)
```

测试DataFrame参数，func为str=diff
```python
>>> res = apply(iris.iloc[:,:-1], "diff", axis=1)
>>> print(res)
```

测试DataFrame参数，func为str=ffill
```python
>>> res = apply(iris.iloc[:,:-1], "ffill")
>>> print(res)
```

测试DataFrame参数，func为str=fillna
```python
>>> res = apply(iris.iloc[:,:-1], "fillna", value=100)
>>> print(res)
```

测试DataFrame参数，func为str=rank
```python
>>> res = apply(iris.iloc[:,:-1], "rank")
>>> print(res)
```

测试DataFrame参数，func为str=shift
```python
>>> res = apply(iris.iloc[:,:-1], "shift", periods=1)
>>> print(res)
```

测试DataFrame参数，func为str=head
```python
>>> res = apply(iris.iloc[:,:-1], "head")
>>> print(res)
```

测试DataFrame参数，func为str=tail
```python
>>> res = apply(iris.iloc[:,:-1], "tail")
>>> print(res)
```

测试DataFrame参数，func为str=tail
```python
>>> res = apply(iris.iloc[:,:-1], "tail")
>>> print(res)
```

测试DataFrame参数，func为自定义函数
```python
>>> res = apply(iris.iloc[:,:-1], lambda x: x+1)
>>> print(res)
```

测试Series参数，func为列表，非聚合函数
```python
>>> res = apply(sepal_length, ["cumsum", lambda x: x+1])
>>> print(res)
```

测试Series参数，func为列表，聚合函数
```python
>>> res = apply(sepal_length, ["max", lambda x: x.max()-x.min()])
>>> print(res)
```

测试DataFrame参数，func为字典，非聚合函数
```python
>>> res = apply(iris.iloc[:, :-1], {"Sepal.Width": "cumsum", "Sepal.Length": lambda x: x+1})
>>> print(res)
```

测试DataFrame参数，func为字典，聚合函数
```python
>>> res = apply(iris.iloc[:, :-1], {"Sepal.Width": "sum", "Sepal.Length": lambda x: x.max()-x.min()})
>>> print(res)
```

测试DataFrame参数，func为列表，非聚合函数
```python
>>> res = apply(iris.iloc[:, :-1], ["cumsum", lambda x: x+1])
>>> print(res)
```

测试DataFrame参数，func为列表，聚合函数
```python
>>> res = apply(iris.iloc[:, :-1], ["sum", lambda x: x.max()-x.min()])
>>> print(res)
```
