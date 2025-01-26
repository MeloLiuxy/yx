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

# 计算关节角速度
def calculate_joint_angular_velocity(joint_angles, time_data):
    angular_velocities = []
    for i in range(1, len(joint_angles)):
        delta_angle = joint_angles[i] - joint_angles[i-1]
        delta_time = time_data[i] - time_data[i-1]
        angular_velocity = delta_angle / delta_time if delta_time != 0 else 0
        angular_velocities.append(angular_velocity)
    return np.array(angular_velocities)

# 计算关节角加速度
def calculate_joint_angular_acceleration(angular_velocities, time_data):
    angular_accelerations = []
    for i in range(1, len(angular_velocities)):
        delta_angular_velocity = angular_velocities[i] - angular_velocities[i-1]
        delta_time = time_data[i] - time_data[i-1]
        angular_acceleration = delta_angular_velocity / delta_time if delta_time != 0 else 0
        angular_accelerations.append(angular_acceleration)
    return np.array(angular_accelerations)

# 主函数 - 速度与位移计算
def main_position_speed():
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
            instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)
            if instantaneous_speed is not None:
                st.write(f"帧 {frame} 的瞬时速度为: {instantaneous_speed:.6f} 米/秒")
            else:
                st.write("该帧的数据不存在。")

        # 计算帧范围内的平均速度和位移
        start_frame = st.number_input("请输入起始帧：", min_value=1, max_value=len(position_data), value=1)
        end_frame = st.number_input("请输入结束帧：", min_value=1, max_value=len(position_data), value=len(position_data))

        if st.button("😃计算选定帧范围的平均速度与位移🧮"):
            if start_frame <= end_frame:
                avg_speed = calculate_average_speed(position_data, time_data, start_frame, end_frame)
                displacement = calculate_displacement(position_data, start_frame, end_frame)

                if avg_speed is not None and displacement is not None:
                    st.write(f"帧 {start_frame} 到 {end_frame} 的平均速度为: {avg_speed:.6f} 米/秒")
                    st.write(f"帧 {start_frame} 到 {end_frame} 的位移为: {displacement:.6f} 米")
                else:
                    st.write("选定帧范围内的数据不存在。")
            else:
                st.error("起始帧必须小于等于结束帧，请重新输入。")

# 主函数 - 关节角度、角速度和角加速度计算
def main_joint_kinematics():
    st.title("💪关节角速度与加速度计算工具")

    # 上传时间数据
    time_data = load_time_data()
    
    if time_data is not None:
        # 关节角度输入
        joint_angles = st.text_area("请输入关节角度数据（以逗号分隔）：", value="0, 10, 20, 30")
        joint_angles = np.array([float(angle) for angle in joint_angles.split(',')])

        # 计算关节角速度和角加速度
        if len(joint_angles) > 1:
            angular_velocities = calculate_joint_angular_velocity(joint_angles, time_data['time'])
            angular_accelerations = calculate_joint_angular_acceleration(angular_velocities, time_data['time'])

            st.write("计算出的关节角速度：", angular_velocities)
            st.write("计算出的关节角加速度：", angular_accelerations)

if __name__ == '__main__':
    mode = st.radio("请选择功能模块", ("速度与位移计算", "关节角速度与加速度计算"))
    
    if mode == "速度与位移计算":
        main_position_speed()
    else:
        main_joint_kinematics()

