import pandas as pd

# 加载数据
file_path = r"C:\Users\LXY\Desktop\机器学习\pass_data.xlsx"
data = pd.read_excel(file_path)

# 查看数据的前几行，确保加载正确
print(data.head())

# 检查缺失值
print(data.isnull().sum())

# 填充缺失值（数值列使用均值填充，分类列使用众数填充）
data = data.fillna(data.mean())  # 对数值列填充均值
data = data.apply(lambda x: x.fillna(x.mode()[0]) if x.dtype == 'object' else x)  # 对类别列填充众数


