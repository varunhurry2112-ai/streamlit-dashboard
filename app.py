import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Paradis Beachcomber Rooms Dashboard", layout="wide")

# ===============================
# TITLE
# ===============================
st.title("🏨 Paradis Beachcomber Rooms Dashboard")

# ===============================
# VIEW SELECTOR
# ===============================
view = st.radio("Select View", ["GMR", "GSS"], horizontal=True)

if view == "GSS":
    st.warning("GSS view will be configured later.")
    st.stop()

# ===============================
# FILE UPLOADERS
# ===============================
gmr_file = st.file_uploader("Upload GMR Excel File", type=["xlsx"])
room_plan_file = st.file_uploader("Upload Room Plan Excel File", type=["xlsx"])

if not gmr_file or not room_plan_file:
    st.info("Please upload BOTH GMR file and Room Plan file.")
    st.stop()

# ===============================
# LOAD ROOM PLAN (EXACT VALUES)
# ===============================
room_plan_df = pd.read_excel(room_plan_file, header=None)

rooms = (
    room_plan_df
    .values
    .astype(str)
    .flatten()
)

rooms = [r.strip() for r in rooms if r.strip().lower() not in ["nan", ""]]

# ===============================
# LOAD GMR FILE
# ===============================
gmr_excel = pd.ExcelFile(gmr_file)

selected_day = st.selectbox("Select Day (Sheet)", gmr_excel.sheet_names)

gmr_df = pd.read_excel(gmr_excel, sheet_name=selected_day)

# ===============================
# STATUS COLUMN DETECTION
# ===============================
room_col = "RM"

status_col = None
for col in gmr_df.columns:
    if "status" in col.lower():
        status_col = col

if room_col is None:
    st.error("No ROOM column found in GMR file.")
    st.stop()

# ===============================
# ROOM GRID DISPLAY
# ===============================
st.subheader(f"📅 GMR View — {selected_day}")

cols = st.columns(10)

selected_room = None

for idx, room in enumerate(rooms):
    col = cols[idx % 10]

    room_data = gmr_df[gmr_df[room_col].astype(str) == room]

    color = "#d3d3d3"

    if not room_data.empty and status_col:
        status = str(room_data.iloc[0][status_col]).lower()
        if "pending" in status:
            color = "#ffbf00"   # amber
        elif "close" in status:
            color = "#4CAF50"   # green

    if col.button(room, key=room):
        selected_room = room

    col.markdown(
        f"""
        <div style="height:10px; background-color:{color}; border-radius:5px;"></div>
        """,
        unsafe_allow_html=True
    )

# ===============================
# ROOM DETAILS
# ===============================
if selected_room:
    st.subheader(f"🛏️ Room Details — {selected_room}")
    room_details = gmr_df[gmr_df[room_col].astype(str) == selected_room]

    if room_details.empty:
        st.warning("No data available for this room.")
    else:
        st.dataframe(room_details, use_container_width=True)
