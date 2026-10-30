"""
Story 2 – OOP Implementation in Python

Concepts covered:
1. Encapsulation
2. Single Inheritance
3. Multiple Inheritance
4. Multilevel Inheritance
5. Hierarchical Inheritance
6. Polymorphism
7. Method Overriding
8. Method Overloading using Default Arguments
9. Composition
10. Aggregation

Run: py oop_examples.py
"""


# ============================================================
# 1. ENCAPSULATION
# Encapsulation groups data and methods in one class.
# A double underscore triggers name mangling to discourage
# direct access to the balance attribute.
# ============================================================

class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount: float) -> None:
        # Only positive amounts can be deposited.
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount:.2f}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount: float) -> None:
        # Check the amount and available balance.
        if amount <= 0:
            print("Invalid withdrawal amount.")
        elif amount > self.__balance:
            print("Insufficient balance.")
        else:
            self.__balance -= amount
            print(f"Withdrawn: {amount:.2f}")

    def get_balance(self) -> float:
        # Provide controlled access to the balance.
        return self.__balance


def demonstrate_encapsulation() -> None:
    print("\n=== 1. Encapsulation ===")
    account = BankAccount("Asha", 1000)
    account.deposit(250)
    account.withdraw(100)
    print("Account holder:", account.owner)
    print(f"Current balance: {account.get_balance():.2f}")


# ============================================================
# 2. SINGLE INHERITANCE
# Developer inherits methods and attributes from Employee.
# ============================================================

class Employee:
    def __init__(self, name: str, employee_id: int):
        self.name = name
        self.employee_id = employee_id

    def show_details(self) -> None:
        print(f"Employee: {self.name}, ID: {self.employee_id}")


class Developer(Employee):
    def write_code(self) -> None:
        print(f"{self.name} is writing Python code.")


def demonstrate_single_inheritance() -> None:
    print("\n=== 2. Single Inheritance ===")
    developer = Developer("Ravi", 101)
    developer.show_details()
    developer.write_code()


# ============================================================
# 3. MULTIPLE INHERITANCE
# SmartPhone inherits features from Camera and Phone.
# ============================================================

class Camera:
    def take_photo(self) -> None:
        print("Photo captured.")


class Phone:
    def make_call(self, number: str) -> None:
        print(f"Calling {number}...")


class SmartPhone(Camera, Phone):
    def browse_internet(self) -> None:
        print("Browsing the internet.")


def demonstrate_multiple_inheritance() -> None:
    print("\n=== 3. Multiple Inheritance ===")
    device = SmartPhone()
    device.take_photo()
    device.make_call("555-0100")
    device.browse_internet()


# ============================================================
# 4. MULTILEVEL INHERITANCE
# LivingThing -> Animal -> Dog
# Dog inherits methods from both Animal and LivingThing.
# ============================================================

class LivingThing:
    def exist(self) -> None:
        print("This living thing exists.")


class Animal(LivingThing):
    def breathe(self) -> None:
        print("The animal breathes.")


class Dog(Animal):
    def bark(self) -> None:
        print("The dog barks.")


def demonstrate_multilevel_inheritance() -> None:
    print("\n=== 4. Multilevel Inheritance ===")
    dog = Dog()
    dog.exist()
    dog.breathe()
    dog.bark()


# ============================================================
# 5. HIERARCHICAL INHERITANCE
# Car and Motorcycle inherit from the same Vehicle class.
# ============================================================

class Vehicle:
    def start(self) -> None:
        print("Vehicle started.")


class Car(Vehicle):
    def drive(self) -> None:
        print("Car is driving.")


class Motorcycle(Vehicle):
    def ride(self) -> None:
        print("Motorcycle is being ridden.")


def demonstrate_hierarchical_inheritance() -> None:
    print("\n=== 5. Hierarchical Inheritance ===")
    car = Car()
    motorcycle = Motorcycle()

    car.start()
    car.drive()

    motorcycle.start()
    motorcycle.ride()


# ============================================================
# 6. POLYMORPHISM
# 7. METHOD OVERRIDING
# Each notification class provides its own send() behavior.
# The same method call produces different results.
# ============================================================

class Notification:
    def send(self, message: str) -> None:
        print(f"General notification: {message}")


class EmailNotification(Notification):
    # Overrides the parent class send() method.
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")


class SMSNotification(Notification):
    # Overrides the parent class send() method.
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


def demonstrate_polymorphism_and_overriding() -> None:
    print("\n=== 6–7. Polymorphism and Method Overriding ===")

    notifications = [
        EmailNotification(),
        SMSNotification(),
        Notification(),
    ]

    # The same method call behaves differently for each object.
    for notification in notifications:
        notification.send("Your order has been shipped.")


# ============================================================
# 8. METHOD OVERLOADING USING DEFAULT ARGUMENTS
# Python does not support traditional Java-style method
# overloading by signature. Default arguments allow optional
# parameters and flexible calls to the same method.
# ============================================================

class BillCalculator:
    def calculate_total(
        self,
        price: float,
        quantity: int = 1,
        discount: float = 0
    ) -> float:
        # Validate the inputs before calculating the total.
        if price < 0 or quantity < 0:
            raise ValueError("Price and quantity cannot be negative.")

        if not 0 <= discount <= 100:
            raise ValueError("Discount must be between 0 and 100.")

        subtotal = price * quantity
        return subtotal * (1 - discount / 100)


def demonstrate_default_argument_overloading() -> None:
    print("\n=== 8. Default Arguments ===")
    calculator = BillCalculator()

    print(f"One item: {calculator.calculate_total(100):.2f}")
    print(f"Three items: {calculator.calculate_total(100, 3):.2f}")
    print(
        "Three items with 10% discount: "
        f"{calculator.calculate_total(100, 3, 10):.2f}"
    )


# ============================================================
# 9. COMPOSITION
# A ComposedCar creates its own Engine object.
# This demonstrates a strong has-a relationship.
# ============================================================

class Engine:
    def start(self) -> None:
        print("Engine started.")


class ComposedCar:
    def __init__(self):
        # The engine is created inside the car.
        self.engine = Engine()

    def start(self) -> None:
        self.engine.start()
        print("Car is ready to move.")


def demonstrate_composition() -> None:
    print("\n=== 9. Composition ===")
    car = ComposedCar()
    car.start()


# ============================================================
# 10. AGGREGATION
# Department receives an existing Teacher object.
# The teacher can exist independently of the department.
# ============================================================

class Teacher:
    def __init__(self, name: str):
        self.name = name


class Department:
    def __init__(self, name: str, teacher: Teacher):
        self.name = name
        self.teacher = teacher

    def show_details(self) -> None:
        print(f"Department: {self.name}")
        print(f"Teacher: {self.teacher.name}")


def demonstrate_aggregation() -> None:
    print("\n=== 10. Aggregation ===")

    # Create the teacher separately from the department.
    teacher = Teacher("Meera")
    department = Department("Computer Science", teacher)

    department.show_details()

    # The teacher object is still independently accessible.
    print(f"Teacher exists independently: {teacher.name}")


# ============================================================
# MAIN FUNCTION
# Run all OOP demonstrations in sequence.
# ============================================================

def main() -> None:
    demonstrate_encapsulation()
    demonstrate_single_inheritance()
    demonstrate_multiple_inheritance()
    demonstrate_multilevel_inheritance()
    demonstrate_hierarchical_inheritance()
    demonstrate_polymorphism_and_overriding()
    demonstrate_default_argument_overloading()
    demonstrate_composition()
    demonstrate_aggregation()


# Execute main() only when this file is run directly.
if __name__ == "__main__":
    main()
