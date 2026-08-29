"""
HobZ - Unified Memory
"""

import sqlite3
from typing import List, Dict
from dataclasses import dataclass
import time


@dataclass
class MemoryItem:
    id: str
    content: str
    tags: str
    importance: float
    timestamp: float


class UnifiedMemory:
    def __init__(self, db_path="hobz_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                content TEXT,
                tags TEXT,
                importance REAL,
                timestamp REAL
            )
        ''')
        conn.commit()
        conn.close()

    def store(self, content: str, tags: List[str], importance: float = 0.5):
        item_id = f"mem_{int(time.time() * 1000)}"
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO memory (id, content, tags, importance, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_id, content, ",".join(tags), importance, time.time()))
        conn.commit()
        conn.close()
        return item_id

    def recall(self, query_tags: List[str], limit: int = 5) -> List[MemoryItem]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        tag_pattern = f"%{query_tags[0]}%" if query_tags else "%"
        query = '''
            SELECT id, content, tags, importance, timestamp
            FROM memory
            WHERE tags LIKE ?
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        '''
        c.execute(query, (tag_pattern, limit))
        rows = c.fetchall()
        conn.close()

        return [MemoryItem(r[0], r[1], r[2], r[3], r[4]) for r in rows]

    def get_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*), AVG(importance) FROM memory')
        row = c.fetchone()
        conn.close()
        return {
            "total_items": row[0] or 0,
            "avg_importance": row[1] or 0.0
        }
