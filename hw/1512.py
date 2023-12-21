import json

# <--====== Fraction sector. ======-->
class Fraction:
    def __init__(self, numerator, denominator) -> None:
        self.numerator = numerator
        self.denominator = denominator

        self.Reduce()

    def __str__(self) -> str:
        return f"[{self.numerator} / {self.denominator}]"
    
    def ToJson(self):  # Performs serialization (transformation into string) of the Fraction object into JSON format.
        return json.dumps(
            {
                'n': self.numerator,
                "d": self.denominator
            })
    
    @classmethod
    def FormJson(cls, json_str):  # Does the inverse of ToJson - it converts the JSON string back into a Fraction object.
        try:
            data = json.loads(json_str)

            if "n" in data and "d" in data:
                return cls(data["n"], data["d"])
            else:
                raise ValueError("Invalid JSON format")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON")
        
    def SaveToFile(self, filename):  # This method is used to save the Fraction object to a file in JSON format.
        with open(filename, 'w') as file:
            file.write(self.ToJson())

    @classmethod
    def LoadFromFile(cls, filename):  # Fraction abbreviations
        try:
            with open(filename, 'r') as file:
                json_str = file.read()
                return cls.FormJson(json_str)
        except FileNotFoundError:
            raise ValueError(f"File {filename} not found")
        except ValueError as e:
            raise ValueError(f"Error loading fraction from file: {e}")
    
    def Reduce(self):
        gcd = self.GCD(self.numerator, self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd

    @staticmethod
    def GCD(a, b):
        while b:
            a, b = b, a % b
        return a
    
    # <--====== Arithmetic operations sector. ======-->
    def __add__(self, other):
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator

        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other):
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator

        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator

        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator

        return Fraction(new_numerator, new_denominator)
    
# <--====== Custom code sector. ======-->
f1 = Fraction(2, 3)
f2 = Fraction(1, 4)

print(f"f1 = {f1}")
print(f"f2 = {f2}")
print(f"{f1} + {f2} = {f1 + f2}")
print(f"{f1} - {f2} = {f1 - f2}")
print(f"{f1} * {f2} = {f1 * f2}")
print(f"{f1} / {f2} = {f1 / f2}")

json_str = f1.ToJson()

print(f"💾 Write to json file ({json_str})")

f3 = Fraction.FormJson(json_str)

print(f"📨 Read from file{f3}")

try:
    f1.SaveToFile("fraction.json")

    f4 = Fraction.LoadFromFile("fraction.json")

    print(str(f4))
except ValueError as ex:
    print(ex)