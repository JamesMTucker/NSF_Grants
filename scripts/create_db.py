import sqlite3 as sql
import os
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@dataclass
class NSFDb:
    db_name: str = 'nsf.db'
    nsf_id: str = 'nsf_id'
    title: str = 'title'
    abstract: str = 'abstract'
    pi: str = 'pi'
    agency: str = 'agency'
    
        
    logger.info(f'Creating database {db_name}')
    con: sql.Connection = sql.connect(Path(__file__).parents[1] / 'data' / db_name)
    cursor: sql.Cursor = con.cursor()
    
    def __post_init__(self):
        """Create database with defined tables"""
        
        def _create_id_tables():
            """Create the tables"""
            logger.info('Creating tables')
            self.cursor.executescript(f"""
                CREATE TABLE IF NOT EXISTS {self.nsf_id} (
                    idx INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT,
                    date TEXT,
                    dateStart TEXT,
                    dateEnd TEXT,
                    is_duplicate INTEGER
                );
                
                CREATE TABLE IF NOT EXISTS {self.title} (
                    idx INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT,
                    title TEXT,
                    CONSTRAINT fk_id
                        FOREIGN KEY (id)
                        REFERENCES {self.nsf_id}(id)
                        ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS {self.abstract} (
                    idx INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT,
                    abstract TEXT,
                    CONSTRAINT fk_id
                        FOREIGN KEY (id)
                        REFERENCES {self.nsf_id}(id)
                        ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS {self.pi} (
                    idx INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    CONSTRAINT fk_id
                        FOREIGN KEY (id)
                        REFERENCES {self.nsf_id}(id)
                        ON DELETE CASCADE
                );
                
                CREATE INDEX IF NOT EXISTS idx_{self.nsf_id}_id ON {self.nsf_id}(id, date, dateStart, dateEnd);
                CREATE INDEX IF NOT EXISTS idx_{self.title}_id ON {self.title}(id, title);
                CREATE INDEX IF NOT EXISTS idx_{self.abstract}_id ON {self.abstract}(id, abstract);
                CREATE INDEX IF NOT EXISTS idx_{self.pi}_id ON {self.pi}(id, first_name, last_name, email);
                
            """)

        # create the database
        _create_id_tables(self.cursor)
        self.con.commit()
        self.con.close()
        
        
if __name__ == '__main__':
    db = NSFDb('nsf.db')