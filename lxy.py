import streamlit as st
import pandas as pd
import numpy as np

# 上传角度数据并读取
def load_angle_data():
    uploaded_angle_file = st.file_uploader("请上传您的角度数据文件（含X、Y、Z三列）", type=["xlsx", "csv"])
    if uploaded_angle_file is not None:
        angle_data = pd.read_excel(uploaded_angle_file) if uploaded_angle_file.name.endswith('.xlsx') else pd.read_csv(uploaded_angle_file)
        angle_data.columns = angle_data.columns.str.strip()  # 清理列名中的多余空格
        return angle_data
    return None

# 计算合角度
def calculate_combined_angle(x, y, z):
    # 计算合角度 (示例: 使用 atan2 和 sqrt 计算)
    return np.degrees(np.arctan2(np.sqrt(x**2 + y**2), z))

# 计算某个帧范围内的最大最小角度和对应的帧号
def calculate_max_min_angle_in_range(angle_data, start_frame, end_frame):
    angles = []
    frames = []

    # 获取指定帧范围内的角度数据
    for index, row in angle_data.iterrows():
        if start_frame <= row['Frame'] <= end_frame:
            x, y, z = row['X'], row['Y'], row['Z']
            angle = calculate_combined_angle(x, y, z)
            angles.append(angle)
            frames.append(row['Frame'])
    
    if angles:
        max_angle = max(angles)
        min_angle = min(angles)
        max_angle_frame = frames[angles.index(max_angle)]  # 获取最大角度对应的帧号
        min_angle_frame = frames[angles.index(min_angle)]  # 获取最小角度对应的帧号
        return max_angle, max_angle_frame, min_angle, min_angle_frame
    else:
        return None, None, None, None

# 计算某个帧的角度
def get_angle_for_frame(angle_data, frame):
    angle_frame_data = angle_data[angle_data['Frame'] == frame]
    if not angle_frame_data.empty:
        x, y, z = angle_frame_data[['X', 'Y', 'Z']].values[0]
        return calculate_combined_angle(x, y, z)
    return None

# 主函数
def main():
    st.title("角度计算工具")

    # 加载角度数据
    angle_data = load_angle_data()

    if angle_data is not None:
        st.write("📉看一眼您的角度数据预览：")
        st.write(angle_data.head())

        # 输入帧范围并计算角度的最大最小值
        st.subheader("请输入计算角度的帧范围：")
        start_frame = st.number_input("请输入起始帧：", min_value=1, max_value=len(angle_data), value=1)
        end_frame = st.number_input("请输入结束帧：", min_value=1, max_value=len(angle_data), value=len(angle_data))

        if st.button("🧑‍🏫计算选定帧范围的最大最小角度"):
            if start_frame <= end_frame:
                max_angle, max_angle_frame, min_angle, min_angle_frame = calculate_max_min_angle_in_range(angle_data, start_frame, end_frame)
                if max_angle is not None and min_angle is not None:
                    st.write(f"帧 {start_frame} 到 {end_frame} 范围内的最大角度为: {max_angle:.2f}° (对应帧号: {max_angle_frame})")
                    st.write(f"帧 {start_frame} 到 {end_frame} 范围内的最小角度为: {min_angle:.2f}° (对应帧号: {min_angle_frame})")
                else:
                    st.write("该帧范围内没有角度数据。")
            else:
                st.error("起始帧必须小于等于结束帧，请重新输入。")

        # 输入帧并计算角度
        st.subheader("请输入查询角度的帧：")
        frame = st.number_input("请输入查询的帧（Frame）以查看角度：", min_value=1, max_value=len(angle_data), value=1)
        if st.button("🧑‍🏫计算指定帧的角度"):
            angle = get_angle_for_frame(angle_data, frame)
            if angle is not None:
                st.write(f"帧 {frame} 的合角度为: {angle:.2f}°")
            else:
                st.write("该帧的角度数据不存在。")

if __name__ == '__main__':
    main()

