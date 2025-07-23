from app.models.student import Student

def format_student_row(student: Student) -> str:
    full_name = f"{student.forename} {student.surname}"
    status = "Active" if bool(student.is_active) else "Inactive"
    return f"{student.id:<5} {full_name:<25} {status:<10} Parent ID: {student.parent_id}"

