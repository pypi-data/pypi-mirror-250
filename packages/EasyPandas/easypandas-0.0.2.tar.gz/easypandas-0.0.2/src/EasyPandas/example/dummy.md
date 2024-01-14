导入模块
```python
>>> with open("../dummy.py", "rt", encoding="utf8") as fp: exec(fp.read())
```

测试还原哑变量
```python
>>> df = pd.DataFrame({"a": [1, 0, 0, 1], "b": [0, 1, 0, 0], "c": [0, 0, 1, 0]})
>>> print(df)
>>> res = dummy(df, getorfromdummy=0)
>>> print(res)
```

```python
>>> df = pd.DataFrame({"col1_a": [1, 0, 1], "col1_b": [0, 1, 0], "col2_a": [0, 1, 0], "col2_b": [1, 0, 0], "col2_c": [0, 0, 1]})
>>> print(df)
>>> res = dummy(df, getorfromdummy=0, sep="_")
>>> print(res)
```

测试变量虚拟化，给定前缀
```python
>>> s = pd.Series(list('abca'))
>>> print(s)
>>> res = dummy(s, prefix="AA")
>>> print(res)
```

测试变量虚拟化，给定前缀，给定分隔符
```python
>>> s = pd.Series(list('abca'))
>>> print(s)
>>> res = dummy(s, prefix="AA", prefix_sep="+")
>>> print(res)
```
