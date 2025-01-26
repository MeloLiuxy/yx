import streamlit as st

# 计算关节转动惯量（通过物体质量和半径）
def calculate_inertia(mass, radius):
    return mass * radius**2

# 计算关节角加速度
def calculate_joint_angular_acceleration(torque, inertia):
    if inertia != 0:
        return torque / inertia
    else:
        return None

# 计算关节角速度
def calculate_joint_angular_velocity(angular_acceleration, initial_angular_velocity=0, delta_time=1):
    return initial_angular_velocity + angular_acceleration * delta_time

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
def main_angular_acceleration_velocity():
    st.title("💓角加速度与角速度计算工具")

    # 输入参数
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
    main_angular_acceleration_velocity()

