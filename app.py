import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Paradis Beachcomber Rooms Dashboard")

# ---- VIEW SELECTOR (GMR / GSS) ----
view = st.radio("Select View", ["GMR", "GSS"], horizontal=True)

if view == "GMR":

    st.subheader("GMR View")

    uploaded_file = st.file_uploader(
        "Upload GMR Excel file (any month)",
        type=["xlsx"],
        key="gmr_upload"
    )

    if uploaded_file:

        # Read all sheets
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names

        selected_sheet = st.selectbox(
            "Select Date (Sheet)",
            sheet_names
        )

        gmr_df = pd.read_excel(xls, sheet_name=selected_sheet)

        # Use EXACT column names from your file
        room_col = "RM"

        status_col = None
        for col in gmr_df.columns:
            if "status" in col.lower():
                status_col = col

        if status_col is None:
            st.error("No STATUS column found in GMR file.")
            st.stop()

        # Room plan
        room_plan = pd.read_excel("Room plan.xlsx")
        rooms = room_plan.iloc[:, 0].astype(str).tolist()

        st.markdown("### Rooms")

        cols = st.columns(10)
        col_index = 0

        for room in rooms:
            room_data = gmr_df[gmr_df[room_col].astype(str) == str(room)]

            if not room_data.empty:
                status = str(room_data.iloc[0][status_col]).lower()
            else:
                status = "unknown"

            if "pending" in status:
                color = "#FFC107"  # amber
            elif "close" in status or "closed" in status:
                color = "#4CAF50"  # green
            else:
                color = "#E0E0E0"  # grey

            with cols[col_index]:
                if st.button(room, key=f"room_{room}"):
                    st.session_state["selected_room"] = room

                st.markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        height:10px;
                        border-radius:5px;
                        margin-bottom:10px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            col_index += 1
            if col_index == 10:
                cols = st.columns(10)
                col_index = 0

        if "selected_room" in st.session_state:
            st.markdown("---")
            st.subheader(f"Room Details: {st.session_state['selected_room']}")

            details = gmr_df[
                gmr_df[room_col].astype(str) == str(st.session_state["selected_room"])
            ]

            st.dataframe(details)

    else:
        st.info("Please upload a GMR Excel file to begin.")

else:
    st.info("GSS view will be added next.")


