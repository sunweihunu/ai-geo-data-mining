% 编写一个函数，该函数接受特征空间中的两个矩阵作为输入，并使用 sigmoid 核将它们转换为 Gram 矩阵。

function G = mysigmoid(U,V)
% Sigmoid kernel function with slope gamma and intercept c
gamma = 1;
c = -1;
G = tanh(gamma*U*V' + c);
end

% 将此代码保存为您的 MATLAB® 路径上名为 mysigmoid 的文件。