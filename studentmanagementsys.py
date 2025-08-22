# Student Management System

students = {}

def add_student():
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    grade = input("Enter student grade: ")
    students[student_id] = {
        "name": name,
        "age": age,
        "grade": grade
    }
    print("Student added successfully.\n")

def update_student():
    student_id = input("Enter student ID to update: ")
    if student_id in students:
        print("Current info:", students[student_id])
        name = input("Enter new name (leave blank to keep current): ")
        age = input("Enter new age (leave blank to keep current): ")
        grade = input("Enter new grade (leave blank to keep current): ")

        if name:
            students[student_id]["name"] = name
        if age:
            students[student_id]["age"] = age
        if grade:
            students[student_id]["grade"] = grade

        print("Student information updated.\n")
    else:
        print("Student not found.\n")

def display_students():
    if not students:
        print("No student records found.\n")
    else:
        for sid, info in students.items():
            print(f"ID: {sid}, Name: {info['name']}, Age: {info['age']}, Grade: {info['grade']}")
        print()

def main():
    while True:
        print("1. Add Student")
        print("2. Update Student")
        print("3. Display All Students")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            display_students()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
