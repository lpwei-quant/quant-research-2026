# 命令行速查

> 项目过程中实际用过的命令。每遇到新的就补一行。

## PowerShell

| 命令 | 作用 | Mac/Linux 对应 |
|---|---|---|
| `pwd` | 打印当前所在目录 | `pwd` |
| `cd 路径` | 切换目录 | `cd 路径` |
| `dir` | 列出目录内容 | `ls` |
| `Get-ChildItem -Force` | 列出内容,含隐藏项 | `ls -la` |
| `Get-Content 文件` | 打印文件全部内容 | `cat 文件` |
| `New-Item -Path X -ItemType File` | 新建文件 | `touch X` |
| `New-Item -Path X -ItemType Directory` | 新建目录 | `mkdir X` |
| `Remove-Item 文件` | 删除文件 | `rm 文件` |
| `code 文件` | 用 VSCode 打开 | `code 文件` |

## Git

| 命令 | 作用 |
|---|---|
| `git status --short` | 查看状态。第1列=暂存区,第2列=工作区 |
| `git add 文件` | 工作区 → 暂存区 |
| `git commit -m "type: 描述"` | 暂存区 → 提交历史 |
| `git ls-files` | 列出所有被追踪的文件 |
| `git rm --cached 文件` | 移出追踪,**保留磁盘文件** |
| `git restore --staged 文件` | 撤出暂存区 |
| `git log --oneline` | 查看提交历史 |
| `git show HEAD` | 查看最近一次提交的改动 |

**状态符号**

| 符号 | 含义 |
|---|---|
| `??` | 未追踪,Git 从没见过 |
| `A` | 新增,已进暂存区 |
| `M` | 已修改 |
| `D` | 已删除 |

## 虚拟环境

| 命令 | 作用 | Mac/Linux |
|---|---|---|
| `.\.venv\Scripts\Activate.ps1` | 激活 | `source .venv/bin/activate` |
| `deactivate` | 退出 | `deactivate` |
| `pip list` | 列出当前环境已装的包 | 相同 |
| `python -c "import sys; print(sys.executable)"` | 确认用的是哪个解释器 | 相同 |

## 踩过的坑

- **`>` 重定向**:PowerShell 5.1 默认写 UTF-16,`pip install -r` 会读不了。用 `Out-File -Encoding utf8`
- **`.\` 的规则**:命令位置**必须**写(安全设计,防同名劫持);参数位置**可写可不写**
- **`code 文件`**:只开缓冲区,**不按 Ctrl+S 磁盘上就没有这个文件**
- **`.gitignore` 只拦未追踪文件**:已追踪的要用 `git rm --cached` 请出去
- **`.git` 在 Windows 有 hidden 属性,`.venv` 没有**:点开头不等于隐藏,那是 Unix 约定
