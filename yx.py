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

# 计算关节角加速度
def calculate_joint_angular_acceleration(torque, inertia):
    if inertia != 0:
        return torque / inertia
    else:
        return None

# 计算关节角速度
def calculate_joint_angular_velocity(angular_acceleration, initial_angular_velocity=0, delta_time=1):
    return initial_angular_velocity + angular_acceleration * delta_time

# 计算关节转动惯量（通过物体质量和半径）
def calculate_inertia(mass, radius):
    return mass * radius**2

# 倒推计算角加速度与角速度
def calculate_angular_acceleration_and_velocity(torque, mass, radius, angle, linear_velocity, delta_time):
    inertia = calculate_inertia(mass, radius)  # 计算转动惯量
    angular_acceleration = calculate_joint_angular_acceleration(torque, inertia)  # 计算角加速度
    
    if angular_acceleration is not None:
        angular_velocity = calculate_joint_angular_velocity(angular_acceleration, angle, delta_time)  # 根据角加速度计算角速度
        return angular_acceleration, angular_velocity
    else:
        return None, None

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

        # 计算瞬时速度
        st.header("🔎 计算瞬时速度")
        frame = st.number_input("高抬贵手🤸下请您输入查询的帧（Frame）：", min_value=1, max_value=len(position_data), value=1)
        if st.button("👅你真棒！终于计算出了瞬时速度💖~"):
            instantaneous_speed = calculate_instantaneous_speed(position_data, time_data, frame)
            if instantaneous_speed is not None:
                st.write(f"帧 {frame} 的瞬时速度为: {instantaneous_speed:.6f} 米/秒")
            else:
                st.write("该帧的数据不存在。")

        # 计算帧范围内的平均速度和位移
        st.header("📈 计算平均速度与位移")
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

        # 计算倒推的角加速度与角速度
        st.header("🌀 计算倒推的角加速度与角速度")
        torque = st.number_input("请输入关节力矩 (N·m)：", value=0.0)
        linear_velocity = st.number_input("请输入关节线速度 (m/s)：", value=0.0)
        mass = st.number_input("请输入物体质量 (kg)：", value=1.0)
        angle = st.number_input("请输入关节角度 (rad)：", value=0.0)
        delta_time = st.number_input("请输入时间间隔 (秒)：", value=1.0)

        if st.button("计算倒推的角加速度与角速度"):
            angular_acceleration, angular_velocity = calculate_angular_acceleration_and_velocity(
                torque, mass, radius=1.0, angle=angle, linear_velocity=linear_velocity, delta_time=delta_time
            )
            if angular_acceleration is not None and angular_velocity is not None:
                st.write(f"角加速度为: {angular_acceleration:.6f} rad/s²")
                st.write(f"角速度为: {angular_velocity:.6f} rad/s")
            else:
                st.write("无法计算角加速度或角速度。")

if __name__ == '__main__':
    main()

