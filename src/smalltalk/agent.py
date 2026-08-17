"""
#Gyan Labs - Conversational Small-talk Agent
============================================
Handles conversational pleasantries, company identity, capabilities, and guidance.
"""

from typing import Optional
from src.config import GROQ_API_KEY, DEFAULT_LLM_MODEL


CONVERSATIONAL_PROMPT = """You are the friendly, expert AI Assistant for #Gyan Labs (HashGyan Technologies).
You help enterprise clients, ML engineers, and researchers explore our high-performance AI hardware catalog,
query real-time stock/pricing via SQL, track orders, and answer warranty/SLA policies.

Respond warmly, concisely, and informatively in 1-3 sentences.

USER: {question}
ASSISTANT:"""


class SmallTalkAgent:
    def __init__(self, model_name: str = DEFAULT_LLM_MODEL):
        self.model_name = model_name
        self.groq_client = None

        if GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception:
                self.groq_client = None

    def talk(self, query: str) -> str:
        """
        Generates conversational response using LLM or intelligent rule fallback.
        """
        if self.groq_client:
            try:
                prompt = CONVERSATIONAL_PROMPT.format(question=query)
                completion = self.groq_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=150
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"Warning: Smalltalk LLM failed: {e}")

        # Intelligent Rule-Based Fallback
        q = query.lower()
        if "who are you" in q or "what are you" in q or "your name" in q:
            return "I am the **#Gyan Labs AI Commerce & Hardware Assistant**! I can help you search GPU servers, compare workstations, run database queries, check warranties, or track orders."
        elif "how are you" in q:
            return "I'm doing great and ready to assist you! Are you looking for NVIDIA GPU servers, developer workstations, or tracking an existing shipment today?"
        elif "thank" in q:
            return "You're very welcome! Let me know if you need any further assistance with #Gyan Labs AI hardware or cloud compute."
        else:
            return "Hello! I am your #Gyan Labs Commerce Assistant. How can I help you with our GPU servers, AI developer workstations, or order tracking today?"
