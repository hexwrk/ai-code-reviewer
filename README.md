# Code Review Assistant

Automatically checks your Python code for security issues before each Git commit.

## What it does

Scans for common security problems:
- Hardcoded passwords and API keys
- SQL injection vulnerabilities
- Unsafe command execution
- Weak cryptographic functions

## Installation
```bash
git clone https://github.com/hexwrk/ai-code-reviewer.git
cd ai-code-reviewer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set up the Git hook:
```bash
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
python3 src/hooks/pre_commit.py
HOOK

chmod +x .git/hooks/pre-commit
```

## Usage

The tool runs automatically when you commit:
```bash
git add your_file.py
git commit -m "your message"
```

If it finds issues, it'll block the commit and show you what's wrong.

To skip the check (not recommended):
```bash
git commit --no-verify -m "your message"
```

## How it works

The scanner uses regex patterns to find problematic code. For example, it catches things like:
```python
# BAD - hardcoded password
password = "admin123"

# BAD - SQL injection risk
query = "SELECT * FROM users WHERE id = " + user_id

# GOOD - parameterized query
query = "SELECT * FROM users WHERE id = ?"
params = (user_id,)
```

## Project structure
```
src/
├── security_scanner.py   # Pattern matching logic
├── git_integration.py    # Git workflow handling
└── hooks/
    └── pre_commit.py     # Hook entry point
```

## Customization

Edit `config/rules.yaml` to adjust what gets flagged.

## Running tests
```bash
python src/security_scanner.py
```

## Notes

The scanner checks Python files only. It uses simple pattern matching, so it might miss complex issues or flag false positives.
