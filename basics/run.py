from classes.Patterns.Factory.AnimalFactory import AnimalFactory

if __name__ == "__main__":
    factory = AnimalFactory()
    animal = factory.create("Cat")
    print("Animal returned None" if animal == None else animal.speak())
