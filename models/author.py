from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._create_in_db()

    def _create_in_db(self):
        # method to create author entry in the database.
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if hasattr(self, '_name'):
            raise ValueError("Name cannot be changed after instantiation.")
        if not isinstance(new_name, str) or len(new_name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = new_name

    def articles(self):
        # Get all articles written by the author.
        from .article import Article
        from .magazine import Magazine
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            rows = cursor.fetchall()
            return [Article(self, Magazine(row[3], None, None), row[1], row[2]) for row in rows]

    def magazines(self):
        # Get all magazines for which the author has written articles.
        from .magazine import Magazine
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT m.* FROM magazines m JOIN articles a ON a.magazine_id = m.id WHERE a.author_id = ?", (self.id,))
            rows = cursor.fetchall()
            return [Magazine(row[0], row[1], row[2]) for row in rows]
