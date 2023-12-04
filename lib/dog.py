import sqlite3

# Connection and cursor setup
CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        """Create the 'dogs' table in the database"""
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the 'dogs' table if it exists"""
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save a dog instance to the 'dogs' table"""
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

        # Update the instance's ID with the last inserted row ID
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        """Create and save a new dog record"""
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        """Create a new dog instance from a database row"""
        dog = cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )
        return dog

    @classmethod
    def get_all(cls):
        """Fetch all dogs from the 'dogs' table"""
        sql = """
            SELECT * FROM dogs
        """

        return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]

    @classmethod
    def find_by_name(cls, name):
        """Find a dog by name in the 'dogs' table"""
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        if not row:
            return None

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    @classmethod
    def find_by_id(cls, id):
        """Find a dog by ID in the 'dogs' table"""
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        if not row:
            return None

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        """Find a dog by name and breed or create a new one in the 'dogs' table"""
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    def update(self):
        """Update the dog's information in the 'dogs' table"""
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
    pass  