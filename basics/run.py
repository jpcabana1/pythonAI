from classes.circle import Circle
from classes.retangle import Rectangle

def main():
    print("Hello!")
    shapes = [Rectangle(3, 4), Circle(5)]
    for shape in shapes:
        print(shape.area())

if __name__ == '__main__':
    main()