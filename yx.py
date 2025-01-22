import streamlit as st
import pandas as pd
import numpy as np

# 读取位置数据文件
def load_position_data(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file, header=None)
        elif uploaded_file.name.endswith('.txt'):
            # 尝试读取 tab 分隔或空格分隔的文件
            try:
                data = pd.read_csv(uploaded_file, header=None, delimiter='\t')
            except pd.errors.ParserError:
                data = pd.read_csv(uploaded_file, header=None, delim_whitespace=True)
        else:
            st.error("只支持 .xlsx 或 .txt 文件")
            return None
        return data
    return None

# 读取时间数据文件
def load_time_data(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file, header=None)
        elif uploaded_file.name.endswith('.txt'):
            # 尝试读取 tab 分隔或空格分隔的文件
            try:
                data = pd.read_csv(uploaded_file, header=None, delimiter='\t')
            except pd.errors.ParserError:
                data = pd.read_csv(uploaded_file, header=None, delim_whitespace=True)
        else:
            st.error("只支持 .xlsx 或 .txt 文件")
            return None
        return data
    return None

# 计算瞬时速度
def calculate_instantaneous_speed(position_data, time_data, frame):
    # 将数据强制转换为数值型，错误值会变成 NaN
    x = pd.to_numeric(position_data[0], errors='coerce').values
    y = pd.to_numeric(position_data[1], errors='coerce').values
    z = pd.to_numeric(position_data[2], errors='coerce').values
    
    # 将时间数据转换为数值型
    time = pd.to_numeric(time_data[0], errors='coerce').values
    
    # 处理空值（NaN）
    valid_data = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z) & ~np.isnan(time)
    x = x[valid_data]
    y = y[valid_data]
    z = z[valid_data]
    time = time[valid_data]

    # 确保 Frame 在有效范围内
    if frame > 0 and frame < len(x):
        delta_x = x[frame] - x[frame - 1]
        delta_y = y[frame] - y[frame - 1]
        delta_z = z[frame] - z[frame - 1]
        
        # 位移计算
        displacement = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        # 时间差
        delta_time = time[frame] - time[frame - 1]

        # 瞬时速度
        instantaneous_speed = displacement / delta_time
        return instantaneous_speed
    else:
        st.error("无效的 Frame 数据")
        return None

# 主函数
def main():
    st.title("瞬时速度计算器")

    # 上传位置数据文件
    uploaded_position_file = st.file_uploader("上传位置数据文件", type=["xlsx", "txt"])
    
    if uploaded_position_file is not None:
        position_data = load_position_data(uploaded_position_file)

        if position_data is not None:
            st.write("位置数据预览：")
            st.write(position_data.head())

            # 上传时间数据文件
            uploaded_time_file = st.file_uploader("上传时间数据文件", type=["xlsx", "txt"])
            
            if uploaded_time_file is not None:
                time_data = load_time_data(uploaded_time_file)

                if time_data is not None:
                    st.write("时间数据预览：")
                    st.write(time_data.head())

                    # 输入 Frame 数据
                    frame = st.number_input(f"请输入时刻（Frame）编号：", min_value=1, max_value=len(position_data), value=1)

                    if st.button("计算瞬时速度"):
                        # 计算瞬时速度
                        instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)

                        if instantaneous_speed is not None:
                            st.write(f"第 {frame} 时刻的瞬时速度为: {instantaneous_speed:.6f} 米/秒")
    
if __name__ == '__main__':
    main()
