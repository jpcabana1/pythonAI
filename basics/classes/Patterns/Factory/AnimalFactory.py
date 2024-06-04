from classes.Patterns.Factory.Factory import Factory
from classes.Patterns.Factory.Cat import Cat
from classes.Patterns.Factory.Dog import Dog
from classes.Patterns.Factory.Cow import Cow
from classes.Patterns.Factory.Bulldog import Bulldog
from classes.Patterns.Factory.Animal import Animal

class AnimalFactory(Factory):
    
    def __init__(self) -> None:
        self.__animals = {
            "Bulldog": Bulldog,
            "Cat": Cat,
            "Cow": Cow,
            "Dog": Dog
        }    
               
    def create(self, name) -> Animal:
        return self.__animals.get("Bulldog")() if self.__animals.get(name)() == None else self.__animals.get(name)()
