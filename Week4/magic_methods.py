class Product:
    def __init__(self,name,price,quantity):
        self.name=name
        self.price=price
        self.quantity=quantity
    def __str__(self):
        return f"{self.name} - Rs.{self.price}"
    def __repr__(self):
        return (f"Product(name={self.name!r},"f"price={self.price},quantity={self.quantity})")
    def __len__(self):
        return self.quantity
    def __eq__(self, other):
        if not isinstance(other,Product):
            return NotImplemented
        return self.price==other.price
    def __lt__(self, other):
        if not isinstance(other,Product):
            return NotImplemented
        return self.price<other.price
    def __gt__(self, other):
        if not isinstance(other,Product):
            return NotImplemented
        return self.price>other.price
    def __add__(self, other):
        if not isinstance(other,Product):
            return NotImplemented
        return Product(
            f"{self.name}+{other.name}",
            self.price+other.price,
            self.quantity+other.quantity
        )
    def __sub__(self, other):
        if not isinstance(other,Product):
            return NotImplemented
        return Product(
            f"{self.name}-{other.name}",
            self.price-other.price,
            self.quantity-other.quantity
        )
p1=Product("Laptop",50000,5)
p2=Product("Mouse",1000,10)
p3=Product("Laptop",50000,5)
print("1. __str__:",str(p1))
print("2. __repr__:", repr(p1))
print("3. __len__:", len(p1))
print("4. __eq__:", p1==p3)
print("5. __lt__:", p2<p1)
print("6. __gt__:",p1>p2)
added=p1+p2
print("7. __add__:", added)
subtracted=p1-p2
print("8. __sub__:",subtracted)