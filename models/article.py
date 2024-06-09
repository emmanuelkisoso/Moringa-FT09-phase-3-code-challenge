from database.connection import get_db_connection
from database.setup import create_tables

class Article:
    def __init__(self, title, content, author_id, magazine_id):
        self._id = None
        self._title = None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

        create_tables()

        conn = get_db_connection()
        cursor = get_db_connection()
        cursor.execute("INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)", (self._author_id, self._magazine_id, self._title))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            return TypeError("must be an integer")
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not ( 5 >= len(value) <= 50 ):
            raise ValueError("tile must be a string between 5 and 50 characters inclusive")
        if hasattr(self, value):
            raise AttributeError("title cannot be changed after initialization")
        self._title = value

    def __repr__(self):
        return f'<Article {self.title}>'
