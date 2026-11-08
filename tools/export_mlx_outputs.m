function report = export_mlx_outputs(folderIds)
%EXPORT_MLX_OUTPUTS 把 Code_Mlx 的 .mlx 实时脚本批量导出为带运行输出的 Markdown
%
%   export_mlx_outputs({'DR','LDA'})   按目录名批量导出（缺省全部 7 个目录）
%
%   用 MATLAB R2022a+ 的 export 命令把每个 .mlx 转成 Markdown（Format="markdown"，
%   EmbedImages=false）：代码块 + 命令行输出（```matlabTextOutput）+ 图窗 PNG，
%   图存到 <name>_media/。只导出脚本里已保存的运行输出，不重新运行代码。
%
%   输出根目录固定为 网站仓库同级 的 Code_Mlx_export/<目录名>/，
%   供 tools/build_mlx.mjs（第二参数可覆盖）读取并注入站点页面。
%
%   返回 report 结构体数组：folder/file/ok/media/outputs/err。

if nargin < 1 || isempty(folderIds)
    folderIds = {'DR','LDA','kNN','DecisionTree_v2','ANN','SVM_V1','DeepL_V2'};
end

here = fileparts(mfilename('fullpath'));        % 网站仓库 tools/
repoRoot = fileparts(here);                     % 网站仓库根
mlxRoot = fullfile(repoRoot, '..', 'Code_Mlx');
expRoot = fullfile(repoRoot, '..', 'Code_Mlx_export');
subMap = containers.Map({'DR','LDA'}, {'Code_DR','Code_LDA'});

report = struct('folder',{},'file',{},'ok',{},'media',{},'outputs',{},'err',{});
nFig = 0; nOut = 0; nPlain = 0;

for fi = 1:numel(folderIds)
    id = folderIds{fi};
    if isKey(subMap, id), sub = char(subMap(id)); else, sub = ''; end
    srcDir = fullfile(mlxRoot, id, sub);
    outDir = fullfile(expRoot, id);
    if ~exist(srcDir, 'dir'), error('源目录不存在: %s', srcDir); end
    if ~exist(outDir, 'dir'), mkdir(outDir); end

    listing = dir(fullfile(srcDir, '*.mlx'));
    [~,order] = sort({listing.name});
    listing = listing(order);

    for k = 1:numel(listing)
        [~, base, e] = fileparts(listing(k).name);
        src = fullfile(srcDir, listing(k).name);
        dst = fullfile(outDir, [base '.md']);
        media = fullfile(outDir, [base '_media']);
        r = struct('folder',id,'file',listing(k).name,'ok',false, ...
                   'media',0,'outputs',0,'err','');
        try
            if exist(media, 'dir'), rmdir(media, 's'); end   % 清掉旧图，避免残留
            export(src, dst, Format="markdown", EmbedImages=false);
            txt = fileread(dst);
            r.outputs = strfind(txt, '```matlabTextOutput');
            r.media = numel(dir(fullfile(media, '*.png')));
            r.ok = true;
            if r.media > 0, nFig = nFig + 1;
            elseif ~isempty(r.outputs), nOut = nOut + 1;
            else, nPlain = nPlain + 1;
            end
        catch err
            r.err = err.message;
            fprintf('  ERR %s/%s: %s\n', id, listing(k).name, err.message);
        end
        report(end+1) = r; %#ok<AGROW>
        fprintf('  %s/%s  图%d 输出%d\n', id, listing(k).name, r.media, numel(r.outputs));
    end
    fprintf('[%s] 完成：%d 个脚本\n', id, numel(listing));
end

fprintf('== 全部完成：有图窗 %d，仅文本输出 %d，无输出 %d ==\n', nFig, nOut, nPlain);
end
