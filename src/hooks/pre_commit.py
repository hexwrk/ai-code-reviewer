#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.git_integration import GitIntegration


def main():
    print("\nRunning code review...\n")
    
    git_int = GitIntegration()
    results = git_int.review_staged_files()
    report = git_int.generate_report(results)
    
    print(report)
    
    if results['total_issues'] > 0:
        print("\nCode review failed. Please fix the issues above.")
        print("Tip: Use 'git commit --no-verify' to bypass this check.")
        return 1
    
    print("\nCode review passed. Proceeding with commit.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
