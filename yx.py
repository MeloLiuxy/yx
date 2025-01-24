import streamlit as st
import pandas as pd
import numpy as np

# 设置页面布局与标题图片
st.set_page_config(page_title="运动数据分析工具", page_icon="🏃‍♂️", layout="centered")

# 在页面顶部添加一张照片
st.image("C:\Users\LXY\Desktop\5a17cddf727b55b635db0f650aa8f3d.jpg", use_column_width=True)
st.title("💓🐑🌃（🥋lxy辛苦了！）")

# 上传位置数据并读取
def load_position_data():
    uploaded_position_file = st.file_uploader("📂 请选择您的位置数据文件：", type=["xlsx", "csv"])
    if uploaded_position_file is not None:
        position_data = pd.read_excel(uploaded_position_file) if uploaded_position_file.name.endswith('.xlsx') else pd.read_csv(uploaded_position_file)
        position_data.columns = position_data.columns.str.strip()  # 清理列名中的多余空格
        return position_data
    return None

# 上传时间数据并读取
def load_time_data():
    uploaded_time_file = st.file_uploader("⏱️ 请上传您的时间数据文件：", type=["xlsx", "csv"])
    if uploaded_time_file is not None:
        time_data = pd.read_excel(uploaded_time_file) if uploaded_time_file.name.endswith('.xlsx') else pd.read_csv(uploaded_time_file)
        time_data.columns = time_data.columns.str.strip()
        st.write("👀 时间数据列名：", time_data.columns)
        return time_data
    return None

# 计算瞬时速度
def calculate_instantaneous_speed(position_data, time_data, frame):
    position_frame_data = position_data[position_data['Frame'] == frame]
    time_frame_data = time_data[time_data['Frame'] == frame]

    if position_frame_data.empty or time_frame_data.empty:
        return None  

    x, y, z = position_frame_data['X'].values[0], position_frame_data['Y'].values[0], position_frame_data['Z'].values[0]

    if 'time' not in time_data.columns:
        st.error("时间数据中没有找到 'time' 列，请检查数据格式。")
        return None

    time = time_frame_data['time'].values[0]
    speed = np.sqrt(x**2 + y**2 + z**2) / time if time != 0 else 0
    
    return speed

# 计算帧范围内的平均速度
def calculate_average_speed(position_data, time_data, start_frame, end_frame):
    total_speed = 0
    count = 0

    for frame in range(start_frame, end_frame + 1):
        speed = calculate_instantaneous_speed(position_data, time_data, frame)
        if speed is not None:
            total_speed += speed
            count += 1
    
    return total_speed / count if count > 0 else None

# 计算帧范围内的位移
def calculate_displacement(position_data, start_frame, end_frame):
    start_pos = position_data[position_data['Frame'] == start_frame]
    end_pos = position_data[position_data['Frame'] == end_frame]

    if start_pos.empty or end_pos.empty:
        return None  

    x1, y1, z1 = start_pos['X'].values[0], start_pos['Y'].values[0], start_pos['Z'].values[0]
    x2, y2, z2 = end_pos['X'].values[0], end_pos['Y'].values[0], end_pos['Z'].values[0]

    displacement = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    return displacement

# 主函数
def main():
    st.sidebar.image("sidebar.jpg", use_column_width=True)  # 添加侧边栏图片
    st.sidebar.header("📊 数据分析菜单")
    
    position_data = load_position_data()
    time_data = load_time_data()

    if position_data is not None and time_data is not None:
        st.success("✅ 数据加载成功！")

        # 展示数据
        if st.checkbox("👀 显示位置数据预览"):
            st.write(position_data.head())

        if st.checkbox("👀 显示时间数据预览"):
            st.write(time_data.head())

        # 单帧速度计算
        frame = st.number_input("📍 请输入要计算瞬时速度的帧（Frame）：", min_value=1, max_value=len(position_data), value=1)
        if st.button("🔍 计算瞬时速度"):
            instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)
            if instantaneous_speed is not None:
                st.success(f"帧 {frame} 的瞬时速度为: {instantaneous_speed:.6f} 米/秒")
            else:
                st.error("该帧的数据不存在，请检查输入。")

        # 计算帧范围的平均速度和位移
        st.subheader("📈 计算帧范围的速度与位移")
        start_frame = st.number_input("🏁 起始帧：", min_value=1, max_value=len(position_data), value=1)
        end_frame = st.number_input("🏁 结束帧：", min_value=1, max_value=len(position_data), value=len(position_data))

        if st.button("⚙️ 计算平均速度与位移"):
            if start_frame <= end_frame:
                avg_speed = calculate_average_speed(position_data, time_data, start_frame, end_frame)
                displacement = calculate_displacement(position_data, start_frame, end_frame)

                if avg_speed is not None and displacement is not None:
                    st.info(f"帧 {start_frame} 到 {end_frame} 的平均速度为: {avg_speed:.6f} 米/秒")
                    st.info(f"帧 {start_frame} 到 {end_frame} 的位移为: {displacement:.6f} 米")
                else:
                    st.warning("选定帧范围内的数据可能不存在，请检查输入范围。")
            else:
                st.error("起始帧必须小于等于结束帧，请重新输入。")

if __name__ == '__main__':
    main()
