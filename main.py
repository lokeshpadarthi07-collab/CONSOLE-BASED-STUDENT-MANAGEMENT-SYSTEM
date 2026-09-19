"""
CONSOLE-BASED STUDENT MANAGEMENT SYSTEM
Main entrypoint module containing interactive CLI menu and application loop.
"""

import sys
from typing import Optional

from models.student import Student
from services.student_manager import StudentManager
from utils.validators import Validator


# Terminal formatting constants for clean CLI display
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(title: str) -> None:
    """Print a stylized section header."""
    print(f"\n{Colors.OKCYAN}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'=' * 60}{Colors.ENDC}")


def print_success(message: str) -> None:
    """Print success message in green."""
    print(f"{Colors.OKGREEN}✔ SUCCESS: {message}{Colors.ENDC}")


def print_error(message: str) -> None:
    """Print error message in red."""
    print(f"{Colors.FAIL}✖ ERROR: {message}{Colors.ENDC}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.WARNING}⚠ WARNING: {message}{Colors.ENDC}")


def get_validated_input(
    prompt: str,
    validator_func,
    allow_empty: bool = False,
    default_value: Optional[str] = None,
) -> str | int | float:
    """
    Prompt user repeatedly until valid input is received or cancelled.

    Args:
        prompt: User input prompt string.
        validator_func: Validation callable function.
        allow_empty: If True, empty input returns default_value.
        default_value: Fallback value if empty input is allowed.
    """
    while True:
        try:
            raw_val = input(f"{Colors.BOLD}{prompt}{Colors.ENDC}").strip()
            if allow_empty and not raw_val:
                return default_value
            return validator_func(raw_val)
        except ValueError as ve:
            print_error(str(ve))
            print("Please try again.\n")


def display_students_table(students: list[Student]) -> None:
    """Display student list in a formatted ASCII table."""
    if not students:
        print_warning("No student records found.")
        return

    header_fmt = (
        "{:<8} | {:<20} | {:<4} | {:<24} | {:<14} | {:<18} | {:<10} | {:<6}"
    )
    row_fmt = (
        "{:<8} | {:<20} | {:<4} | {:<24} | {:<14} | {:<18} | {:<10} | {:<6.2f}"
    )
    separator = "-" * 118

    print(f"\n{Colors.OKCYAN}{separator}{Colors.ENDC}")
    print(
        Colors.BOLD
        + header_fmt.format(
            "ID", "Name", "Age", "Email", "Phone", "Course", "Year", "GPA"
        )
        + Colors.ENDC
    )
    print(f"{Colors.OKCYAN}{separator}{Colors.ENDC}")

    for s in students:
        print(
            row_fmt.format(
                s.student_id,
                s.name[:20],
                s.age,
                s.email[:24],
                s.phone[:14],
                s.course[:18],
                s.year[:10],
                s.gpa,
            )
        )

    print(f"{Colors.OKCYAN}{separator}{Colors.ENDC}")
    print(f"Total Records: {Colors.BOLD}{len(students)}{Colors.ENDC}\n")


class StudentApp:
    """Main CLI Application handler for the Student Management System."""

    def __init__(self) -> None:
        self.manager = StudentManager()

    def run(self) -> None:
        """Application main execution loop."""
        # Auto-load existing records from JSON on launch
        try:
            count = self.manager.load_from_json()
            if count > 0:
                print(
                    f"{Colors.OKGREEN}System initialized. Loaded {count} student records from JSON persistence.{Colors.ENDC}"
                )
        except Exception as e:
            print_warning(f"Could not load initial records: {e}")

        while True:
            self.display_main_menu()
            choice = input(
                f"{Colors.BOLD}Enter your choice (1-9): {Colors.ENDC}"
            ).strip()

            if choice == "1":
                self.handle_add_student()
            elif choice == "2":
                self.handle_update_student()
            elif choice == "3":
                self.handle_delete_student()
            elif choice == "4":
                self.handle_search_student()
            elif choice == "5":
                self.handle_display_all()
            elif choice == "6":
                self.handle_save_json()
            elif choice == "7":
                self.handle_load_json()
            elif choice == "8":
                self.handle_export_csv()
            elif choice == "9":
                print_header("THANK YOU FOR USING STUDENT MANAGEMENT SYSTEM")
                print("Goodbye!\n")
                sys.exit(0)
            else:
                print_error("Invalid option choice. Please select a number between 1 and 9.\n")

    @staticmethod
    def display_main_menu() -> None:
        """Display clean main menu interface."""
        print(f"\n{Colors.OKBLUE}{'=' * 44}{Colors.ENDC}")
        print(
            f"{Colors.BOLD}{Colors.OKBLUE}       STUDENT MANAGEMENT SYSTEM       {Colors.ENDC}"
        )
        print(f"{Colors.OKBLUE}{'=' * 44}{Colors.ENDC}")
        print("  1. Add Student")
        print("  2. Update Student")
        print("  3. Delete Student")
        print("  4. Search Student")
        print("  5. Display All Students")
        print("  6. Save Students to JSON")
        print("  7. Load Students from JSON")
        print("  8. Export Students to CSV")
        print("  9. Exit")
        print(f"{Colors.OKBLUE}{'-' * 44}{Colors.ENDC}")

    def handle_add_student(self) -> None:
        """Option 1: Add Student"""
        print_header("ADD NEW STUDENT")

        # Validate unique ID
        def id_val(val: str) -> str:
            return Validator.validate_student_id(val, self.manager.get_existing_ids())

        student_id = get_validated_input("Enter Student ID (e.g., S105): ", id_val)
        name = get_validated_input("Enter Student Name: ", Validator.validate_name)
        age = get_validated_input("Enter Age (15-100): ", Validator.validate_age)
        email = get_validated_input("Enter Email: ", Validator.validate_email)
        phone = get_validated_input("Enter Phone Number: ", Validator.validate_phone)
        course = get_validated_input(
            "Enter Course (e.g., B.Tech CS): ",
            lambda v: Validator.validate_non_empty(v, "Course"),
        )
        year = get_validated_input("Enter Year (e.g., 1st Year): ", Validator.validate_year)
        department = get_validated_input(
            "Enter Department: ",
            lambda v: Validator.validate_non_empty(v, "Department"),
        )
        gpa = get_validated_input("Enter Marks/GPA (0.0 to 100.0): ", Validator.validate_gpa)

        new_student = Student(
            student_id=str(student_id),
            name=str(name),
            age=int(age),
            email=str(email),
            phone=str(phone),
            course=str(course),
            year=str(year),
            department=str(department),
            gpa=float(gpa),
        )

        try:
            self.manager.add_student(new_student)
            print_success(f"Student '{new_student.name}' (ID: {new_student.student_id}) added successfully!")
        except ValueError as ve:
            print_error(str(ve))

    def handle_update_student(self) -> None:
        """Option 2: Update Student"""
        print_header("UPDATE STUDENT DETAILS")

        student_id = input("Enter Student ID to update: ").strip()
        student = self.manager.get_student_by_id(student_id)

        if not student:
            print_error(f"Student with ID '{student_id}' not found.")
            return

        print(f"\n{Colors.BOLD}Current Details for Student ID: {student.student_id}{Colors.ENDC}")
        print(student)
        print("\n(Press ENTER to skip any field and keep its current value)\n")

        updated_fields = {}

        # Name
        new_name = get_validated_input(
            f"New Name [{student.name}]: ",
            Validator.validate_name,
            allow_empty=True,
            default_value=student.name,
        )
        if new_name != student.name:
            updated_fields["name"] = new_name

        # Age
        new_age = get_validated_input(
            f"New Age [{student.age}]: ",
            Validator.validate_age,
            allow_empty=True,
            default_value=student.age,
        )
        if new_age != student.age:
            updated_fields["age"] = new_age

        # Email
        new_email = get_validated_input(
            f"New Email [{student.email}]: ",
            Validator.validate_email,
            allow_empty=True,
            default_value=student.email,
        )
        if new_email != student.email:
            updated_fields["email"] = new_email

        # Phone
        new_phone = get_validated_input(
            f"New Phone [{student.phone}]: ",
            Validator.validate_phone,
            allow_empty=True,
            default_value=student.phone,
        )
        if new_phone != student.phone:
            updated_fields["phone"] = new_phone

        # Course
        new_course = get_validated_input(
            f"New Course [{student.course}]: ",
            lambda v: Validator.validate_non_empty(v, "Course"),
            allow_empty=True,
            default_value=student.course,
        )
        if new_course != student.course:
            updated_fields["course"] = new_course

        # Year
        new_year = get_validated_input(
            f"New Year [{student.year}]: ",
            Validator.validate_year,
            allow_empty=True,
            default_value=student.year,
        )
        if new_year != student.year:
            updated_fields["year"] = new_year

        # Department
        new_dept = get_validated_input(
            f"New Department [{student.department}]: ",
            lambda v: Validator.validate_non_empty(v, "Department"),
            allow_empty=True,
            default_value=student.department,
        )
        if new_dept != student.department:
            updated_fields["department"] = new_dept

        # GPA
        new_gpa = get_validated_input(
            f"New Marks/GPA [{student.gpa}]: ",
            Validator.validate_gpa,
            allow_empty=True,
            default_value=student.gpa,
        )
        if new_gpa != student.gpa:
            updated_fields["gpa"] = new_gpa

        if not updated_fields:
            print_warning("No changes were made.")
            return

        try:
            self.manager.update_student(student.student_id, updated_fields)
            print_success(f"Student '{student.student_id}' updated successfully!")
        except Exception as e:
            print_error(f"Failed to update student: {e}")

    def handle_delete_student(self) -> None:
        """Option 3: Delete Student"""
        print_header("DELETE STUDENT RECORD")

        student_id = input("Enter Student ID to delete: ").strip()
        student = self.manager.get_student_by_id(student_id)

        if not student:
            print_error(f"Student with ID '{student_id}' not found.")
            return

        print(f"\n{Colors.WARNING}Found Student Record:{Colors.ENDC}")
        print(student)

        confirm = input(
            f"\n{Colors.BOLD}{Colors.FAIL}Are you sure you want to delete this student? (y/N): {Colors.ENDC}"
        ).strip().lower()

        if confirm in ("y", "yes"):
            try:
                self.manager.delete_student(student.student_id)
                print_success(f"Student ID '{student_id}' deleted successfully.")
            except KeyError as ke:
                print_error(str(ke))
        else:
            print_warning("Deletion cancelled.")

    def handle_search_student(self) -> None:
        """Option 4: Search Student"""
        print_header("SEARCH STUDENTS")

        print("Search by:")
        print("  1. Student ID")
        print("  2. Name")
        print("  3. Course")
        print("  4. Department")
        print("  5. All Fields")

        sub_choice = input(f"\n{Colors.BOLD}Enter search option (1-5): {Colors.ENDC}").strip()
        search_field_map = {
            "1": "id",
            "2": "name",
            "3": "course",
            "4": "department",
            "5": "all",
        }

        search_by = search_field_map.get(sub_choice, "all")
        query = input("Enter search term: ").strip()

        results = self.manager.search_students(query, search_by=search_by)

        if results:
            print_success(f"Found {len(results)} matching student(s):")
            display_students_table(results)
        else:
            print_warning(f"No student found matching query '{query}'.")

    def handle_display_all(self) -> None:
        """Option 5: Display All Students"""
        print_header("ALL REGISTERED STUDENTS")
        display_students_table(self.manager.get_all_students())

    def handle_save_json(self) -> None:
        """Option 6: Save Students to JSON"""
        print_header("SAVE RECORDS TO JSON")
        try:
            self.manager.save_to_json()
            print_success(f"Successfully saved {self.manager.student_count} records to '{self.manager.json_file_path}'.")
        except Exception as e:
            print_error(f"Failed to save records to JSON: {e}")

    def handle_load_json(self) -> None:
        """Option 7: Load Students from JSON"""
        print_header("LOAD RECORDS FROM JSON")
        try:
            count = self.manager.load_from_json()
            print_success(f"Successfully loaded {count} student records from '{self.manager.json_file_path}'.")
        except FileNotFoundError:
            print_warning(f"JSON persistence file '{self.manager.json_file_path}' was not found.")
        except Exception as e:
            print_error(f"Failed to load JSON file: {e}")

    def handle_export_csv(self) -> None:
        """Option 8: Export Students to CSV"""
        print_header("EXPORT RECORDS TO CSV")
        try:
            self.manager.export_to_csv()
            print_success(f"Successfully exported {self.manager.student_count} records to '{self.manager.csv_file_path}'.")
        except Exception as e:
            print_error(f"Failed to export CSV: {e}")


def main() -> None:
    """Program entrypoint."""
    try:
        app = StudentApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
