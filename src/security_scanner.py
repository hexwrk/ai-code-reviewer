import re
from typing import List, Dict


class SecurityScanner:
    """Scans code for common security vulnerabilities."""
    
    def __init__(self):
        self.patterns = {
            'hardcoded_secrets': [
                (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password detected'),
                (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key detected'),
                (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret detected'),
                (r'token\s*=\s*["\'][^"\']+["\']', 'Hardcoded token detected'),
            ],
            'sql_injection': [
                (r'execute\s*\(\s*["\'].*%s.*["\']', 'Possible SQL injection vulnerability'),
                (r'\.execute\s*\([^)]*\+[^)]*\)', 'SQL query concatenation detected'),
            ],
            'command_injection': [
                (r'os\.system\s*\(', 'Potentially unsafe os.system() call'),
                (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', 'Dangerous shell=True parameter'),
            ],
            'weak_crypto': [
                (r'hashlib\.md5\s*\(', 'MD5 is cryptographically broken'),
                (r'hashlib\.sha1\s*\(', 'SHA1 is weak, use SHA256 or higher'),
            ]
        }
    
    def scan_code(self, code: str, file_path: str) -> List[Dict]:
        warnings = []
        lines = code.split('\n')
        
        for category, patterns in self.patterns.items():
            for pattern, message in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        warnings.append({
                            'line': line_num,
                            'category': category,
                            'severity': 'HIGH',
                            'message': message,
                            'code': line.strip()
                        })
        
        return warnings


if __name__ == '__main__':
    scanner = SecurityScanner()
    
    vulnerable_code = """
password = "admin123"
api_key = "sk-1234567890"

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    
import os
os.system("ls " + user_input)
"""
    
    print("Security Scanner Test\n")
    warnings = scanner.scan_code(vulnerable_code, "test.py")
    
    if warnings:
        print(f"Found {len(warnings)} security issues:\n")
        for w in warnings:
            print(f"Line {w['line']}: {w['message']}")
            print(f"Code: {w['code']}\n")
    else:
        print("No security issues found.")
