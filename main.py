import pandas as pd
import matplotlib.pyplot as plt
from soccer_pitch_grid import plot_pitch1  # 导入 plot_pitch1 函数

def plot_location_from_excel(excel_file_path):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file_path)

    # 提取 location 数据（每个值为 [x, y] 列表）
    location_data = df['location'].apply(eval)  # 将每个字符串转换为列表，如 '[x, y]' -> [x, y]

    # 过滤掉超出球场范围的点（x 在 [0, 105] 范围，y 在 [0, 68] 范围）
    valid_locations = [(x, y) for x, y in location_data if 0 <= x <= 105 and 0 <= y <= 68]

    # 创建图像并获取坐标轴
    fig, ax = plt.subplots(figsize=(12, 7))

    # 绘制球场
    ax = plot_pitch1(ax)  # 使用 plot_pitch1 绘制球场

    # 在球场上绘制每个有效的位置点
    for loc in valid_locations:
        x, y = loc
        ax.scatter(x, y, color='red', marker='o', s=50)  # 红色点标记位置

    # 显示图形
    plt.show()

# 使用 Excel 文件路径调用函数
plot_location_from_excel(r"C:\Users\LXY\Desktop\正式\马竞\Atlético Madrid_line_breaking_pass_1.xlsx")
