# Windows 命令行学习笔记

这是项目过程中使用过的基础命令速查，不属于分析结论。

## PowerShell

| 命令 | 作用 | Mac/Linux 对应 |
|---|---|---|
| `pwd` | 打印当前目录 | `pwd` |
| `cd 路径` | 切换目录 | `cd 路径` |
| `dir` | 列出目录内容 | `ls` |
| `Get-ChildItem -Force` | 列出内容（含隐藏项） | `ls -la` |
| `Get-Content 文件` | 打印文件内容 | `cat 文件` |
| `New-Item -Path X -ItemType File` | 新建文件 | `touch X` |
| `New-Item -Path X -ItemType Directory` | 新建目录 | `mkdir X` |

## Git

| 命令 | 作用 |
|---|---|
| `git status --short` | 查看暂存区和工作区状态 |
| `git add 文件` | 将指定文件加入暂存区 |
| `git commit -m "type: 描述"` | 创建提交 |
| `git ls-files` | 列出已追踪文件 |
| `git restore --staged 文件` | 将文件移出暂存区 |
| `git log --oneline` | 查看简洁提交历史 |

## 虚拟环境

| 命令 | 作用 | Mac/Linux 对应 |
|---|---|---|
| `.\.venv\Scripts\Activate.ps1` | 激活环境 | `source .venv/bin/activate` |
| `deactivate` | 退出环境 | `deactivate` |
| `python -m pip list` | 查看当前解释器的包 | 相同 |
| `python -c "import sys; print(sys.executable)"` | 确认解释器路径 | 相同 |

## 踩坑记录

- PowerShell 5.1 的默认重定向编码可能不是 UTF-8；写文本文件时要显式确认编码。
- Windows 中运行当前目录下的脚本通常需要 `.\` 前缀。
- `.gitignore` 只影响未追踪文件；已追踪文件需要单独移出索引。
