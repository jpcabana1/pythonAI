from classes.Patterns.Factory.Animal import Animal
from classes.Patterns.Factory.ResolverFactory import ResolverFactory

class AnimalFactory(ResolverFactory):
    def create_animal(self, name):
        return super().create(name, Animal)    
