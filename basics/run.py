from classes.Patterns.Factory.AnimalFactory import AnimalFactory

if __name__ == "__main__":
    print(AnimalFactory().create("Cat").speak())
