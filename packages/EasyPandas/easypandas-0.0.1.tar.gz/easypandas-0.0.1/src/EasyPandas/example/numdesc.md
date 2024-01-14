导入模块
```python
>>> with open("../numdesc.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
```

DataFrame的测试
```python
>>> res = numdesc(iris.iloc[:, 1:-1], isprint=1)
```

Series的测试
```python
>>> res = numdesc(iris["Petal.Length"], isprint=1)
```
