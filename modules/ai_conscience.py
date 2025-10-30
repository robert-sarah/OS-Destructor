#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Conscience Module - Local conversational AI for all projects
"""
from transformers import pipeline

class AIConscience:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.chatbot = pipeline("conversational", model=model_name)

    def ask(self, message):
        result = self.chatbot(message)
        # Pour transformers >=4.30, le résultat est une liste de dicts
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        # Pour d'autres versions, fallback
        return str(result)

if __name__ == "__main__":
    ai = AIConscience()
    while True:
        msg = input("Vous: ")
        print("IA:", ai.ask(msg))
