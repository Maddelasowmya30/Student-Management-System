
import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# Initialize Student List
# -------------------------------

if "students" not in st.session_state:
    st.session_state.students = []


# -------------------------------
# Calculate Student Result
# -------------------------------

def calculate_result(marks):
    total = sum(marks.values())
    percentage = total / len(marks)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    return total, percentage, grade


# -------------------------------
# Find Student by ID
# -------------------------------

def find_student(student_id):
    for student in st.session_state.students:
        if student["id"] == student_id:
            return student
    return None


# -------------------------------
# Display Student Information
# -------------------------------

def display_student(student):
    total, percentage, grade = calculate_result(student["marks"])

    st.write("**Student ID:**", student["id"])
    st.write("**Name:**", student["name"])

    st.write("**Marks:**")
    for subject, mark in student["marks"].items():
        st.write(f"- {subject}: {mark}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Marks", f"{total:.2f}")
    col2.metric("Percentage", f"{percentage:.2f}%")
    col3.metric("Grade", grade)


# -------------------------------
# Application Title
# -------------------------------

st.title("🎓 Student Management System")
st.write("Manage student records, marks, and academic results.")

st.divider()

# -------------------------------
# Sidebar Menu
# -------------------------------

menu = st.sidebar.selectbox(
    "Choose an Operation",
    [
        "Home",
        "Add Student",
        "Display Students",
        "Search Student",
        "Update Student",
        "Delete Student"
    ]
)


# -------------------------------
# Home
# -------------------------------

if menu == "Home":

    st.header("Welcome to Student Management System")

    st.write(
        "This application allows you to add, view, search, "
        "update, and delete student records."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Students",
        len(st.session_state.students)
    )

    col2.metric(
        "Subjects",
        3
    )

    col3.metric(
        "Application",
        "Streamlit"
    )

    st.info("Select an operation from the sidebar to get started.")


# -------------------------------
# Add Student
# -------------------------------

elif menu == "Add Student":

    st.header("➕ Add Student")

    with st.form("add_student_form"):

        student_id = st.text_input("Student ID")
        name = st.text_input("Student Name")

        st.subheader("Enter Marks")

        python_marks = st.number_input(
            "Python Marks",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0
        )

        maths_marks = st.number_input(
            "Maths Marks",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0
        )

        english_marks = st.number_input(
            "English Marks",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0
        )

        submit = st.form_submit_button("Add Student")

        if submit:

            student_id = student_id.strip()
            name = name.strip()

            if student_id == "" or name == "":
                st.error("Please enter both student ID and name.")

            elif find_student(student_id) is not None:
                st.error("A student with this ID already exists.")

            else:

                student = {
                    "id": student_id,
                    "name": name,
                    "marks": {
                        "Python": python_marks,
                        "Maths": maths_marks,
                        "English": english_marks
                    }
                }

                st.session_state.students.append(student)

                st.success("Student added successfully!")


# -------------------------------
# Display All Students
# -------------------------------

elif menu == "Display Students":

    st.header("📋 All Student Records")

    if len(st.session_state.students) == 0:

        st.warning("No student records available.")

    else:

        for index, student in enumerate(
            st.session_state.students
        ):

            with st.expander(
                f"{student['id']} - {student['name']}"
            ):

                display_student(student)

                st.divider()


# -------------------------------
# Search Student
# -------------------------------

elif menu == "Search Student":

    st.header("🔍 Search Student")

    search_value = st.text_input(
        "Enter student ID or name"
    ).strip().lower()

    if st.button("Search"):

        if search_value == "":
            st.warning("Please enter an ID or name.")

        else:

            found = False

            for student in st.session_state.students:

                if (
                    student["id"].lower() == search_value
                    or student["name"].lower() == search_value
                ):

                    display_student(student)
                    st.divider()
                    found = True

            if not found:
                st.error("Student not found.")


# -------------------------------
# Update Student
# -------------------------------

elif menu == "Update Student":

    st.header("✏️ Update Student")

    if len(st.session_state.students) == 0:

        st.warning("No student records available.")

    else:

        student_ids = [
            student["id"]
            for student in st.session_state.students
        ]

        selected_id = st.selectbox(
            "Select Student ID",
            student_ids
        )

        student = find_student(selected_id)

        if student is not None:

            with st.form("update_student_form"):

                new_name = st.text_input(
                    "Student Name",
                    value=student["name"]
                )

                st.subheader("Update Marks")

                new_python = st.number_input(
                    "Python Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(student["marks"]["Python"]),
                    step=1.0
                )

                new_maths = st.number_input(
                    "Maths Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(student["marks"]["Maths"]),
                    step=1.0
                )

                new_english = st.number_input(
                    "English Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(student["marks"]["English"]),
                    step=1.0
                )

                update_button = st.form_submit_button(
                    "Update Student"
                )

                if update_button:

                    new_name = new_name.strip()

                    if new_name == "":
                        st.error("Name cannot be empty.")

                    else:

                        student["name"] = new_name

                        student["marks"] = {
                            "Python": new_python,
                            "Maths": new_maths,
                            "English": new_english
                        }

                        st.success(
                            "Student record updated successfully!"
                        )


# -------------------------------
# Delete Student
# -------------------------------

elif menu == "Delete Student":

    st.header("🗑️ Delete Student")

    if len(st.session_state.students) == 0:

        st.warning("No student records available.")

    else:

        student_ids = [
            student["id"]
            for student in st.session_state.students
        ]

        selected_id = st.selectbox(
            "Select Student ID to delete",
            student_ids
        )

        student = find_student(selected_id)

        if student is not None:

            st.write("**Student Name:**", student["name"])

            confirm = st.checkbox(
                "I confirm that I want to delete this student."
            )

            if st.button("Delete Student", type="primary"):

                if confirm:

                    st.session_state.students = [
                        item
                        for item in st.session_state.students
                        if item["id"] != selected_id
                    ]

                    st.success(
                        "Student deleted successfully!"
                    )

                else:

                    st.warning(
                        "Please confirm deletion first."
                    )