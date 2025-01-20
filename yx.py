import streamlit as st
import pandas as pd
import numpy as np

# 上传文件并读取数据
def load_data():
    uploaded_file = st.file_uploader("上传那个叫yx的EXCEL", type=["xlsx"])
    if uploaded_file is not None:
        # 读取 Excel 文件
        data = pd.read_excel(uploaded_file, header=None)
        return data
    return None

# 主函数
def main():
    st.title("💖💖💖🐑🌃")

    # 加载数据
    data = load_data()

    if data is not None:
        st.write("随便看一眼数据对不对：")
        st.write(data.head())

        # 输入起始和结束行号
        start_row = st.number_input(f"请输入起始行号（最小值: 1，最大值: {len(data)}）: ", min_value=1, max_value=len(data), value=1)
        end_row = st.number_input(f"请输入结束行号（最小值: {start_row}，最大值: {len(data)}）: ", min_value=start_row, max_value=len(data), value=len(data))

        # 输入时间间隔
        time_interval = st.number_input("请输入时间间隔（秒）: ", min_value=0.01, value=0.3, step=0.01)

        if st.button("计算位移与速度"):
            # 根据输入的起始和结束行号提取数据
            subset_data = data.iloc[start_row-1:end_row]  # 注意行号是从0开始索引的

            # 将数据强制转换为数值型，错误值会变成 NaN
            x = pd.to_numeric(subset_data[0], errors='coerce').values  # 第一列为 x
            y = pd.to_numeric(subset_data[1], errors='coerce').values  # 第二列为 y
            z = pd.to_numeric(subset_data[2], errors='coerce').values  # 第三列为 z

            # 处理可能存在的空值（NaN）行，可以选择删除含有NaN的行
            valid_data = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
            x = x[valid_data]
            y = y[valid_data]
            z = z[valid_data]

            # 计算该段位移（累加每一对相邻点的位移）
            total_displacement = 0
            for i in range(1, len(x)):
                distance = np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2 + (z[i] - z[i-1])**2)
                total_displacement += distance

            # 计算总时间（总行数 * 时间间隔）
            total_time = len(x) * time_interval

            # 计算平均速度
            average_speed = total_displacement / total_time

            # 输出结果，增加精度
            st.write(f"从第 {start_row} 行到第 {end_row} 行的总位移: {total_displacement:.6f} 米")
            st.write(f"该段的平均速度: {average_speed:.6f} 米/秒")
    
if __name__ == '__main__':
    main()

