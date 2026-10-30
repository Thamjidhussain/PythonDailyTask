"""
Story 6 – OOP Coding Challenges
Ten practical, runnable Python OOP examples.

Run:
    py coding_challenges.py

No external packages are required.
"""

from dataclasses import dataclass,field
from math import pi

# 1.Studnet class

class Student:
    def __init__(self,name,roll_number,marks):
        if not name.strip():
            raise ValueError("Studnet name cannot be empty.")
        if not isinstance(marks,(int,float)) or not 0<=marks<=100:
            raise ValueError("Marks must be between 0 and 100.")
        self.name=name
        self.roll_number=roll_number
        self.marks=marks
    def get_grade(self):
        if self.marks>=90:
            return "A"
        if self.marks>=75:
            return "B"
        if self.marks>=60:
            return "C"
        if self.marks>=40:
            return "D"
        return "F"
    def display(self):
        return(
            f"Studnet:{self.name},Roll No:{self.roll_number},"
            f"Marks:{self.marks},Grade:{self.get_grade()}"
        )

# 2 Bank account class 

class BankAccount:
    def __init__(self,account_holder,balance=0):
        if balance<0:
            raise ValueError("Opening balance cannot be negative.")
        self.account_holder=account_holder
        self.__balance=float(balance) #Encapsulated attribute
    def deposit(self,amount):
        if amount<=0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance+=amount
        return self.__balance
    def withdraw(self,amount):
        if amount<=0:
            raise ValueError("Withdraw amount must be positive.")
        if amount>self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance-=amount
        return self.__balance
    def get_balance(self):
        return self.__balance

# 3.Employee Management

@dataclass
class Employee:
    employee_id:int
    name:str
    department:str
    salary:float

    def __post_init__(self):
        if self.salary<0:
            raise ValueError("Salary cannot be negative.")
    def display(self):
        return(
            f"ID:{self.employee_id},Name:{self.name},"
            f"Department:{self.department},Salary:{self.salary:.2f}"
        )
class EmployeeManagement:
    def __init__(self):
        self.employees={}
    def add_employee(self,employee):
        if employee.employee_id in self.employees:
            raise ValueError("Employee ID already exists.")
        self.employees[employee.employee_id]=employee

    def got_employee(self,employee_id):
        return self.employees.get(employee_id)
    def remove_employee(self,employee_id):
        if employee_id not in self.employees:
            raise KeyError("Employee not found.")
        return self.employees.pop(employee_id)
    def display_all(self):
        return [employee.display() for employee in self.employees.values()]

# 4.vehicle inheritance

class Vehicle:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model
    def start(self):
        return f"{self.brand} {self.model} is starting."
class Car(Vehicle):
    def start(self):
        return f"Car {self.brand} {self.model} start with a key or button."
class Bike(Vehicle):
    def start(self):
        return f"Bike{self.brand} {self.model} starts with an ignition."


# 5.shape area calculator

class Shape:
    def area(self):
        raise NotImplementedError("Subclasses implement area().")
class Circle(Shape):
    def __init__(self,radius):
         if radius<0:
             raise ValueError("Radius cannot be negative.")
         self.radius=radius
    def area(self):
        return pi * self.radius **2

class Rectangle(Shape):
    def __init__(self,length,width):
        if length<0 or width <0:
            raise ValueError("Length and width cannot be negative.")
        self.length=length
        self.width=width

    def area(self):
        return self.length*self.width

class Triangle(Shape):
    def __init__(self,base,height):
        if base <0 or height<0:
            raise ValueError("Base and height cannot be negative.")
        self.base=base
        self.height=height
    def area(self):
        return 0.5* self.base *self.height


# 6.shopping cart

@dataclass 
class Product:
    name:str
    price:float

    def __post_init__(self):
        if self.price<0:
            raise ValueError("Product price cannot be negative.")
class ShoppingCart:
    def __init__(self):
        self.items={}

    def add_item(self,product,quantity=1):
        if quantity <=0:
            raise ValueError("Quantity must be positive.")

        if product.name in self.items:
            self.items[product.name][1]+=quantity

        else:
            self.items[product.name]=[product,quantity]

    def remove_item(self,product_name):
        if product_name not in self.items:
            raise KeyError("product is not  in the cart.")
        del self.items[product_name]

    def total(self):
        return sum(product.price*quantity
                   for product,quantity in self.items.values())

    def display(self):

        return[
            f"{product.name} x {quantity} ="
            f"{product.price * quantity:.2f}"
            for product,quantity in self.items.values()
        ]

# 7. Movie rating system
class Movie:
    def __init__(self, title):
        self.title = title
        self._ratings = []

    def add_rating(self, rating):
        if not isinstance(rating, (int, float)) or not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self._ratings.append(float(rating))

    def average_rating(self):
        if not self._ratings:
            return 0.0
        return sum(self._ratings) / len(self._ratings)

    def display(self):
        return (
            f"{self.title}: {len(self._ratings)} ratings, "
            f"average {self.average_rating():.1f}/5"
        )

# 8. Hospital patient records
@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    diagnosis: str

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative.")

    def display(self):
        return (
            f"Patient ID: {self.patient_id}, Name: {self.name}, "
            f"Age: {self.age}, Diagnosis: {self.diagnosis}"
        )


class Hospital:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient):
        if patient.patient_id in self.patients:
            raise ValueError("Patient ID already exists.")
        self.patients[patient.patient_id] = patient

    def find_patient(self, patient_id):
        return self.patients.get(patient_id)

    def remove_patient(self, patient_id):
        if patient_id not in self.patients:
            raise KeyError("Patient not found.")
        return self.patients.pop(patient_id)

# 9. School result processing
class SchoolResult:
    def __init__(self, student_name, subject_marks):
        if not subject_marks:
            raise ValueError("At least one subject mark is required.")
        for subject, mark in subject_marks.items():
            if not 0 <= mark <= 100:
                raise ValueError(f"Invalid mark for {subject}.")
        self.student_name = student_name
        self.subject_marks = dict(subject_marks)

    def total_marks(self):
        return sum(self.subject_marks.values())

    def percentage(self):
        return self.total_marks() / len(self.subject_marks)

    def result(self):
        return "Pass" if all(mark >= 35 for mark in self.subject_marks.values()) else "Fail"

    def display(self):
        subjects = ", ".join(
            f"{subject}: {mark}" for subject, mark in self.subject_marks.items()
        )
        return (
            f"{self.student_name} | {subjects} | "
            f"Total: {self.total_marks()} | "
            f"Percentage: {self.percentage():.2f}% | "
            f"Result: {self.result()}"
        )
# 10. Online course management
@dataclass
class Course:
    course_id: int
    title: str
    instructor: str
    fee: float

    def __post_init__(self):
        if self.fee < 0:
            raise ValueError("Course fee cannot be negative.")


class OnlineCourseManagement:
    def __init__(self):
        self.courses = {}
        self.enrollments = {}

    def add_course(self, course):
        if course.course_id in self.courses:
            raise ValueError("Course ID already exists.")
        self.courses[course.course_id] = course

    def enroll_student(self, student_name, course_id):
        if course_id not in self.courses:
            raise KeyError("Course not found.")
        self.enrollments.setdefault(course_id, set()).add(student_name)

    def list_students(self, course_id):
        if course_id not in self.courses:
            raise KeyError("Course not found.")
        return sorted(self.enrollments.get(course_id, set()))

    def list_courses(self):
        return [
            f"{course.title} by {course.instructor} - Fee: {course.fee:.2f}"
            for course in self.courses.values()
        ]
# Demonstration of all 10 challenges
def main():
    print("\n1. STUDENT CLASS")
    student = Student("Asha", 101, 86)
    print(student.display())

    print("\n2. BANK ACCOUNT")
    account = BankAccount("Asha", 1000)
    account.deposit(500)
    account.withdraw(200)
    print(f"Account holder: {account.account_holder}")
    print(f"Balance: {account.get_balance():.2f}")

    print("\n3. EMPLOYEE MANAGEMENT")
    employees = EmployeeManagement()
    employees.add_employee(Employee(1, "Ravi", "IT", 45000))
    employees.add_employee(Employee(2, "Meena", "HR", 40000))
    for record in employees.display_all():
        print(record)

    print("\n4. VEHICLE INHERITANCE")
    vehicles = [Car("Toyota", "Corolla"), Bike("Honda", "Shine")]
    for vehicle in vehicles:
        print(vehicle.start())

    print("\n5. SHAPE AREA CALCULATOR")
    shapes = [Circle(5), Rectangle(4, 6), Triangle(4, 5)]
    for shape in shapes:
        print(f"{type(shape).__name__} area: {shape.area():.2f}")

    print("\n6. SHOPPING CART")
    cart = ShoppingCart()
    cart.add_item(Product("Notebook", 50), 2)
    cart.add_item(Product("Pen", 10), 3)
    for item in cart.display():
        print(item)
    print(f"Cart total: {cart.total():.2f}")

    print("\n7. MOVIE RATING SYSTEM")
    movie = Movie("The Example Movie")
    movie.add_rating(4)
    movie.add_rating(5)
    movie.add_rating(3)
    print(movie.display())

    print("\n8. HOSPITAL PATIENT RECORDS")
    hospital = Hospital()
    hospital.add_patient(Patient(1001, "Kiran", 35, "Fever"))
    patient = hospital.find_patient(1001)
    print(patient.display() if patient else "Patient not found.")

    print("\n9. SCHOOL RESULT PROCESSING")
    result = SchoolResult("Arun", {
        "Maths": 85, "Science": 78, "English": 92
    })
    print(result.display())

    print("\n10. ONLINE COURSE MANAGEMENT")
    learning = OnlineCourseManagement()
    learning.add_course(Course(501, "Python OOP", "Instructor Priya", 1999))
    learning.enroll_student("Asha", 501)
    learning.enroll_student("Ravi", 501)
    for course in learning.list_courses():
        print(course)
    print("Enrolled students:", learning.list_students(501))


if __name__ == "__main__":
    main()