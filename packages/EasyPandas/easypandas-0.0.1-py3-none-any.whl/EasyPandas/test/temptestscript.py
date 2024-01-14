import numpy as np
with open("../read.py", "rt", encoding="utf8") as fp: exec(fp.read())
with open("../plot.py", "rt", encoding="utf8") as fp: exec(fp.read())
with open("../factor.py", "rt", encoding="utf8") as fp: exec(fp.read())
iris = read("../data/iris.xlsx")
np.random.seed(123456)
spacing = np.linspace(-99 * np.pi, 99 * np.pi, num=1000)
data = pd.Series(0.1 * np.random.rand(1000) + 0.9 * np.sin(spacing))
plot(data, "autocorrelation_plot", "../data/自相关系数图.pdf")
