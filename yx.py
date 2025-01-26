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
def calculate_joint_angular_velocity(angular_acceleration, initial_angular_velocity=0, delta_time=1):
    return initial_angular_velocity + angular_acceleration * delta_time

# 计算关节角加速度
def calculate_joint_angular_acceleration(torque, inertia):
    if inertia != 0:
        return torque / inertia
    else:
        return None

# 计算转动惯量（倒推计算）
def calculate_inertia_from_torque_and_acceleration(torque, angular_acceleration):
    if angular_acceleration != 0:
        return torque / angular_acceleration
    else:
        return None

# 倒推计算角加速度与角速度
def calculate_angular_acceleration_and_velocity(torque_x, torque_y, torque_z, mass, angle_x, angle_y, angle_z, linear_velocity_x, linear_velocity_y, linear_velocity_z, delta_time, joint_acceleration_x, joint_acceleration_y, joint_acceleration_z):
    # 使用输入的关节加速度倒推计算转动惯量
    inertia_x = calculate_inertia_from_torque_and_acceleration(torque_x, joint_acceleration_x)
    inertia_y = calculate_inertia_from_torque_and_acceleration(torque_y, joint_acceleration_y)
    inertia_z = calculate_inertia_from_torque_and_acceleration(torque_z, joint_acceleration_z)

    if None in [inertia_x, inertia_y, inertia_z]:
        return None, None, None, None, None, None

    # 计算每个方向的角速度
    angular_velocity_x = calculate_joint_angular_velocity(joint_acceleration_x, angle_x, delta_time)
    angular_velocity_y = calculate_joint_angular_velocity(joint_acceleration_y, angle_y, delta_time)
    angular_velocity_z = calculate_joint_angular_velocity(joint_acceleration_z, angle_z, delta_time)

    # 合成角加速度和角速度
    total_angular_acceleration = np.sqrt(joint_acceleration_x**2 + joint_acceleration_y**2 + joint_acceleration_z**2)
    total_angular_velocity = np.sqrt(angular_velocity_x**2 + angular_velocity_y**2 + angular_velocity_z**2)

    return total_angular_acceleration, total_angular_velocity, inertia_x, inertia_y, inertia_z

# 主函数 - 关节角度、角速度和角加速度计算
def main_joint_kinematics():
    st.title("💪关节角速度与加速度计算工具")

    # 手动输入数据
    torque_x = st.number_input("请输入关节力矩 x (N·m)：", value=0.0)
    torque_y = st.number_input("请输入关节力矩 y (N·m)：", value=0.0)
    torque_z = st.number_input("请输入关节力矩 z (N·m)：", value=0.0)

    linear_velocity_x = st.number_input("请输入关节线速度 x (m/s)：", value=0.0)
    linear_velocity_y = st.number_input("请输入关节线速度 y (m/s)：", value=0.0)
    linear_velocity_z = st.number_input("请输入关节线速度 z (m/s)：", value=0.0)

    mass = st.number_input("请输入物体质量 (kg)：", value=1.0)  # 输入统一质量值

    angle_x = st.number_input("请输入关节角度 x (rad)：", value=0.0)
    angle_y = st.number_input("请输入关节角度 y (rad)：", value=0.0)
    angle_z = st.number_input("请输入关节角度 z (rad)：", value=0.0)

    delta_time = st.number_input("请输入时间间隔 (秒)：", value=1.0)

    # 输入关节加速度，分别为x、y、z方向
    joint_acceleration_x = st.number_input("请输入关节加速度 x (rad/s²)：", value=0.0)
    joint_acceleration_y = st.number_input("请输入关节加速度 y (rad/s²)：", value=0.0)
    joint_acceleration_z = st.number_input("请输入关节加速度 z (rad/s²)：", value=0.0)

    if st.button("计算关节合成角速度与角加速度"):
        # 调用计算函数
        total_angular_acceleration, total_angular_velocity, inertia_x, inertia_y, inertia_z = calculate_angular_acceleration_and_velocity(
            torque_x, torque_y, torque_z, mass, angle_x, angle_y, angle_z,
            linear_velocity_x=linear_velocity_x, linear_velocity_y=linear_velocity_y, linear_velocity_z=linear_velocity_z,
            delta_time=delta_time, joint_acceleration_x=joint_acceleration_x, joint_acceleration_y=joint_acceleration_y, joint_acceleration_z=joint_acceleration_z
        )

        if total_angular_acceleration is not None:
            # 输出计算的结果
            st.write(f"关节合成角加速度为: {total_angular_acceleration:.6f} rad/s²")
            st.write(f"关节合成角速度为: {total_angular_velocity:.6f} rad/s")
            st.write(f"关节 x 方向的转动惯量为: {inertia_x:.6f} kg·m²")
            st.write(f"关节 y 方向的转动惯量为: {inertia_y:.6f} kg·m²")
            st.write(f"关节 z 方向的转动惯量为: {inertia_z:.6f} kg·m²")
        else:
            st.write("无法计算转动惯量，可能是因为角加速度为零。")

if __name__ == '__main__':
    mode = st.radio("请选择功能模块", ("关节角速度与加速度计算", "其他模块"))

    if mode == "关节角速度与加速度计算":
        main_joint_kinematics()
    elif mode == "其他模块":
        st.write("您选择了其他模块。") 

