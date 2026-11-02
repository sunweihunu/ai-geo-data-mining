# processTurboFanDataTrain.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 3.2 KB · 代码 18 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/processTurboFanDataTrain.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/processTurboFanDataTrain.mlx" download>下载 processTurboFanDataTrain.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

## 脚本内容

The function processTurboFanDataTrain extracts the data from

filenamePredictors and returns the cell arrays predictors and responses which contain the predictor and response sequences, respectively. The data contains zip-compressed text files with 26 columns of numbers, separated by spaces. Each row is a snapshot of data taken during a single operational cycle, and each column is a different variable. The columns correspond to the following: 1: Unit number 2: Time in cycles 3–5: Operational settings 6–26: Sensor measurements 1–17

```matlab
function [predictors,responses] = processTurboFanDataTrain(filenamePredictors)

dataTrain = dlmread(filenamePredictors);

numObservations = max(dataTrain(:,1));

predictors = cell(numObservations,1);
responses = cell(numObservations,1);
for i = 1:numObservations
    idx = dataTrain(:,1) == i;

    predictors{i} = dataTrain(idx,3:end)';

    timeSteps = dataTrain(idx,2)';
    responses{i} = fliplr(timeSteps);
end

end
```
