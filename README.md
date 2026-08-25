# 沪深 300 收益率与极端交易日研究

一个可复现的 Python 小型研究：对沪深 300 价格指数做数据质量检查、收益率计算、净值双路径校验与极端交易日分析。

![沪深 300 归一化净值曲线](output/figures/csi300_nav_curve.png)

## 数据与结论

- 数据口径：沪深 300 价格指数（000300），2023-07-24 至 2026-07-22，共 726 个交易日。
- 样本期末净值为 **1.239676**，累计价格收益约 **+23.97%**。
- 2024-09-24 至 2024-10-08 实际包含 **6 个交易日**；以前一交易日收盘为基准，累计上涨约 **+32.47%**。
- 最大单日收盘到收盘跌幅出现在 2024-10-09，约 **-7.05%**。
- 2024-10-08 收盘到收盘上涨约 **+5.93%**，但开盘到收盘下跌约 **-4.37%**，说明日收益率不能代替日内路径。

以上均为样本内描述性结果，不构成预测或交易建议。

## 方法与质量控制

简单收益率为 `P_t / P_(t-1) - 1`，对数收益率为 `ln(1 + R_t)`。净值同时通过简单收益率连乘和对数收益率累加后取指数两条路径计算，并用 `numpy.allclose` 交叉检查。

程序还会：

- 先按日期排序，拒绝重复日期、缺失价格和非正价格；
- 仅允许首行收益率因缺少前序价格而为空；
- 拒绝用整列 `fillna(0)` 隐藏序列中间的数据问题；
- 在极端日输出中同时给出收盘到收盘和开盘到收盘收益。

详细口径见 [M02 研究说明](docs/m02_return_nav.md)。

## 快速复现

```powershell
git clone https://github.com/lpwei-quant/quant-research-2026.git
cd quant-research-2026

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

python -m src.fetch_csi300
python -m src.inspect_csi300
python -m src.return_nav_analysis
python -m src.extreme_days_analysis
python -m pytest -v
```

数据目录不纳入版本控制，运行获取脚本后生成 `data/csi300_daily.csv`。图表会写入 `output/figures/`。

## 目录

```text
quant-research-2026/
├── .github/workflows/ci.yml
├── docs/
│   ├── m02_return_nav.md
│   └── windows_cli_notes.md
├── output/figures/csi300_nav_curve.png
├── src/
│   ├── fetch_csi300.py
│   ├── inspect_csi300.py
│   ├── return_nav_analysis.py
│   └── extreme_days_analysis.py
├── tests/
├── README.md
└── requirements.txt
```

## 已知局限

- 价格指数不含股息再投资，不能替代全收益指数。
- 收盘到收盘收益不反映完整日内路径，也不等于任意时点的可实现收益。
- 当前结果没有纳入交易成本、流动性与样本外检验。
