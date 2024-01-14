导入模块
```python
>>> import pandas as pd
>>> with open("../reshape.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> df = pd.DataFrame({'foo': ['one', 'one', 'one', 'two', 'two', 'two'], 'bar': ['A', 'B', 'C', 'A', 'B', 'C'], 'baz': [1, 2, 3, 4, 5, 6], 'zoo': ['x', 'y', 'z', 'q', 'w', 't']})
```

测试l2w
```python
>>> print(df)
>>> res = reshape(df, "l2w", index='foo', columns='bar', values='baz')
>>> print(res)
```

测试w2l
```python
>>> res = reshape(df, "l2w", index='foo', columns='bar', values='baz')
>>> print(res)
>>> res = reshape(res, "w2l", groups={"baz": ["A", "B", "C"]})
>>> print(res)
```
