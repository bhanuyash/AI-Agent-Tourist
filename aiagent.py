import json
import os
from openai import OpenAI
import google.generativeai as genai

with open("keys.json", "r") as f:
        keys = json.load(f)

class AI_AGENT():
    def __init__(self):
        self.open_ai_client = OpenAI(api_key=keys["open_ai_subscription_key"])
        self.open_ai_model = "gpt-3.5-turbo"
        genai.configure(api_key=keys["gemini_api_key"])
        self.gemini_model = genai.GenerativeModel('gemini-1.0-pro')
        
        
    def open_ai_completion(self, system_prompt, user_prompt):
        completion = self.open_ai_client.chat.completions.create(
            model=self.open_ai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
                ]
        )
        return completion.choices[0].message.content
    
    def gemini_completion(self, system_prompt, user_prompt):
        
        response = self.gemini_model.generate_content(system_prompt + user_prompt)
        
        return response.text
