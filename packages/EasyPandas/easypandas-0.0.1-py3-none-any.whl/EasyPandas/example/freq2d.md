导入模块
```python
>>> with open("../freq2d.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> df = read("../data/toothgrowth.txt", textfileparamsdict={"sep": "\t"})
```

基本测试
```python
>>> print(df)
>>> res = freq2d(df, "supp", "dose")
>>> print(res)
```

基本测试，给定行列名
```python
>>> print(df)
>>> res = freq2d(df, "supp", "dose", rownames="A", colnames="B")
>>> print(res)
```

基本测试，不显示边际
```python
>>> print(df)
>>> res = freq2d(df, "supp", "dose", rownames="A", colnames="B", margins=0)
>>> print(res)
```

基本测试，修改边际名称
```python
>>> print(df)
>>> res = freq2d(df, "supp", "dose", rownames="A", colnames="B", margins_name="边际频数")
>>> print(res)
```

基本测试，修改边际名称，显示频率
```python
>>> print(df)
>>> res = freq2d(df, "supp", "dose", rownames="A", colnames="B", margins_name="边际频数", normalize=1)
>>> print(res)
```
