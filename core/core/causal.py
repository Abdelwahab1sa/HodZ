"""
HobZ - Causal Engine (Simplified)
"""

import sqlite3
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CausalRelation:
    cause: str
    effect: str
    strength: float
    mechanism: str


class CausalEngine:
    def __init__(self, db_path="hobz_causal.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS causal_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cause TEXT,
                effect TEXT,
                strength REAL,
                mechanism TEXT,
                UNIQUE(cause, effect)
            )
        ''')
        conn.commit()
        conn.close()

    def add_relation(self, cause: str, effect: str, strength: float, mechanism: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO causal_relations (cause, effect, strength, mechanism)
            VALUES (?, ?, ?, ?)
        ''', (cause, effect, strength, mechanism))
        conn.commit()
        conn.close()

    def get_causes(self, effect: str) -> List[CausalRelation]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT cause, effect, strength, mechanism FROM causal_relations WHERE effect = ?', (effect,))
        rows = c.fetchall()
        conn.close()
        return [CausalRelation(r[0], r[1], r[2], r[3]) for r in rows]

    def predict(self, scenario: str, factors: List[Dict]) -> Tuple[str, float]:
        if not factors:
            return "لا توجد بيانات كافية للتنبؤ", 0.0

        avg_strength = sum(f.get('strength', 0.5) for f in factors) / len(factors)
        
        prediction = f"بناءً على تحليل {len(factors)} عامل، النتيجة المتوقعة هي: "
        
        if avg_strength > 0.7:
            prediction += "نتيجة قوية وموثوقة."
        elif avg_strength > 0.4:
            prediction += "نتيجة متوسطة الثقة."
        else:
            prediction += "نتيجة غير مؤكدة."

        return prediction, avg_strength

    def explain(self, effect: str) -> str:
        causes = self.get_causes(effect)
        if not causes:
            return f"لا توجد علاقات سببية معروفة لـ '{effect}'"

        explanation = [f"التفسير السببي لـ '{effect}':"]
        for cause in causes:
            explanation.append(f"  ← {cause.cause} (قوة: {cause.strength:.0%})")
            explanation.append(f"    الآلية: {cause.mechanism}")

        return "\n".join(explanation)
