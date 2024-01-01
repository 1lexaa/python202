# Основи ООП

class Point :                  # Оголошення класу
    x = 0                      # поля, описані у класі є відкритими
    y = 0                      # та ! статичними.
                               # 
                               # 
def demo1() -> None :          # 
    p1 = Point()               # Особливість: оператор new не
    p2 = Point()               # зазначається, тільки назва класу
    print(p1.x, p2.x, Point.x) # 0 0 0
    Point.x = 10               # На даному етапі р1 не має поля "х", тому береться більш "глобальне" - поле класу
    print(p1.x, p2.x, Point.x) # 10 10 10
    p1.x = 20                  # Створення об'єктного (локального) поля "х", яке приховує класове (статичне)
    print(p1.x, p2.x, Point.x) # 20 10 10
    Point.x = 30               #
    print(p1.x, p2.x, Point.x) # 20 30 30
    del p1.x                   # Видаляємо об'єктне поле, але статичне (класове) залишається
    print(p1.x, p2.x, Point.x) # 30 30 30


class Vector :                   # Для того щоб створити об'єктні поля необхідний
                                 # екземпляр (instance) об'єкту. Він з'являється у
    def __init__( self,          # конструкторі. У Python конструктор - спец. метод __init__
           x:float=0,            # На відміну від неявного this використовується явний self 
           y:float=0 ) -> None:  # self є першим параметром усіх методів, звернення до 
        self.x = x               # полів та інших методів мають починатись з self.
        self.y = y               # В силу відсутності перевантаження, "різницю" у 
                                 # конструкторах також реалізують значеннями за замовчанням
    def __str__(self) -> str:    # ~ ToString() - викликається при виводі, у рядкових
        return f"({self.x}, {self.y})"  # операціях та приведення до рядкового типу

    def __repr__(self) -> str:   # representation - аналог __str__ але для "строгого" виведення
        return f"<Vector>({self.x}, {self.y})"
    
    def __add__(self, other) :   # "перевантаження" операторів - опис спец. методів.
        if isinstance( other, Vector ) :
            return Vector( self.x + other.x, self.y + other.y )
        else :
            raise ValueError( "Incompatable type: Vector required" )
        
    def __mul__(self, other) :     # демонструємо операції з різними типами
        if isinstance( other, (int, float) ) :   # множення вектора на число
            return Vector( self.x * other, self.y * other )
        elif isinstance( other, Vector ) :       # скалярне множення вектора на вектор
            return self.x * other.x + self.y * other.y
        else :
            raise ValueError( "Incompatable type: Vector or number required" )
    
    def magnitude(self) -> float :
        return (self.x * self.x + self.y * self.y) ** (1/2)

    def translate(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy



def demo2() -> None :
    v1 = Vector()
    v2 = Vector( 1 )
    v3 = Vector( 1, -1 )
    v4 = Vector( y=-1 )
    print(v3, v4, v3 + v4 )
    print( v3.magnitude() )    # при виклику метода self пропускається
    v3.translate(0.1, 0.2)
    print( "v3 translated =", v3 )
    print( "v3 * 2 =", v3 * 2 )
    print( "v3 * v2 =", v3 * v2 )


def main() -> None :           # 
    demo2()                    # 


if __name__ == "__main__" :
    main()

'''
Реалізувати роботу з числовими дробами
Оголосити клас Fraction {numerator:int, denominator:int}
Для нього реалізувати алгебраїчні операції (+-/*), а також
- представлення для виведення на екран у форматі [2/3]
- метод представлення у JSON
- метод видобутку з JSON з аналізом на структуру JSON (наявність потрібних полів)
   f1 = Fraction.fromJson("{n:2, d:3}") -- OK
   f1 = Fraction.fromJson('{str:"Hello"}') -- Invalid (Error)
- збереження у файлі
- відновлення з файлу з обробкою виняткових ситуацій (викид виключення)
- метод скорочення дробу ([4/6].reduce() -> [2/3])
'''