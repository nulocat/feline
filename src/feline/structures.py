class AttributeDict:
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None
