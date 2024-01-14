导入模块
```python
>>> with open("../na.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> import numpy as np
>>> import pandas as pd
>>> df = pd.DataFrame(np.random.randn(5, 3), index=["a", "c", "e", "f", "h"], columns=["one", "two", "three"])
>>> df["four"] = "bar"
>>> df["five"] = df["one"] > 0
>>> df2 = df.reindex(["a", "b", "c", "d", "e", "f", "g", "h"])
```

DataFrame判断是否为缺失值
```python
>>> res = na(df2, "isna")
>>> print(res)
```

Series判断是否为缺失值
```python
>>> res = na(df2["two"], "isna")
>>> print(res)
```

DataFrame判断是否不为缺失值
```python
>>> res = na(df2, "notna")
>>> print(res)
```

Series判断是否不为缺失值
```python
>>> res = na(df2["two"], "notna")
>>> print(res)
```

DataFrame填充缺失值为平均数
```python
>>> res = na(df2.iloc[:, :3], "fill")
>>> print(res)
```

DataFrame填充缺失值为100
```python
>>> res = na(df2.iloc[:, :3], "fill", fillvalue=100)
>>> print(res)
```

Series填充缺失值为平均数
```python
>>> res = na(df2["two"], "fill")
>>> print(res)
```

Series填充缺失值为100
```python
>>> res = na(df2["two"], "fill", fillvalue=100)
>>> print(res)
```

Series填充缺失值为foo
```python
>>> res = na(df2["four"], "fill", fillvalue="foo")
>>> print(res)
```

DataFrame向前填充
```python
>>> res = na(df2, "ffill")
>>> print(res)
```

Series向前填充
```python
>>> res = na(df2, "ffill")
>>> print(res)
```

Series向前填充
```python
>>> res = na(df2["four"], "ffill")
>>> print(res)
```

DataFrame向后填充
```python
>>> res = na(df2, "ffill")
>>> print(res)
```

Series向后填充
```python
>>> res = na(df2, "ffill")
>>> print(res)
```

Series向后填充
```python
>>> res = na(df2["four"], "ffill")
>>> print(res)
```

DataFrame删除缺失值，按行删除，只要某行存在缺失值就删除，不原地删除
```python
>>> res = na(df2, "delete")
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按行删除，只要某行存在缺失值就删除，原地删除
```python
>>> res = na(df2, "delete", inplace=1)
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按行删除，某行全为缺失值才删除，不原地删除
```python
>>> res = na(df2, "delete", how="all")
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按行删除，某行全为缺失值才删除，原地删除
```python
>>> res = na(df2, "delete", how="all", inplace=1)
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按行删除，只要two列存在缺失值就删除，不原地删除
```python
>>> res = na(df2, "delete", subset="two")
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按行删除，two列和four列全为缺失值才删除，不原地删除
```python
>>> res = na(df2, "delete", subset=["two", "four"], how="all")
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按列删除，某列全为缺失值才删除，不原地删除
```python
>>> res = na(df2, "delete", how="all", bycol=1)
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按列删除，某列存在缺失值就删除，不原地删除
```python
>>> res = na(df2, "delete", bycol=1)
>>> print(df2)
>>> print(res)
```

DataFrame删除缺失值，按列删除，某列存在缺失值就删除，原地删除
```python
>>> res = na(df2, "delete", bycol=1, inplace=1)
>>> print(df2)
>>> print(res)
```

Series删除缺失值，存在缺失值就删除，不原地删除
```python
>>> res = na(df2["two"], "delete")
>>> print(df2["two"])
>>> print(res)
```

Series删除缺失值，全为缺失值才删除，不原地删除（Series只能按照上面的方式删除，这种方法是无法删除的）
```python
>>> res = na(df2["two"], "delete", how="all")
>>> print(df2["two"])
>>> print(res)
```

Series删除缺失值，存在缺失值就删除，原地删除（DataFrame的列是视图，无法原地删除）
```python
>>> res = na(df2["two"], "delete", inplace=1)
>>> print(df2["two"])
>>> print(res)
```

Series删除缺失值，存在缺失值就删除，原地删除（DataFrame的列是视图，无法原地删除，先复制才能）
```python
>>> s = df2["two"].copy()
>>> res = na(s, "delete", inplace=1)
>>> print(s)
>>> print(res)
```
