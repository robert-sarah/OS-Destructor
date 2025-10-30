#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Conscience Module - Local conversational AI for all projects
"""
from transformers import pipeline, Conversation

class AIConscience:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.chatbot = pipeline("conversational", model=model_name)

    def ask(self, message):
        conv = Conversation(message)
        result = self.chatbot(conv)
        return result.generated_responses[-1]

if __name__ == "__main__":
    ai = AIConscience()
    while True:
        msg = input("Vous: ")
        print("IA:", ai.ask(msg))
