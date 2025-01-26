# 倒推计算角加速度与角速度
def calculate_angular_acceleration_and_velocity(torque, mass, radius, angle, linear_velocity, delta_time):
    inertia = calculate_inertia(mass, radius)  # 计算转动惯量
    angular_acceleration = calculate_joint_angular_acceleration(torque, inertia)  # 计算角加速度
    if angular_acceleration is not None:
        angular_velocity = calculate_joint_angular_velocity(angular_acceleration, angle, delta_time)  # 根据角加速度计算角速度
        return angular_acceleration, angular_velocity
    else:
        return None, None

# 功能2：倒推角加速度与角速度计算
def calculate_angular_speed_and_acceleration():
    st.title("🌀 计算倒推的角加速度与角速度")

    # 输入 x, y, z 轴的数据
    torque_x = st.number_input("请输入关节力矩 (x轴 N·m)：", value=0.0)
    torque_y = st.number_input("请输入关节力矩 (y轴 N·m)：", value=0.0)
    torque_z = st.number_input("请输入关节力矩 (z轴 N·m)：", value=0.0)

    linear_velocity_x = st.number_input("请输入关节线速度 (x轴 m/s)：", value=0.0)
    linear_velocity_y = st.number_input("请输入关节线速度 (y轴 m/s)：", value=0.0)
    linear_velocity_z = st.number_input("请输入关节线速度 (z轴 m/s)：", value=0.0)

    mass = st.number_input("请输入物体质量 (kg)：", value=1.0)
    angle_x = st.number_input("请输入关节角度 (x轴 rad)：", value=0.0)
    angle_y = st.number_input("请输入关节角度 (y轴 rad)：", value=0.0)
    angle_z = st.number_input("请输入关节角度 (z轴 rad)：", value=0.0)

    delta_time = st.number_input("请输入时间间隔 (秒)：", value=1.0)

    if st.button("计算倒推的角加速度与角速度"):
        # 将输入的x, y, z轴合并为向量
        torque = np.array([torque_x, torque_y, torque_z])
        linear_velocity = np.array([linear_velocity_x, linear_velocity_y, linear_velocity_z])
        angle = np.array([angle_x, angle_y, angle_z])

        # 假设转动惯量半径为1
        radius = 1.0
        angular_acceleration, angular_velocity = calculate_angular_acceleration_and_velocity(
            torque, mass, radius, angle, linear_velocity, delta_time
        )
        
        if angular_acceleration is not None and angular_velocity is not None:
            # 确保角加速度是一个数值类型再输出
            if isinstance(angular_acceleration, (int, float)):
                st.write(f"角加速度为: {angular_acceleration:.6f} rad/s²")
            else:
                st.write("角加速度的计算结果无效。")
            
            # 确保角速度是一个数值类型再输出
            if isinstance(angular_velocity, (int, float)):
                st.write(f"角速度为: {angular_velocity:.6f} rad/s")
            else:
                st.write("角速度的计算结果无效。")
        else:
            st.write("无法计算角加速度或角速度。")

