import json
import os

class Student:
   
    def __init__(self, name, favorite_subject):
        if not name or not isinstance(name, str):
            raise ValueError("Student name cannot be empty and must be a string.")
        if not favorite_subject or not isinstance(favorite_subject, str):
            raise ValueError("Favorite subject cannot be empty and must be a string.")
        self.name = name.strip().title() 
        self.favorite_subject = favorite_subject.strip().title() 
    def to_dict(self):
       
        return {"name": self.name, "favorite_subject": self.favorite_subject}

    @classmethod
    def from_dict(cls, data):
       
        return cls(data["name"], data["favorite_subject"])

    def __str__(self):
       
        return f"Name: {self.name}, Favorite Subject: {self.favorite_subject}"

class ClassRecordManager:
    
    def __init__(self, filename="class_records.json"):
        self.filename = filename
        self.students = self._load_students()

    def _load_students(self):
      
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
              
                return [Student.from_dict(s_data) for s_data in data]
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {self.filename}. Starting with empty records.")
            return []
        except Exception as e:
            print(f"An error occurred while loading records: {e}. Starting with empty records.")
            return []

    def _save_students(self):
       
        try:
           
            data = [s.to_dict() for s in self.students]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving records to {self.filename}: {e}")

    def add_student(self, name, favorite_subject):
       
        if any(s.name == name.strip().title() for s in self.students):
            print(f"Error: Student '{name.strip().title()}' already exists. Use 'Update Student' to change their subject.")
            return False
        try:
            new_student = Student(name, favorite_subject)
            self.students.append(new_student)
            self._save_students()
            print(f"Student '{new_student.name}' added successfully.")
            return True
        except ValueError as e:
            print(f"Error adding student: {e}")
            return False

    def update_student_subject(self, name, new_favorite_subject):
       
        found = False
        target_name = name.strip().title()
        for student in self.students:
            if student.name == target_name:
                try:
                   
                    if not new_favorite_subject or not isinstance(new_favorite_subject, str):
                        raise ValueError("New favorite subject cannot be empty and must be a string.")
                    student.favorite_subject = new_favorite_subject.strip().title()
                    self._save_students()
                    print(f"Student '{student.name}'s favorite subject updated to '{student.favorite_subject}'.")
                    found = True
                    break
                except ValueError as e:
                    print(f"Error updating subject for '{target_name}': {e}")
                    return False
        if not found:
            print(f"Error: Student '{target_name}' not found in records.")
            return False
        return True

    def display_all_students(self):
       
        if not self.students:
            print("No student records found.")
            return

        print("\n--- Class Student Records ---")
        for i, student in enumerate(self.students, 1):
            print(f"{i}. {student}")
        print("-----------------------------")


def get_user_input(prompt):
   
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again.")

def main_roy_interface():
   
    manager = ClassRecordManager()
    print("--- Welcome, Roy! Class Record Management System ---")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new student")
        print("2. Update an existing student's favorite subject")
        print("3. View all student records")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            name = get_user_input("Enter student's name: ")
            subject = get_user_input(f"Enter {name}'s favorite subject:")
