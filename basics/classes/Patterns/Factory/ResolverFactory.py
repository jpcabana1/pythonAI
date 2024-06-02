from classes.Patterns.Factory.Factory import Factory

class ResolverFactory(Factory):
    def create(self, name: str, cls):
        all_subclasses = self.get_all_subclasses(cls)
        for sub in all_subclasses:
            if name == sub.__name__:
                return sub()
        return None if len(list(all_subclasses)) == 0 else list(all_subclasses)[0]()
    
    def get_all_subclasses(self, cls):
        subclasses = set(cls.__subclasses__())
        for subclass in cls.__subclasses__():
            subclasses.update(self.get_all_subclasses(subclass))
        return subclasses
    