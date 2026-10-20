import pandas as pd
import streamlit as st
import os

st.title("Attendance Management System")

# Students ki details read karo
students = pd.read_csv("students.csv")

# Date select karo
date = st.date_input("Select Date")

st.subheader("Mark Attendance")

# Attendance column add karo
students["Attendance"] = "Present"

# Table
attendance_table = st.data_editor(
    students,

    column_config={
        "Roll No.": st.column_config.NumberColumn(
            "Roll No.",
            disabled=True
        ),

        "Name": st.column_config.TextColumn(
            "Name",
            disabled=True
        ),

        "Subject": st.column_config.TextColumn(
            "Subject",
            disabled=True
        ),

        "Attendance": st.column_config.SelectboxColumn(
            "Attendance",
            options=["Present", "Absent"],
            required=True
        )
    },

    hide_index=True,
    width="stretch"
)

# Save button
if st.button("Save Attendance"):

    # Date ko table me add karo
    attendance_table["Date"] = date

    # Columns ko required order me arrange karo
    attendance_table = attendance_table[
        ["Date", "Roll No.", "Name", "Subject", "Attendance"]
    ]

    # Attendance file me save karo
    file_exists = os.path.exists("attendance.csv")

    attendance_table.to_csv(
        "attendance.csv",
        mode="a",
        header=not file_exists,
        index=False
    )

    st.success("Attendance successfully saved!")

    st.write("Saved Attendance:")
    st.dataframe(attendance_table)

st.subheader("Student Attendance Profile")

roll_no = st.number_input(
    "Enter Roll No.",
    min_value=1,
    step=1
)

if st.button("Search Student"):

    # Student ki basic details students.csv se
    student = students.loc[students["Roll No."] == roll_no]

    if student.empty:

        st.error("Student not found!")

    else:

        # Student ki details
        student_info = student.iloc[0]

        name = student_info["Name"]
        subject = student_info["Subject"]

        # Attendance file check karo
        if os.path.exists("attendance.csv"):

            attendance = pd.read_csv("attendance.csv")

            # Sirf selected student ka attendance
            student_attendance = attendance[
                attendance["Roll No."] == roll_no
            ]

            # Total classes
            total_classes = len(student_attendance)

            # Present count
            present = (
                student_attendance["Attendance"] == "Present"
            ).sum()

            # Absent count
            absent = (
                student_attendance["Attendance"] == "Absent"
            ).sum()

            # Percentage
            if total_classes > 0:
                percentage = (present / total_classes) * 100
            else:
                percentage = 0

            # Profile display
            st.success("Student Found!")

            st.write("### Student Details")

            st.write("**Roll No.:**", roll_no)
            st.write("**Name:**", name)
            st.write("**Subject:**", subject)

            st.write("### Attendance Details")

            st.write("**Total Classes:**", total_classes)
            st.write("**Present:**", present)
            st.write("**Absent:**", absent)
            st.write(
                "**Attendance Percentage:**",
                f"{percentage:.2f}%"
            )

        else:
            st.warning("No attendance data available yet.")