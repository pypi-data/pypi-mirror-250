导入模块
```python
>>> import numpy as np
>>> with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../plot.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> with open("../factor.py", "rt", encoding="utf8") as fp: exec(fp.read())
>>> iris = read("../data/iris.xlsx")
```

Series的线图绘制
```python
>>> np.random.seed(123456)
>>> ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
>>> ts = ts.cumsum()
>>> plot(ts, plottype="line")
```

DataFrame的线图绘制
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df, plottype="line")
```

Series的线图绘制，给定参数
```python
>>> np.random.seed(123456)
>>> ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
>>> ts = ts.cumsum()
>>> plot(ts, plottype="line", color="black")
```

绘制xy之间的线图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> df["A"] = range(1, 1+df.shape[0])
>>> plot(df, plottype="line", x="A", y="C")
```

Series的柱状图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[4, ], plottype="bar")
```

DataFrame的柱状图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[:4, ], plottype="bar")
```

DataFrame的柱状图，堆叠形式
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[:4, ], plottype="bar", stacked=True)
```

Series的水平柱状图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[4, ], plottype="barh")
```

DataFrame的水平柱状图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[:4, ], plottype="barh")
```

DataFrame的水平柱状图，堆叠形式
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[:4, ], plottype="barh", stacked=True)
```

Series的直方图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df.iloc[:, 0], plottype="hist")
```

DataFrame的直方图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df, plottype="hist")
```

DataFrame的直方图，堆叠形式
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.randn(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> df = df.cumsum()
>>> plot(df, plottype="hist", stacked=True)
```

Series的箱线图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.rand(10, 5), columns=["A", "B", "C", "D", "E"])
>>> plot(df["A"], plottype="box")
```

DataFrame的箱线图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.rand(10, 5), columns=["A", "B", "C", "D", "E"])
>>> plot(df, plottype="box")
```

DataFrame的分组箱线图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.rand(10, 5), columns=["A", "B", "C", "D", "E"])
>>> df["X"] = pd.Series(["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"])
>>> plot(df, plottype="box", by="X")
```

Series的面积图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.rand(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> plot(df.loc[: ,"A"], plottype="area")
```

DataFrame的面积图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(np.random.rand(1000, 4), index=pd.date_range("1/1/2000", periods=1000), columns=list("ABCD"))
>>> plot(df, plottype="area")
```

散点图
```python
>>> plot(iris, plottype="scatter", x="Sepal.Length", y="Sepal.Width")
```

散点图，参数
```python
>>> plot(iris, plottype="scatter", x="Sepal.Length", y="Sepal.Width", s=50, color="black", alpha=0.3)
```

散点图，参数
```python
>>> iris["category_species"] = factor(iris["Species"], as_category=1)
>>> plot(iris, plottype="scatter", x="Sepal.Length", y="Sepal.Width", s=50, c="category_species", alpha=0.3, colormap="Set2")
```

Series的饼图
```python
>>> np.random.seed(123456)
>>> series = pd.Series(3 * np.random.rand(4), index=["a", "b", "c", "d"], name="series")
>>> plot(series, plottype="pie")
```

DataFrame的饼图
```python
>>> np.random.seed(123456)
>>> df = pd.DataFrame(3 * np.random.rand(4, 2), index=["a", "b", "c", "d"], columns=["x", "y"])
>>> plot(df, plottype="pie")
```

DataFrame的scattermatrix
```python
>>> np.random.seed(123456)
>>> plot(iris.iloc[:, 1:-1], plottype="scatter_matrix")
```

DataFrame的andrew曲线
```python
>>> np.random.seed(123456)
>>> plot(iris.iloc[:, 1:], plottype="andrews_curves", class_column="Species")
```

DataFrame的parallel_coordinates曲线
```python
>>> np.random.seed(123456)
>>> plot(iris.iloc[:, 1:], plottype="parallel_coordinates", class_column="Species")
```

Series的lag_plot曲线
```python
>>> np.random.seed(123456)
>>> spacing = np.linspace(-99 * np.pi, 99 * np.pi, num=1000)
>>> data = pd.Series(0.1 * np.random.rand(1000) + 0.9 * np.sin(spacing))
>>> plot(data, plottype="lag_plot")
```

Series的lag_plot曲线，给定参数
```python
>>> np.random.seed(123456)
>>> spacing = np.linspace(-99 * np.pi, 99 * np.pi, num=1000)
>>> data = pd.Series(0.1 * np.random.rand(1000) + 0.9 * np.sin(spacing))
>>> plot(data, plottype="lag_plot", lag=3)
```

Series的autocorrelation_plot曲线
```python
>>> np.random.seed(123456)
>>> spacing = np.linspace(-99 * np.pi, 99 * np.pi, num=1000)
>>> data = pd.Series(0.1 * np.random.rand(1000) + 0.9 * np.sin(spacing))
>>> plot(data, plottype="autocorrelation_plot")
```

保存文件
```python
>>> np.random.seed(123456)
>>> spacing = np.linspace(-99 * np.pi, 99 * np.pi, num=1000)
>>> data = pd.Series(0.1 * np.random.rand(1000) + 0.9 * np.sin(spacing))
>>> plot(data, "autocorrelation_plot", "../data/自相关系数图.pdf")
```