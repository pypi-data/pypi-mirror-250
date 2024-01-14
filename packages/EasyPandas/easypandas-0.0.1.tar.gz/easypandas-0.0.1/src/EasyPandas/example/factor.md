导入模块
```python
>>> with open("../factor.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> df = read("../data/toothgrowth.txt", textfileparamsdict={"sep": "\t"})
```

基本测试
```python
>>> res = factor(df["supp"])
>>> print(res)
```