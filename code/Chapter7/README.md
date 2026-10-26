# Chapter7 配套代码与数据 —— k 最近邻（kNN）模型

对应书稿《人工智能与地理数据挖掘》**第07章 k最近邻（kNN）模型**（原始讲义：《机器学习与地学应用》第七讲）。

## 文件清单

| 文件 | 对应书稿章节 | 内容 |
|------|--------------|------|
| `kNN_exp01_hospital.m` | 7.8.1 案例1 | 医院数据中为 5 个新病人查找最近邻（`knnsearch`，默认 k=1），并可视化 |
| `kNN_exp02_iris_classify.m` | 7.8.2 案例2 | Fisher 鸢尾花 kNN 分类：1 个与 3 个待测样本（k=10），闵可夫斯基与切比雪夫两种距离函数对比，`tabulate` 统计邻居品种构成并投票定类 |
| `kNN_exp03_iris_k_effect.m` | 7.8.3 案例3 | 全部 4 个属性下，k=1..10 的训练集回代正确率与 10 折交叉验证正确率（`fitcknn` + `predict` + `crossval`），绘制性能随 k 变化曲线 |
| `data/hospital_new_patients.csv` | 7.8.1 | 案例1 的 5 个待测病人（年龄、体重），与脚本内 Y 取值一致 |
| `data/iris_query_samples.csv` | 7.8.2 | 案例2 的待测鸢尾花查询点（花瓣长度、宽度），与脚本内取值一致 |

## 运行环境与说明

- 需要 **MATLAB 及 Statistics and Machine Learning Toolbox**（`knnsearch`、`fitcknn`、`crossval` 均来自该工具箱）。
- 训练数据均为 MATLAB **内置数据集**：`hospital`（100 个病人）、`fisheriris`（150 个鸢尾花标本，`meas` 为 150×4 测量值、`species` 为品种名），无需另行下载；`data/` 中仅存放待测查询点示例值。
- 运行前将 MATLAB 当前文件夹切换到本目录（`脚本/Chapter7`），直接运行各脚本即可。
- 待测样本的具体数值为**示例值**；课件运行结果（versicolor 8 ∶ virginica 2 等，见书稿表 7-5）与实际输出可能因查询点取值不同而略有差异，以自己的运行输出为准。
- 课件英文原版示例：`openExample('stats/ClassifyingQueryDataUsingKnnsearchExample')`。
