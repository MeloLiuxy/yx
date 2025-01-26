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

# 计算最大和最小角度
def calculate_max_min_angle(angle_data):
    angles = []
    for index, row in angle_data.iterrows():
        x, y, z = row['X'], row['Y'], row['Z']
        angle = calculate_combined_angle(x, y, z)
        angles.append(angle)
    
    max_angle = max(angles)
    min_angle = min(angles)
    
    return max_angle, min_angle, angles

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

        # 计算角度的最大最小值
        max_angle, min_angle, angles = calculate_max_min_angle(angle_data)
        st.write(f"最大角度: {max_angle:.2f}°")
        st.write(f"最小角度: {min_angle:.2f}°")

        # 输入帧并计算角度
        frame = st.number_input("请输入查询的帧（Frame）以查看角度：", min_value=1, max_value=len(angle_data), value=1)
        if st.button("🧑‍🏫计算指定帧的角度"):
            angle = get_angle_for_frame(angle_data, frame)
            if angle is not None:
                st.write(f"帧 {frame} 的合角度为: {angle:.2f}°")
            else:
                st.write("该帧的角度数据不存在。")

if __name__ == '__main__':
    main()
