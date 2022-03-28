import os
import pathlib
import sqlite3
import tempfile

from pydantic_yaml import YamlModel


class ChangeLog(YamlModel):
    name: str
    sql: list[str]


class DBStructure(YamlModel):
    version: str
    changes: list[ChangeLog]


class DocumentDBEngine:

    # We need to be able to create a new document db engine this will initialize a
    # new SQLite database and the load the structure.yml and apply the changelog
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.is_new = True
        if db_path is not None:
            self.is_tmp = False
            path = pathlib.Path(db_path)
            if path.exists():
                # At this point we need to load the db
                self.is_new = False
        else:
            from kodexa import KodexaPlatform
            new_file, filename = tempfile.mkstemp(suffix='.kddb', dir=KodexaPlatform.get_tempdir())
            self.db_path = filename
            self.is_tmp = True

        self.current_filename = self.db_path

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def load_structure(self):
        structure = DBStructure.parse_file(os.path.join(os.path.dirname(__file__), "structure.yml"))
        for change in structure.changes:
            for sql in change.sql:
                self.cursor.executescript(sql)

    def close(self):
        self.connection.close()
