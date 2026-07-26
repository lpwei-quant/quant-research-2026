from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


csv_path = "data/csi300_daily.csv"

df = pd.read_csv(
    csv_path,
    parse_dates=["date"]
)

print("DataFrame 对象类型：")
print(type(df))

print("\n数据规模 shape：")
print(df.shape)

print("\n行索引 index：")
print(df.index)

print("\n列标签 columns：")
print(df.columns)

print("\n各列数据类型 dtypes：")
print(df.dtypes)

print("\n前三行数据：")
print(df.head(3))

print("\n后三行数据：")
print(df.tail(3))
df = df.sort_values("date").reset_index(drop=True)

df["simple_return"] = df["close"].pct_change(fill_method=None)
print("\n简单收益率检查：")
print(df[["date","close","simple_return"]].head(5))
print("\n简单收益率缺失值数量：")
print(df["simple_return"].isna().sum())

print("\n有效收益率数量：")
print(df["simple_return"].notna().sum())

df["log_return"] = np.log1p(df["simple_return"])
print("\n简单收益率与对数收益率: ")
print(df[["date","close","simple_return","log_return"]].head(5))

print("\n对数收益率缺失值数量：")
print(df["log_return"].isna().sum())

print("\n有效对数收益率数量：")
print(df["log_return"].notna().sum())
df["nav"] = (1 + df["simple_return"].fillna(0)).cumprod()

print("\n净值检查：")
print(df[["date","close","simple_return","nav"]].head(5))

print("\n最后五行净值检查：")
print(df[["date","close","simple_return","nav"]].tail(5))
df["nav_from_log"] = np.exp(
    df["log_return"].fillna(0).cumsum()
)

print("\n对数收益率计算的净值检查：")
print(df[["date","close","simple_return","nav","nav_from_log"]].head(5))

print("\n最后五行对数收益率计算的净值检查：")
print(df[["date","close","simple_return","nav","nav_from_log"]].tail(5))
print(
    np.allclose(df["nav"],df["nav_from_log"])
)
figure_path = Path("output") / "figures" / "csi300_nav_curve.png"

figure_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    df["date"],
    df["nav"],
    label="CSI 300 NAV"
)

ax.axhline(
    y=1.0,
    linestyle="--",
    linewidth=1,
    label="Initial NAV"
)

ax.set_title("CSI 300 Normalized Net Value")
ax.set_xlabel("Date")
ax.set_ylabel("Net Value")

ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()

fig.savefig(
    figure_path,
    dpi=150,
    bbox_inches="tight"
)

print(f"\n净值曲线已保存至：{figure_path}")

plt.show()