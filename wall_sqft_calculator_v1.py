import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

def calculate_wall_area(length_ft, width_ft, height_ft, num_windows=0, window_w=0, window_h=0,
                        num_doors=0, door_w=0, door_h=0):
    total_wall_area = 2 * (length_ft + width_ft) * height_ft
    window_area = num_windows * (window_w * window_h)
    door_area = num_doors * (door_w * door_h)
    net_wall_area = total_wall_area - (window_area + door_area)
    return max(net_wall_area, 0)

def calculate_linear_trim(length_ft, width_ft, include_baseboard, include_frames):
    perimeter = 2 * (length_ft + width_ft)
    baseboard = perimeter if include_baseboard else 0
    frames = 0
    if include_frames:
        frames = num_windows * (2 * window_w + 2 * window_h) + num_doors * (2 * door_w + 2 * door_h)
    return baseboard + frames

def calculate_ceiling_area(length_ft, width_ft, include_ceiling):
    return length_ft * width_ft if include_ceiling else 0

st.title("🧮 Wall Square Footage Calculator")
st.markdown("Estimate the total paintable wall area in a room.")

with st.form("wall_form"):
    st.subheader("Room Dimensions")
    length = st.number_input("Room length (ft)", min_value=0.0, value=12.0, step=0.5)
    width = st.number_input("Room width (ft)", min_value=0.0, value=10.0, step=0.5)
    height = st.number_input("Ceiling height (ft)", min_value=0.0, value=8.0, step=0.5)

    st.subheader("Windows")
    num_windows = st.number_input("Number of windows", min_value=0, value=0, step=1)
    window_w = st.number_input("Window width (ft)", min_value=0.0, value=3.0, step=0.5) if num_windows > 0 else 0
    window_h = st.number_input("Window height (ft)", min_value=0.0, value=4.0, step=0.5) if num_windows > 0 else 0

    st.subheader("Doors")
    num_doors = st.number_input("Number of doors", min_value=0, value=0, step=1)
    door_w = st.number_input("Door width (ft)", min_value=0.0, value=3.0, step=0.5) if num_doors > 0 else 0
    door_h = st.number_input("Door height (ft)", min_value=0.0, value=7.0, step=0.5) if num_doors > 0 else 0

    st.subheader("Additional Options")
    include_baseboard = st.checkbox("Include baseboards in linear footage", value=True)
    include_frames = st.checkbox("Include window and door casings in linear footage", value=True)
    include_ceiling = st.checkbox("Include ceiling square footage", value=False)

    submitted = st.form_submit_button("Calculate")

if submitted:
    sqft = calculate_wall_area(length, width, height, num_windows, window_w, window_h,
                               num_doors, door_w, door_h)
    linear_trim = calculate_linear_trim(length, width, include_baseboard, include_frames)
    ceiling_area = calculate_ceiling_area(length, width, include_ceiling)

    st.success(f"Estimated wall square footage: {sqft:.2f} sq ft")
    if include_baseboard or include_frames:
        st.info(f"Estimated linear trim (baseboards + casings): {linear_trim:.2f} ft")
    if include_ceiling:
        st.info(f"Estimated ceiling area: {ceiling_area:.2f} sq ft")

st.subheader("📸 Optional: Upload a Room Photo")
uploaded_file = st.file_uploader("Upload a photo of the room (optional)", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Room Photo", use_column_width=True)

    st.subheader("Edge Detection Preview")
    img_array = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    st.image(edges_rgb, caption="Detected Edges (for future dimension analysis)", use_column_width=True)
    st.info("Edges show detected shapes and outlines. In a future version, this can help estimate room features.")