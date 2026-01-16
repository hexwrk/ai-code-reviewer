import os
from openai import OpenAI
from typing import Dict, Any, List
import yaml


class CodeReviewer:
    """Analyzes code quality and provides improvement suggestions."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
        self.load_rules()
    
    def load_rules(self):
        try:
            with open('config/rules.yaml', 'r') as f:
                self.rules = yaml.safe_load(f)
        except FileNotFoundError:
            self.rules = {
                'max_function_length': 50,
                'require_docstrings': True,
                'security_checks': True,
            }
    
    def review_code(self, code: str, file_path: str) -> Dict[str, Any]:
        print(f"Reviewing {file_path}...")
        
        results = {
            'file': file_path,
            'suggestions': [],
            'score': 0
        }
        
        if self.client:
            results['suggestions'] = self.get_ai_suggestions(code, file_path)
        
        results['score'] = max(0, 100 - len(results['suggestions']) * 10)
        
        return results
    
    def get_ai_suggestions(self, code: str, file_path: str) -> List[str]:
        prompt = f"""Review this Python code and provide 3-5 specific improvement suggestions.

File: {file_path}

Code:
```python
{code}
```

Focus on code quality, potential bugs, best practices, and security.
Provide suggestions as a numbered list."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Be concise and specific."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            suggestions = [line.strip() for line in content.split('\n') 
                          if line.strip() and line[0].isdigit()]
            return suggestions[:5]
            
        except Exception as e:
            return [f"Error getting AI suggestions: {str(e)}"]


if __name__ == '__main__':
    test_code = """
def add(a, b):
    return a + b
"""
    
    try:
        reviewer = CodeReviewer()
        result = reviewer.review_code(test_code, "test.py")
        print(f"\nReview complete.")
        print(f"Score: {result['score']}/100")
        print(f"\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"{i}. {suggestion}")
    except Exception as e:
        print(f"Error: {e}")
