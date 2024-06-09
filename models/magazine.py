class Magazine:
    def __init__(self, name, category):
        self._id = None
        self._name = None
        self.name = name
        self._category = None
        self.category = category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 >= len(value) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters,inclusive")
        self._name(value)

    @property
    def catergory(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("category must not be an empty string")
        self._category = value

    def __repr__(self):
        return f'<Magazine {self.name}>'
