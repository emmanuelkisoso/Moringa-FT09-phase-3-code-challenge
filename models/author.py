class Author:
    def __init__(self, name):
        self._id = None
        self._name = None
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("id must be an interger")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("name must not be a non-empty string")
        if hasattr(self, value):
            raise AttributeError("name cannot be changed after initialization")
        self._name = value

    def __repr__(self):
        return f'<Author {self.name}>'
