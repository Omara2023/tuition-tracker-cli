from app.models.student import Student

def format_student_row(student: Student) -> str:
    full_name = f"{student.forename} {student.surname}"
    status = "Active" if bool(student.is_active) else "Inactive"
    return f"{student.id:<5} {full_name:<20} {status:<10} {student.parent_id:<10}"

