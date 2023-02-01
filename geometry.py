from math import sqrt
class Line:
    def __init__ (self, a, b):
        self.A = a
        self.B = b

    def __str__ (self):
        return f"({self.A},{self.B})"

    def __get_item__ (self, key):
        return self.A if key == 0 else self.B

class Point:
    def __init__ (self, name, location):
        self.name = name
        self.location = location
    
    def __str__ (self):
        return f"{self.name} : {self.location}"
    
    def __get_item__ (self, key):
        return self.location[key]
