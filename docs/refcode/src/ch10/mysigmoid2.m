% 编写另一个 sigmoid 函数，但设置 gamma = 0.5;。

function G = mysigmoid2(U,V)
% Sigmoid kernel function with slope gamma and intercept c
gamma = 0.5;
c = -1;
G = tanh(gamma*U*V' + c);
end

% 将此代码保存为您的 MATLAB® 路径上名为 mysigmoid2 的文件。