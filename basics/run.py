from classes.Inheritance.circle import Circle
from classes.Inheritance.retangle import Rectangle

def main():
    shapes = [Rectangle(3, 4), Circle(5)]
    for shape in shapes:
        print(shape.area())

if __name__ == '__main__':
    main()