# Story 1 – Python OOP Fundamentals

## 1. Introduction to Object-Oriented Programming

Object-Oriented Programming (OOP) is a programming approach that organizes code using classes and objects. It helps developers write reusable, maintainable, and organized code.

Python supports OOP concepts such as classes, objects, constructors, instance variables, class variables, methods, and object lifecycle management.

### Why is OOP used?

- Code reusability
- Better organization
- Easy maintenance
- Real-world modeling
- Data and behavior can be grouped together

**Real-world example:** An employee has data such as name, employee ID, and salary. An employee can also perform actions such as displaying details or calculating a bonus. A Python class can represent these properties and actions.

---

## 2. Classes and Objects

### What is a class?

A class is a blueprint or template used to create objects. It defines the data and behavior that its objects can have.

### What is an object?

An object is an instance of a class. Each object can hold its own data.

### Example

```python
class Employee:
    def display(self):
        print("Employee details")


emp1 = Employee()
emp2 = Employee()

emp1.display()
emp2.display()
```

**Output:**

```text
Employee details
Employee details
```

### Diagram

```text
            Employee Class
                 |
          -----------------
          |               |
       Object 1         Object 2
        emp1              emp2
          |               |
      Employee A       Employee B
```

### Real-world example

A `Car` class defines common properties such as brand and color. Individual car objects can represent a Honda, Toyota, or Hyundai.

### Class vs Object

| Class | Object |
|---|---|
| Blueprint or template | Instance of a class |
| Defines attributes and methods | Holds actual attribute values |
| Created using the `class` keyword | Created by calling the class |
| Example: `Employee` | Example: `Employee()` |

---

## 3. Constructors – `__init__()`

A constructor-like initialization method in Python is `__init__()`. It is automatically called when a new instance is initialized.

It is commonly used to assign initial values to an object's attributes.

### Example

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print(self.name, self.salary)


emp1 = Employee("Rahul", 30000)
emp1.display()
```

**Output:**

```text
Rahul 30000
```

### Explanation

- `__init__()` initializes the instance.
- `self.name` stores the employee's name.
- `self.salary` stores the employee's salary.
- `"Rahul"` and `30000` are passed when creating the object.

### Types of initialization patterns

**1. No-argument initialization**

```python
class Student:
    def __init__(self):
        self.name = "Unknown"
```

**2. Parameterized initialization**

```python
class Student:
    def __init__(self, name):
        self.name = name
```

### `__init__()` vs `__new__()`

| `__init__()` | `__new__()` |
|---|---|
| Initializes a new instance | Creates and returns the instance |
| Receives the created instance as `self` | Receives the class as `cls` |
| Commonly used in everyday classes | Used in advanced object creation |

Note: `__init__()` is not the method that creates the object itself. Python generally calls `__new__()` first, followed by `__init__()`.

---

## 4. Instance Variables and Class Variables

Variables in a class can store information belonging to individual objects or information shared by the class.

### Instance variables

Instance variables belong to individual objects. They are usually defined using `self`.

### Class variables

Class variables belong to the class and are shared by instances unless an instance overrides the value with its own attribute.

### Example

```python
class Employee:
    company = "ABC Technologies"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


emp1 = Employee("Rahul", 30000)
emp2 = Employee("Priya", 40000)

print(emp1.name)
print(emp2.name)
print(emp1.company)
print(emp2.company)
```

**Output:**

```text
Rahul
Priya
ABC Technologies
ABC Technologies
```

### Diagram

```text
          Employee Class
          company = ABC Technologies
                  |
          -------------------
          |                 |
       Employee 1        Employee 2
       name: Rahul       name: Priya
       salary: 30000     salary: 40000
```

### Comparison

| Instance variable | Class variable |
|---|---|
| Belongs to an individual instance | Belongs to the class |
| Usually defined with `self` | Defined in the class body |
| Can differ between objects | Shared by instances by default |
| Example: employee name | Example: company name |

**Important:** If you assign `emp1.company = "XYZ"`, you normally create or update an instance attribute for `emp1`. It does not change `Employee.company` or the value seen through `emp2`.

---

## 5. Instance, Class, and Static Methods

Python supports three commonly used method types. They differ in how they receive information and what they are intended to do.

### A. Instance method

An instance method works with an individual object's data. Its first parameter is conventionally named `self`.

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def display(self):
        print("Employee:", self.name)


emp = Employee("Rahul")
emp.display()
```

**Output:**

```text
Employee: Rahul
```

### B. Class method

A class method receives the class as its first argument, conventionally named `cls`. It is defined using `@classmethod`.

```python
class Employee:
    company = "ABC Technologies"

    @classmethod
    def change_company(cls, name):
        cls.company = name


Employee.change_company("XYZ Technologies")
print(Employee.company)
```

**Output:**

```text
XYZ Technologies
```

Class methods are useful for operations involving class-level data and for alternative constructors.

### C. Static method

A static method does not automatically receive `self` or `cls`. It is defined using `@staticmethod` and is useful for related utility logic.

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b


print(Calculator.add(10, 20))
```

**Output:**

```text
30
```

### Method comparison

| Feature | Instance method | Class method | Static method |
|---|---|---|---|
| Decorator | None required | `@classmethod` | `@staticmethod` |
| First parameter | `self` | `cls` | No automatic parameter |
| Main purpose | Work with instance data | Work with class-level data | Related utility operation |
| Example | Display employee details | Change company name | Add two numbers |

### Real-world example

In an employee management application:

- An instance method displays a particular employee's details.
- A class method changes the company name for the class.
- A static method validates an employee ID format.

---

## 6. Understanding `self` and `cls`

### What is `self`?

`self` refers to the current instance on which an instance method is called. It allows the method to access that object's attributes and other instance methods.

`self` is a naming convention, not a Python keyword, but it should be used by convention.

```python
class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello", self.name)


student = Student("Aman")
student.greet()
```

**Output:**

```text
Hello Aman
```

### What is `cls`?

`cls` refers to the class received by a class method. It allows the method to access or modify class-level attributes.

```python
class Student:
    school = "ABC School"

    @classmethod
    def show_school(cls):
        print(cls.school)


Student.show_school()
```

**Output:**

```text
ABC School
```

### `self` vs `cls`

| `self` | `cls` |
|---|---|
| Refers to an instance | Refers to a class |
| Used in instance methods | Used in class methods |
| Accesses instance attributes | Accesses class attributes |
| Conventionally used as the first parameter of instance methods | Conventionally used as the first parameter of class methods |

---

## 7. Object Lifecycle

The object lifecycle describes the stages an object goes through, from creation to eventual cleanup.

### Main stages

1. **Class definition:** Python defines the class.
2. **Object creation:** Python creates an instance, generally through `__new__()`.
3. **Initialization:** Python calls `__init__()` to initialize the instance.
4. **Usage:** The program accesses the object's attributes and methods.
5. **Cleanup:** When an object is no longer needed, it may eventually be reclaimed by Python's memory management.

### Diagram

```text
       Define Class
            |
            v
      Create Object
        (__new__)
            |
            v
      Initialize Object
        (__init__)
            |
            v
       Use the Object
            |
            v
   Object Becomes Unreachable
            |
            v
    Memory Reclaimed Later
```

### Example

```python
class Demo:
    def __init__(self):
        print("Object initialized")

    def __del__(self):
        print("Cleanup method called")


obj = Demo()
print("Object is being used")

del obj
```

**Possible output:**

```text
Object initialized
Object is being used
Cleanup method called
```

The timing of `__del__()` is not guaranteed in every situation. It is a finalization hook, not a reliable replacement for explicit resource management.

**Best practice:** Use context managers, such as `with open(...)`, to manage files and other resources safely.

---

## 8. Practical Example – Employee Management

This example combines classes, objects, constructors, instance variables, class variables, and all three method types.

```python
class Employee:
    company = "ABC Technologies"
    employee_count = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.employee_count += 1

    def display(self):
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")
        print(f"Company: {self.company}")

    @classmethod
    def get_employee_count(cls):
        return cls.employee_count

    @staticmethod
    def is_valid_salary(salary):
        return isinstance(salary, (int, float)) and not isinstance(salary, bool) and salary >= 0


emp1 = Employee("Rahul", 30000)
emp2 = Employee("Priya", 40000)

emp1.display()
print("Employee count:", Employee.get_employee_count())
print("Valid salary:", Employee.is_valid_salary(30000))
```

**Output:**

```text
Name: Rahul
Salary: 30000
Company: ABC Technologies
Employee count: 2
Valid salary: True
```

### What this example demonstrates

- `Employee` is the class.
- `emp1` and `emp2` are objects.
- `__init__()` initializes each employee.
- `self.name` and `self.salary` are instance variables.
- `company` and `employee_count` are class variables.
- `display()` is an instance method.
- `get_employee_count()` is a class method.
- `is_valid_salary()` is a static method.

Note: The employee count is maintained through the class in this example. In a multithreaded application, concurrent updates may require additional synchronization.

---

## 9. Common Mistakes to Avoid

1. Forgetting `self` in an instance method definition.
2. Forgetting to use `@classmethod` when defining a class method.
3. Using `self` to represent the class when `cls` is appropriate.
4. Confusing class variables with instance variables.
5. Assuming `__init__()` creates the object itself.
6. Assuming `__del__()` always runs immediately.
7. Using mutable class variables, such as lists, when separate per-object data is required.

### Example of a class-variable mistake

```python
class Student:
    subjects = []  # Shared by all instances
```

If each student needs a separate list of subjects, define it inside `__init__()`:

```python
class Student:
    def __init__(self):
        self.subjects = []
```

---

## 10. Key Takeaways

- A class defines the structure and behavior of objects.
- An object is an instance of a class.
- `__init__()` initializes an instance.
- Instance variables store per-object data.
- Class variables hold class-level data shared by instances by default.
- Instance methods use `self`.
- Class methods use `cls` and `@classmethod`.
- Static methods use `@staticmethod` for related utility logic.
- Python manages object memory, but resource cleanup should be handled safely.

## 11. Practice Questions

1. What is the difference between a class and an object?
2. What is the purpose of `__init__()`?
3. What is the difference between an instance variable and a class variable?
4. What are `self` and `cls`?
5. Explain instance methods, class methods, and static methods.
6. What happens during the object lifecycle?
7. Why should `__del__()` not be relied upon for immediate cleanup?
8. Create a `BankAccount` class with account holder name, balance, deposit, and withdrawal methods.

## 12. Deliverable Checklist

- [ ] Created `oop_notes.md`
- [ ] Explained classes and objects
- [ ] Explained constructors and initialization
- [ ] Explained instance and class variables
- [ ] Covered instance, class, and static methods
- [ ] Explained `self` and `cls`
- [ ] Added object lifecycle diagram
- [ ] Included real-world employee management example
- [ ] Added comparisons and common mistakes
- [ ] Added practice questions
