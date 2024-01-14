导入模块
```python
>>> import pandas as pd
>>> with open("../merge.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> df1 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'], 'value_1': [1, 2, 3, 5]})
>>> df2 = pd.DataFrame({'key': ['foo', 'bar', 'baz', 'foo'], 'value_2': [5, 6, 7, 8]})
```

测试按照变量合并，inner合并
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], isbyvar=1, on="key", how="inner")
>>> print(res)
```

测试按照变量合并，outer合并
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], isbyvar=1, on="key", how="outer")
>>> print(res)
```

测试按照变量合并，left合并
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], isbyvar=1, on="key", how="left")
>>> print(res)
```

测试普通合并，按行合并
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2])
>>> print(res)
```

测试普通合并，按列合并
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], axis=1)
>>> print(res)
```

测试普通合并，按列合并，重新排列索引
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], axis=1, ignore_index=1)
>>> print(res)
```

测试普通合并，按行合并，设置多重索引
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], axis=0, keys=["left", "right"])
>>> print(res)
```

测试普通合并，按行合并，outer合并
```python
>>> print(df1)
>>> print(df2)
>>> res = merge([df1, df2], axis=0, keys=["left", "right"], join="outer")
>>> print(res)
```
