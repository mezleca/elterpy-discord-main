import sqlite3
import json

from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = f"{db_name}.db"
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table(self, table_name: str):
        self.connect()
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data JSON
            )
        ''')
        self.conn.commit()
        self.disconnect()

    def insert(self, table_name: str, data: Dict):
        self.connect()
        json_data = json.dumps(data)
        self.cursor.execute(f"INSERT INTO {table_name} (data) VALUES (?)", (json_data,))
        self.conn.commit()
        self.disconnect()

    def get_all(self, table_name: str) -> List[Dict]:
        self.connect()
        self.cursor.execute(f"SELECT data FROM {table_name}")
        results = self.cursor.fetchall()
        self.disconnect()
        
        return [json.loads(row[0]) for row in results]

    def get_by_id(self, table_name: str, id: int) -> Optional[Dict]:
        self.connect()
        self.cursor.execute(f"SELECT data FROM {table_name} WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        self.disconnect()
        
        return json.loads(result[0]) if result else None