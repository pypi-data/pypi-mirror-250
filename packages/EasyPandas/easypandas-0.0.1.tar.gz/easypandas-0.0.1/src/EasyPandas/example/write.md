导入模块
```python
>>> with open("../rdata.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../write.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> irisdf = rdata("../data/iris.csv")
```

测试csv参数
```python
>>> write(irisdf, "../data/wiris.csv")
```

写入行名
```python
>>> write(irisdf, "../data/wiris.csv", textfileparamsdict={"isindex": 1})
```

不写入列名
```python
>>> write(irisdf, "../data/wiris.csv", textfileparamsdict={"isheader": 0})
```

设置分隔符
```python
>>> write(irisdf, "../data/wiris.csv", textfileparamsdict={"sep": "\t"})
```

写入哪些列
```python
>>> write(irisdf, "../data/wiris.csv", textfileparamsdict={"columns": ["Petal.Length", "Petal.Width", "Species"]})
```

测试excel数据，有行名有列名地写入
```python
>>> write(irisdf, "../data/wiris.xlsx")
```

不写行名
```python
>>> write(irisdf, "../data/wiris.xlsx", excelfileparamsdict={"index": 0})
```

不写列名
```python
>>> write(irisdf, "../data/wiris.xlsx", excelfileparamsdict={"header": 0})
```

写入指定的列
```python
>>> write(irisdf, "../data/wiris.xlsx", excelfileparamsdict={"columns": ["Petal.Length", "Petal.Width", "Species"]})
```

写入xls格式
```python
>>> write(irisdf, "../data/wiris.xls", excelfileparamsdict={"engine": "xlsxwriter"})
```

测试pkl文件
```python
>>> write(irisdf, "../data/wiris.pkl")
```
