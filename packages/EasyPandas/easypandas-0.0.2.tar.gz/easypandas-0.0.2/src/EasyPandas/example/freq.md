导入模块
```python
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../freq.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
>>> toothgrowth = read("../data/toothgrowth.txt", textfileparamsdict={"sep": "\t"})
```

测试DataFrame对象
```python
>>> res = freq(toothgrowth)
>>> print(res)
```

测试DataFrame对象，频率统计
```python
>>> res = freq(toothgrowth, normalize=1)
>>> print(res)
```

测试DataFrame对象，不排序
```python
>>> res = freq(toothgrowth, sort=0)
>>> print(res)
```

测试DataFrame对象，升序排列
```python
>>> res = freq(toothgrowth, ascending=1)
>>> print(res)
```

测试DataFrame对象，指定列
```python
>>> res = freq(toothgrowth, subset="supp")
>>> print(res)
```

测试Series对象
```python
>>> res = freq(iris["Species"])
>>> print(res)
```

测试Series对象，频率统计
```python
>>> res = freq(iris["Sepal.Length"], normalize=1)
>>> print(res)
```

测试Series对象，不排序
```python
>>> res = freq(iris["Sepal.Length"], sort=0)
>>> print(res)
```

测试Series对象，升序排列
```python
>>> res = freq(iris["Sepal.Length"], ascending=1)
>>> print(res)
```

测试Series对象，等距分组为5组
```python
>>> res = freq(iris["Sepal.Length"], ascending=1, bins=5)
>>> print(res)
```
