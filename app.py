import os
import google.generativeai as genai
from pathlib import Path

class MCPHandler:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.contexts = self._load_contexts()
    
    def _load_contexts(self):
        """Load all .context files"""
        context_dir = Path("contexts")
        return {
            file.stem: file.read_text() 
            for file in context_dir.glob("*.context")
        }
    
    def generate_response(self, prompt, context_name):
        """Generate response using specified context"""
        if context_name not in self.contexts:
            return f"Error: Context '{context_name}' not found"
        
        full_prompt = f"{self.contexts[context_name]}\n\nUser: {prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text

if __name__ == "__main__":
    mcp = MCPHandler()
    print("Available contexts:", ", ".join(mcp.contexts.keys()))
    
    while True:
        context = input("\nChoose context: ")
        prompt = input("Your prompt: ")
        if prompt.lower() in ['exit', 'quit']: break
        print("\nResponse:", mcp.generate_response(prompt, context))



