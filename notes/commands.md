# 项目命令速查

## 环境与运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python fetch_csi300.py
python inspect_csi300.py
python src/day02_return_analysis.py
python src/m02_extreme_days.py
```

## Git日常检查

```powershell
git status --short
git diff
git log --oneline -10
```

项目生成的原始数据、指标CSV和事件明细均已在 `.gitignore` 中排除；README展示用净值图保留在版本库中。

