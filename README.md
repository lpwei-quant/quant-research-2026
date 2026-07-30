# 沪深300 收益率与风险结构研究

基于沪深300指数(000300)2023-07-24 至 2026-07-22 共 726 个交易日数据,
构建收益率计算、净值重构与极值归因分析流程。

## 核心发现

- 三年累计收益 **+23.97%**(期末净值 1.2397),年化约 7.4%
- **2024-09-24 至 10-08 的 9 个交易日累计上涨约 32.5%,超过三年总回报**
- 最大单日跌幅 -7.05%(2024-10-09)紧随最大涨幅簇,与之属同一事件
- 2024-10-08 日收益率 +5.93%,但开盘价即全天最高价,**当日开盘买入者实际亏损 4.37%**
- 采用简单收益率与对数收益率双路径构造净值,交叉验证一致

## 快速开始

```bash
git clone <你的仓库地址>
cd quant_research_summer_2026

python -m venv .venv
.\.venv\Scripts\Activate.ps1      # Windows
source .venv/bin/activate         # Mac/Linux

pip install -r requirements.txt

python fetch_csi300.py            # 获取数据(data/ 未纳入版本控制)
python src/day02_return_analysis.py
python src/m02_extreme_days.py
```

## 目录结构
quant_research_summer_2026/
├── src/
│ ├── day02_return_analysis.py # 收益率与净值构造
│ └── m02_extreme_days.py # 极值归因
├── fetch_csi300.py # 数据获取
├── inspect_csi300.py # 数据检查
├── output/figures/ # 图表输出
├── notes/commands.md # 命令行速查
└── requirements.txt
## 方法说明

**收益率**
简单收益率: R_t = P_t / P_{t-1} - 1
对数收益率: r_t = ln(1 + R_t)
**净值构造**(两条数学等价路径,用 np.allclose 交叉验证)
路径一: NAV_T = Π (1 + R_t)
路径二: NAV_T = exp( Σ r_t )
**已知局限**

- 使用价格指数(000300)而非全收益指数(H00300),不含股息再投资,
  系统性低估真实持有收益,幅度约等于市场股息率
- 收盘价收益率不反映日内路径,极端行情下与可实现收益差异显著