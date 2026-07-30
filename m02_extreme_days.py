# 引入需要使用的python包
import pandas as pd

# 获取数据的示例代码

csv_path = "data/csi300_daily.csv"
df = pd.read_csv(csv_path, encoding="utf-8",parse_dates=["date"])
df = df.sort_values(by="date").reset_index(drop=True)
# 计算每日收益率
df["simple_return"] = df["close"].pct_change(fill_method=None)
# 计算极端收益日

# 输出极端收益日
print("最大收益日:")
print(df.nlargest(5, "simple_return"))
print("最小收益日:")
print(df.nsmallest(5, "simple_return"))
df["date_gap"] = df["date"].diff()      
print(df.nlargest(5, "date_gap"))  



