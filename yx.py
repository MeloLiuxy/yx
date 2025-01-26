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

# 计算旋转轴长度
def calculate_axis_length(linear_velocity, angular_velocity):
    if angular_velocity != 0:
        return linear_velocity / angular_velocity
    else:
        return None

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

        # 计算关节角加速度、角速度和旋转轴长度
        st.write("请输入相关参数计算关节角加速度、关节角速度和旋转轴长度：")
        
        torque = st.number_input("请输入关节力矩 (N·m)：", value=0.0)
        inertia = st.number_input("请输入关节转动惯量 (kg·m²)：", value=1.0)
        angular_velocity_initial = st.number_input("请输入初始关节角速度 (rad/s)：", value=0.0)
        delta_time = st.number_input("请输入时间间隔 (秒)：", value=1.0)
        linear_velocity = st.number_input("请输入关节线速度 (m/s)：", value=0.0)
        
        if st.button("计算关节角加速度、角速度和旋转轴长度"):
            # 计算角加速度
            angular_acceleration = calculate_joint_angular_acceleration(torque, inertia)
            if angular_acceleration is not None:
                st.write(f"关节的角加速度为: {angular_acceleration:.6f} rad/s²")
                
                # 计算角速度
                angular_velocity = calculate_joint_angular_velocity(angular_acceleration, angular_velocity_initial, delta_time)
                st.write(f"关节的角速度为: {angular_velocity:.6f} rad/s")
                
                # 计算旋转轴长度
                axis_length = calculate_axis_length(linear_velocity, angular_velocity)
                if axis_length is not None:
                    st.write(f"旋转轴长度为: {axis_length:.6f} 米")
                else:
                    st.write("无法计算旋转轴长度，可能是角速度为零。")
            else:
                st.write("无法计算角加速度，可能是转动惯量为零。")

if __name__ == '__main__':
    main()
