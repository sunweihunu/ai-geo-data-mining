# processTurboFanDataTest.mlx

「深度学习（DeepL）」目录 · 对应书稿 **第11章 深度学习** · 3.1 KB · 代码 18 行

<p class="refcode-actions"><a class="md-button" href="https://matlab.mathworks.com/open/github/v1?repo=sunweihunu/ai-geo-data-mining&file=docs/mlx/src/DeepL_V2/processTurboFanDataTest.mlx" target="_blank" rel="noopener">在 MATLAB Online 中打开 ↗</a> <button class="md-button mlxcopy" type="button">复制代码</button> <a class="md-button" href="../src/DeepL_V2/processTurboFanDataTest.mlx" download>下载 processTurboFanDataTest.mlx</a></p>

!!! tip "MATLAB 实时脚本（.mlx）"

    本页是该实时脚本内代码与文字的网页摘录（运行输出与图窗不随网页展示）。「复制代码」复制脚本全部代码，「下载」保存原始 .mlx 文件，「在 MATLAB Online 中打开」在本站仓库推送到 GitHub 后生效。

## 脚本内容

The function processTurboFanDataTest extracts the data from filenamePredictors

and filenameResponses and returns the cell arrays predictors and responses, which contain the test predictor and response sequences. In filenamePredictors, the time series ends some time prior to system failure. The data in filenameResponses provides a vector of true RUL values for the test data.

```matlab
function [predictors,responses] = processTurboFanDataTest(filenamePredictors,filenameResponses)

predictors = processTurboFanDataTrain(filenamePredictors);

RULTest = dlmread(filenameResponses);

numObservations = numel(RULTest);

responses = cell(numObservations,1);
for i = 1:numObservations
    X = predictors{i};
    sequenceLength = size(X,2);

    rul = RULTest(i);
    responses{i} = rul+sequenceLength-1:-1:rul;
end

end
```
