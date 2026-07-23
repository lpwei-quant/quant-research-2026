import os

import akshare as ak
df = ak.stock_zh_index_daily_tx(
    symbol="sh000300",
    start_date="20230723",
    end_date="20260723"
)
print(type(df))
print(df.head(3))
print(df.tail(3))
print(df.shape)

os.makedirs("data", exist_ok=True)

output_path = os.path.join("data", "csi300_daily.csv")
df.to_csv(output_path, index=False,encoding="utf-8-sig")
print(f"数据已保存到:{output_path}")
