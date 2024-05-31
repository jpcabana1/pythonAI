from abc import ABC, abstractmethod
from classes.Inheritance.circle import Circle
from classes.Inheritance.retangle import Rectangle
from classes.Inheritance.retangle import Rectangle
from classes.Inheritance.shape import Shape

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass
    
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Cow(Animal):
    def speak(self):
        return "Moo!"

class Bulldog(Dog):
    def speak(self):
        return "Woof Woof!"

def get_all_subclasses(cls):
    subclasses = set(cls.__subclasses__())
    for subclass in cls.__subclasses__():
        subclasses.update(get_all_subclasses(subclass))
    
    factory = dict()
    
    for sub in subclasses:
        print(f"{sub.__name__}, {sub().speak()}")
        #factory[str(sub.__name__)] = sub()
        # instance = sub() 
        # factory[sub.__name__] = instance
        #print(f"{sub.__name__}: {instance.speak()}")
    return factory

if __name__ == "__main__":
    all_subclasses = get_all_subclasses(Animal)
    print(all_subclasses)

