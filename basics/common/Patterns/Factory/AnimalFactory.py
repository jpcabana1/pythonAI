from common.Patterns.Factory.Factory import Factory
from common.Patterns.Factory.Cat import Cat
from common.Patterns.Factory.Dog import Dog
from common.Patterns.Factory.Cow import Cow
from common.Patterns.Factory.Bulldog import Bulldog
from common.Patterns.Factory.Animal import Animal

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
