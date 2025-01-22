import streamlit as st
import pandas as pd
import numpy as np

# 上传位置数据并读取
def load_position_data():
    uploaded_position_file = st.file_uploader("上传位置数据文件", type=["xlsx", "csv"])
    if uploaded_position_file is not None:
        # 读取 Excel 或 CSV 文件
        position_data = pd.read_excel(uploaded_position_file) if uploaded_position_file.name.endswith('.xlsx') else pd.read_csv(uploaded_position_file)
        
        # 清理列名中的多余空格
        position_data.columns = position_data.columns.str.strip()
        
        return position_data
    return None

# 上传时间数据并读取
def load_time_data():
    uploaded_time_file = st.file_uploader("上传时间数据文件", type=["xlsx", "csv"])
    if uploaded_time_file is not None:
        # 读取 Excel 或 CSV 文件
        time_data = pd.read_excel(uploaded_time_file) if uploaded_time_file.name.endswith('.xlsx') else pd.read_csv(uploaded_time_file)
        
        # 清理列名中的多余空格
        time_data.columns = time_data.columns.str.strip()
        
        # 打印列名以检查
        st.write("时间数据列名：", time_data.columns)
        
        return time_data
    return None

# 计算瞬时速度
def calculate_instantaneous_speed(position_data, time_data, frame):
    # 查询位置数据和时间数据对应帧的数据
    position_frame_data = position_data[position_data['Frame'] == frame]
    time_frame_data = time_data[time_data['Frame'] == frame]

    if position_frame_data.empty or time_frame_data.empty:
        return None  # 如果该帧的数据不存在
    
    # 提取位置和时间数据
    x, y, z = position_frame_data['X'].values[0], position_frame_data['Y'].values[0], position_frame_data['Z'].values[0]
    
    # 获取时间数据，列名为 'time'
    if 'time' not in time_data.columns:
        st.error("时间数据中没有找到 'time' 列，请检查数据格式。")
        return None

    time = time_frame_data['time'].values[0]
    
    # 计算瞬时速度（假设每帧之间的时间间隔为常数）
    speed = np.sqrt(x**2 + y**2 + z**2) / time if time != 0 else 0
    
    return speed

# 主函数
def main():
    st.title("🐑❤️‍🔥🌃（瞬时速度计算）")

    # 加载位置数据和时间数据
    position_data = load_position_data()
    time_data = load_time_data()

    if position_data is not None and time_data is not None:
        st.write("位置数据预览：")
        st.write(position_data.head())

        st.write("时间数据预览：")
        st.write(time_data.head())

        # 输入查询的 Frame
        frame = st.number_input("请输入查询的帧（Frame）：", min_value=1, max_value=len(position_data), value=1)

        if st.button("计算瞬时速度"):
            instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)
            if instantaneous_speed is not None:
                st.write(f"帧 {frame} 的瞬时速度为: {instantaneous_speed:.6f} 米/秒")
            else:
                st.write("该帧的数据不存在。")

if __name__ == '__main__':
    main()
