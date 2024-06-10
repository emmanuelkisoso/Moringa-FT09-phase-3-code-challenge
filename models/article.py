from database.connection import get_db_connection

class Article:
    def __init__(self, author, magazine, title, content, id=None):
        self._author = author
        self._magazine = magazine
        self._title = title
        self._content = content
        self._id = id
         # If id is not provided, create the article in the database
        if self._id is None:
            self._create_in_db()

    def _create_in_db(self):
        # Create the article record in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (self._title, self._content, self._author.id, self._magazine.id)
        )
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if hasattr(self, '_title'):
            raise ValueError("Title cannot be changed after instantiation.")
        if not isinstance(new_title, str) or len(new_title) < 5 or len(new_title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._title = new_title

    @property
    def author(self):
        # Get the author of the article
        from .author import Author  # Local import to avoid circular import
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE id = ?", (self._author.id,))
            row = cursor.fetchone()
            return Author(row[0], row[1])

    @property
    def magazine(self):
        # Get the magazine of the article
        from .magazine import Magazine  # Local import to avoid circular import
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (self._magazine.id,))
            row = cursor.fetchone()
            return Magazine(row[0], row[1], row[2])
