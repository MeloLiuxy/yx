import streamlit as st
import pandas as pd
import numpy as np

# 上传文件并读取数据
def load_data():
    uploaded_file = st.file_uploader("选择一个 Excel 文件", type=["xlsx"])
    if uploaded_file is not None:
        # 读取 Excel 文件
        data = pd.read_excel(uploaded_file, engine='openpyxl')
        return data
    return None

# 主函数
def main():
    st.title("刘小旖辛苦了")

    # 加载数据
    data = load_data()

    if data is not None:
        # 显示数据的列名和数据类型
        st.write("数据列名:", data.columns)
        st.write("数据类型:", data.dtypes)

        # 检查是否包含所需的列
        required_columns = ['Frame', 'x', 'y', 'z']
        for col in required_columns:
            if col not in data.columns:
                st.error(f"缺少必要的列：{col}")
                return

        st.write("刘小旖辛苦了！以下是数据预览：")
        st.write(data.head())

        # 输入序号范围和时间间隔
        start_index = st.number_input("请输入起始序号", min_value=int(data['Frame'].min()), max_value=int(data['Frame'].max()))
        end_index = st.number_input("请输入结束序号", min_value=start_index, max_value=int(data['Frame'].max()))
        time_interval = st.number_input("请输入时间间隔（秒）", min_value=0.01, value=0.3, step=0.01)

        if st.button("计算速度"):
            # 根据序号范围获取数据
            subset_data = data[(data['Frame'] >= start_index) & (data['Frame'] <= end_index)]

        

            # 获取 x, y, z 坐标
            x = subset_data['x'].values
            y = subset_data['y'].values
            z = subset_data['z'].values

            # 计算该段位移
            total_displacement = 0
            for i in range(1, len(x)):
                dx = x[i] - x[i-1]
                dy = y[i] - y[i-1]
                dz = z[i] - z[i-1]
                st.write(f"第 {i} 步: dx={dx}, dy={dy}, dz={dz}")  # 调试信息
                distance = np.sqrt(dx**2 + dy**2 + dz**2)
                total_displacement += distance

            # 计算该段的速度（总位移 / 时间间隔）
            # 需要确保时间计算准确
            total_time = (end_index - start_index + 1) * time_interval
            average_speed = total_displacement / total_time

            # 输出结果
            st.write(f"从序号 {start_index} 到 {end_index} 的总位移: {total_displacement:.2f} 米")
            st.write(f"该段的平均速度: {average_speed:.2f} 米/秒")

if __name__ == '__main__':
    main()

