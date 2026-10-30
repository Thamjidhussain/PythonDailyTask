# 1.Single Responsibility Principle(SRP)
# A class should have only one responsibility.

class Employee:
    def __init__(self,name,salary):
        self.name=name
        self.salary=salary
class SalartRport:
    def generate(self,employee):
        return f"Employee:{employee.name},Salary:{employee.salary}"

# 2. Open/Closed Principle (OCP)
# Classes should be open for extension but closed for modification.

class Discount:
    def calculate(self,amount):
        raise NotImplementedError("Subclass must implement calculate()")
class RegularDiscount(Discount):
    def calculate(self, amount):
        return amount*0.05
class PremimumDiscount(Discount):
    def calculate(self, amount):
        return amount*0.15
def final_price(amount,discount):
    return amount-discount.calculate(amount)
# 3. Liskov Substitution Principle (LSP)
# A child class should be usable wherever its parent is expected.

class Bird:
    def move(self):
        return "Bird is moving"
class Sparrow(Bird):
    def move(self):
        return "Sparrow is flying"
def make_bird_move(bird):
    print(bird.move())

# 4. Interface Segregation Principle (ISP)
# Classes should not be forced to implement methods they do not need.
class Printer:
    def print_document(self,document):
        return f"Printing:{document}"
class Scanner:
    def scan_document(self,document):
        return f"Scanning:{document}"

class MultiFunctionDevice(Printer,Scanner):
    pass
class EmailNotifier:
    def send(self,message):
        return f"Email sent:{message}"
class SMSNotifier:
    def send(self,message):
        return f"SMS sent:{message}"
class OrderService:
    def __init__(self,notifier):
        self.notifier=notifier

    def place_order(self,order_id):
        return self.notifier.send(f"Oder{order_id} placed successfully")
if __name__=="__main__":
    print("1.single Responsiblity Principle")
    emp1=Employee("rahul",30000)
    report=SalartRport()
    print(report.generate(emp1))
    print("\n2. Open/Closed Principle")
    print(f"Regular customer price: {final_price(1000,RegularDiscount())}")
    print(f"Premimum customer price: {final_price(1000,PremimumDiscount())}")
    print("\n 3.Liskov Substitution Principle")
    make_bird_move(Sparrow())
    print("\n4. Interface Segregation Principle")
    device=MultiFunctionDevice()
    print(device.print_document("Report"))
    print(device.scan_document("Report"))
    print("\n5. Dependency Inversion Principle")
    email_service=OrderService(EmailNotifier())
    sms_service=OrderService(SMSNotifier())
    print(email_service.place_order(101))
    print(sms_service.place_order(102))