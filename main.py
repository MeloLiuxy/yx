import streamlit as st
import pandas as pd
import numpy as np

# 上传位置数据并读取
def load_position_data():
    uploaded_position_file = st.file_uploader("请美女😋宵上传您的位置数据文件", type=["xlsx", "csv"])
    if uploaded_position_file is not None:
        position_data = pd.read_excel(uploaded_position_file) if uploaded_position_file.name.endswith('.xlsx') else pd.read_csv(uploaded_position_file)
        position_data.columns = position_data.columns.str.strip()
        return position_data
    return None

# 上传时间数据并读取
def load_time_data():
    uploaded_time_file = st.file_uploader("😻辛苦您上传您的时间⏱️数据文件", type=["xlsx", "csv"])
    if uploaded_time_file is not None:
        time_data = pd.read_excel(uploaded_time_file) if uploaded_time_file.name.endswith('.xlsx') else pd.read_csv(uploaded_time_file)
        time_data.columns = time_data.columns.str.strip()
        st.write("辛苦您的眼睛了🫡，看一眼时间数据列名：", time_data.columns)
        return time_data
    return None

# 计算瞬时速度（xyz方向）
def calculate_instantaneous_speed(position_data, time_data, frame):
    position_frame_data = position_data[position_data['Frame'] == frame]
    time_frame_data = time_data[time_data['Frame'] == frame]

    if position_frame_data.empty or time_frame_data.empty:
        return None, None, None, None  # 返回空值以便显示错误

    # 获取当前帧的位置数据
    x, y, z = position_frame_data['X'].values[0], position_frame_data['Y'].values[0], position_frame_data['Z'].values[0]
    
    # 获取时间数据
    if 'time' not in time_data.columns:
        st.error("时间数据中没有找到 'time' 列，请检查数据格式。")
        return None, None, None, None

    time = time_frame_data['time'].values[0]

    # 计算x、y、z方向的瞬时速度
    # 注意：瞬时速度是位移/时间差，这里简单处理为当前帧的坐标值除以时间
    speed_x = x / time if time != 0 else 0
    speed_y = y / time if time != 0 else 0
    speed_z = z / time if time != 0 else 0
    
    return speed_x, speed_y, speed_z, np.sqrt(speed_x**2 + speed_y**2 + speed_z**2)

def calculate_average_speed(position_data, time_data, start_frame, end_frame):
    total_distance = 0  # 累计总位移
    total_time = 0  # 累计总时间
    count = 0

    for frame in range(start_frame, end_frame + 1):
        speed_x, speed_y, speed_z, instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)
        if speed_x is not None:
            # 累计位移
            total_distance += instantaneous_speed  # 计算总位移

            # 累计时间
            time_frame_data = time_data[time_data['Frame'] == frame]
            if not time_frame_data.empty:
                total_time += time_frame_data['time'].values[0]  # 累计时间

            count += 1
    
    # 计算平均速度（总位移除以总时间）
    avg_speed = total_distance / total_time if total_time > 0 else None
    
    # 分别计算x、y、z方向的平均速度
    avg_speed_x = total_distance / count if count > 0 else None
    avg_speed_y = total_distance / count if count > 0 else None
    avg_speed_z = total_distance / count if count > 0 else None
    
    return avg_speed_x, avg_speed_y, avg_speed_z, avg_speed


# 计算帧范围内的位移
def calculate_displacement(position_data, start_frame, end_frame):
    start_pos = position_data[position_data['Frame'] == start_frame]
    end_pos = position_data[position_data['Frame'] == end_frame]

    if start_pos.empty or end_pos.empty:
        return None, None, None, None  # 返回空值以便显示错误

    x1, y1, z1 = start_pos['X'].values[0], start_pos['Y'].values[0], start_pos['Z'].values[0]
    x2, y2, z2 = end_pos['X'].values[0], end_pos['Y'].values[0], end_pos['Z'].values[0]

    displacement = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    # 位移的 x、y、z 分量
    displacement_x = x2 - x1
    displacement_y = y2 - y1
    displacement_z = z2 - z1
    
    return displacement, displacement_x, displacement_y, displacement_z

# 主函数
def main():
    st.title("💓🐑🌃（🥋速度与位移计算工具）")

    # 加载位置数据和时间数据
    position_data = load_position_data()
    time_data = load_time_data()

    if position_data is not None and time_data is not None:
        st.write("🐯再辛苦您一下，看一眼🙈位置数据预览：")
        st.write(position_data.head())

        st.write("👭最后看一眼时间数据预览：")
        st.write(time_data.head())

        # 计算单帧瞬时速度
        frame = st.number_input("高抬贵手🤸下请您输入查询的帧（Frame）：", min_value=1, max_value=len(position_data), value=1)
        if st.button("👅你真棒！终于计算出了瞬时速度💖~"):
            speed_x, speed_y, speed_z, instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)
            if instantaneous_speed is not None:
                st.write(f"帧 {frame} 的瞬时速度：")
                st.write(f"X方向速度: {speed_x:.6f} 米/秒")
                st.write(f"Y方向速度: {speed_y:.6f} 米/秒")
                st.write(f"Z方向速度: {speed_z:.6f} 米/秒")
                st.write(f"总瞬时速度: {instantaneous_speed:.6f} 米/秒")
            else:
                st.write("该帧的数据不存在。")

        # 计算帧范围内的平均速度及总速度
        start_frame = st.number_input("请输入起始帧：", min_value=1, max_value=len(position_data), value=1)
        end_frame = st.number_input("请输入结束帧：", min_value=1, max_value=len(position_data), value=len(position_data))

        if st.button("😃计算选定帧范围的平均速度🧮"):
            if start_frame <= end_frame:
                avg_speed_x, avg_speed_y, avg_speed_z, avg_total_speed = calculate_average_speed(position_data, time_data, start_frame, end_frame)
                displacement, disp_x, disp_y, disp_z = calculate_displacement(position_data, start_frame, end_frame)

                if avg_speed_x is not None and displacement is not None:
                    st.write(f"帧 {start_frame} 到 {end_frame} 的平均速度：")
                    st.write(f"X方向平均速度: {avg_speed_x:.6f} 米/秒")
                    st.write(f"Y方向平均速度: {avg_speed_y:.6f} 米/秒")
                    st.write(f"Z方向平均速度: {avg_speed_z:.6f} 米/秒")
                    st.write(f"总平均速度: {avg_total_speed:.6f} 米/秒")  # 显示总平均速度
                    st.write(f"帧 {start_frame} 到 {end_frame} 的位移为: {displacement:.6f} 米")
                    st.write(f"位移分量：X={disp_x}, Y={disp_y}, Z={disp_z}")
                else:
                    st.write("选定帧范围内的数据不存在。")
            else:
                st.error("起始帧必须小于等于结束帧，请重新输入。")

if __name__ == '__main__':
    main()
