导入模块
```python
>>> with open("../strdesc.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> auto = read("../data/auto.dta")
```

DataFrame的测试
```python
>>> res = strdesc(auto[["make", "foreign"]], isprint=1)
```

Series的测试
```python
>>> res = strdesc(auto["foreign"], isprint=1)
```
