import streamlit as st
import pandas as pd
import numpy as np

# 上传文件并读取数据
def load_data(uploaded_file):
    # 通过扩展名来判断文件类型，选择不同的读取方法
    if uploaded_file is not None:
        # 判断文件类型并进行相应处理
        if uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file, header=None)
        elif uploaded_file.name.endswith('.txt'):
            data = pd.read_csv(uploaded_file, header=None, delimiter='\t')  # 假设 txt 是制表符分隔
        else:
            st.error("只支持 .xlsx 或 .txt 文件")
            return None
        return data
    return None

# 计算瞬时速度
def calculate_instantaneous_speed(data, frame, time_interval):
    # 根据给定的时刻，计算前后点之间的瞬时速度
    x = pd.to_numeric(data[0], errors='coerce').values
    y = pd.to_numeric(data[1], errors='coerce').values
    z = pd.to_numeric(data[2], errors='coerce').values

    # 处理可能存在的空值（NaN）行
    valid_data = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
    x = x[valid_data]
    y = y[valid_data]
    z = z[valid_data]

    # 确保我们不会访问超出范围的索引
    if frame > 0 and frame < len(x):
        # 使用前后的两个数据点来计算瞬时速度
        delta_x = x[frame] - x[frame - 1]
        delta_y = y[frame] - y[frame - 1]
        delta_z = z[frame] - z[frame - 1]

        # 位移
        displacement = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        # 瞬时速度
        instantaneous_speed = displacement / time_interval
        return instantaneous_speed
    else:
        st.error("无效的时刻或 Frame 数据")
        return None

# 主函数
def main():
    st.title("💖💖💖🐑🌃 瞬时速度计算器")

    # 上传文件
    uploaded_file = st.file_uploader("上传时间数据文件", type=["xlsx", "txt"])
    
    if uploaded_file is not None:
        # 读取数据
        data = load_data(uploaded_file)
        
        if data is not None:
            st.write("数据预览：")
            st.write(data.head())

            # 输入时刻或 Frame 数据
            frame = st.number_input(f"请输入时刻（Frame）编号：", min_value=1, max_value=len(data), value=1)

            # 输入时间间隔
            time_interval = st.number_input("请输入时间间隔（秒）: ", min_value=0.01, value=0.3, step=0.01)

            if st.button("计算瞬时速度"):
                # 计算瞬时速度
                instantaneous_speed = calculate_instantaneous_speed(data, frame, time_interval)

                if instantaneous_speed is not None:
                    st.write(f"第 {frame} 时刻的瞬时速度为: {instantaneous_speed:.6f} 米/秒")
    
if __name__ == '__main__':
    main()
