"""
HobZ - Agents
"""

from typing import Dict, List


class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def think(self, task: str, context: Dict) -> str:
        # نسخة مبسطة بدون Ollama (لأن Streamlit Cloud لا يدعمه)
        return f"[{self.name} - {self.role}]: تم تحليل المهمة بنجاح. السياق يحتوي على {len(context)} عنصر."


class AgentTeam:
    def __init__(self):
        self.agents = [
            Agent("محلل", "تحليل البيانات والعلاقات"),
            Agent("ناقد", "مراجعة النتائج والتحقق من صحتها"),
            Agent("متنبئ", "توليد التنبؤات النهائية"),
        ]

    def run_consultation(self, task: str, context: Dict) -> List[Dict]:
        results = []
        for agent in self.agents:
            response = agent.think(task, context)
            results.append({
                "agent": agent.name,
                "role": agent.role,
                "response": response
            })
        return results
