from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category
        self._create_in_db()

    def _create_in_db(self):
        # method to create magazine entry in the database.
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
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
        if not isinstance(new_name, str) or len(new_name) < 2 or len(new_name) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str) or len(new_category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = new_category

    def articles(self):
        # Get all articles associated with the magazine.
        from .article import Article
        from .author import Author
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
            return [Article(Author(row[3], None), self, row[1], row[2]) for row in rows]

    def contributors(self):
        # Get all authors who have contributed to the magazine.
        from .author import Author
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT a.* FROM authors a JOIN articles ar ON a.id = ar.author_id WHERE ar.magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
            return [Author(row[0], row[1]) for row in rows]

    def article_titles(self):
        # Get the titles of all articles associated with the magazine.
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
            return [row[0] for row in rows] if rows else None

    def contributing_authors(self):
        from .author import Author

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.name
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            authors = cursor.fetchall()

        # Filter authors who have written more than 2 articles
        contributing_authors = [Author(id_, name) for id_, name in authors]
        return contributing_authors if len(contributing_authors) > 2 else None