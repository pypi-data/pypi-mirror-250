导入模块
```python
>>> with open("../filter.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
```

DataFrame的筛选

等于筛选
```python
>>> res = filter(iris, "`Sepal.Length` == 4.9")
>>> print(res)
```

不等于筛选
```python
>>> res = filter(iris, "`Sepal.Length` != 4.9")
>>> print(res)
```

大于筛选
```python
>>> res = filter(iris, "`Sepal.Length` > 4.9")
>>> print(res)
```

大于等于筛选
```python
>>> res = filter(iris, "`Sepal.Length` >= 4.9")
>>> print(res)
```

小于筛选
```python
>>> res = filter(iris, "`Sepal.Length` < 4.9")
>>> print(res)
```

小于等于筛选
```python
>>> res = filter(iris, "`Sepal.Length` <= 4.9")
>>> print(res)
```

字符串等于筛选
```python
>>> res = filter(iris, "`Species` == 'setosa'")
>>> print(res)
```

字符串不等于筛选
```python
>>> res = filter(iris, "`Species` != 'setosa'")
>>> print(res)
```

字符串包含筛选
```python
>>> res = filter(iris, "`Species` ^C$ 'v'")
>>> print(res)
```

字符串不包含筛选
```python
>>> res = filter(iris, "`Species` !^C$ 'v'")
>>> print(res)
```

字符串开始为
```python
>>> res = filter(iris, "`Species` ^^ 'set'")
>>> print(res)
```

字符串结束为
```python
>>> res = filter(iris, "`Species` $$ 'color'")
>>> print(res)
```

列之间的大于比较
```python
>>> res = filter(iris, "`Sepal.Length` > `Petal.Length`")
>>> print(res)
```

列之间的大于等于比较
```python
>>> res = filter(iris, "`Sepal.Width` > `Petal.Width`")
>>> print(res)
```

列之间的小于比较
```python
>>> res = filter(iris, "`Sepal.Width` < `Petal.Width`")
>>> print(res)
```

列之间的小于等于比较
```python
>>> res = filter(iris, "`Sepal.Length` <= `Petal.Length`")
>>> print(res)
```

列之间的等于比较
```python
>>> res = filter(iris, "`Sepal.Length` == `Petal.Length`")
>>> print(res)
```

列之间的不等于比较
```python
>>> res = filter(iris, "`Sepal.Width` != `Petal.Width`")
>>> print(res)
```

多个筛选条件
```python
>>> res = filter(iris, "`Sepal.Length` >= 5", "`Sepal.Length` <= 4.5", "and")
>>> print(res)
>>> res = filter(iris, "`Sepal.Length` >= 5", "`Sepal.Length` <= 4.5", "or")
>>> print(res)
>>> res = filter(iris, "`Sepal.Length` >= 5", "`Sepal.Length` <= 4.5", None)
>>> print(res)
>>> res = filter(iris, "`Species` ^C$ 'color'", "`Species` ^C$ 'set'", "or")
>>> print(res)
>>> res = filter(iris, "`Species` ^C$ 'color'", "`Sepal.Length` > 5", "and")
>>> print(res)
```

测试Series

等于筛选
```python
>>> res = filter(iris["Sepal.Length"], "== 4.9")
>>> print(res)
```

不等于筛选
```python
>>> res = filter(iris["Sepal.Length"], "!= 4.9")
>>> print(res)
```

大于筛选
```python
>>> res = filter(iris["Sepal.Length"], "> 4.9")
>>> print(res)
```

大于等于筛选
```python
>>> res = filter(iris["Sepal.Length"], ">= 4.9")
>>> print(res)
```

小于筛选
```python
>>> res = filter(iris["Sepal.Length"], "< 4.9")
>>> print(res)
```

小于等于筛选
```python
>>> res = filter(iris["Sepal.Length"], "<= 4.9")
>>> print(res)
```

字符串等于筛选
```python
>>> res = filter(iris["Species"], "== 'setosa'")
>>> print(res)
```

字符串不等于筛选
```python
>>> res = filter(iris["Species"], "!='setosa'")
>>> print(res)
```

字符串包含筛选
```python
>>> res = filter(iris["Species"], "^C$ 'v'")
>>> print(res)
```

字符串不包含筛选
```python
>>> res = filter(iris["Species"], "!^C$ 'v'")
>>> print(res)
```

字符串开始为
```python
>>> res = filter(iris["Species"], "^^ 'set'")
>>> print(res)
```

字符串结束为
```python
>>> res = filter(iris["Species"], "$$ 'color'")
>>> print(res)
```

对于一个一般的Series

```python
>>> s = pd.Series([i for i in range(100)])
>>> res = filter(s, ">90")
>>> print(res)
```
