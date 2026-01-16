import git
import os
from pathlib import Path
from typing import List, Dict
from src.security_scanner import SecurityScanner


class GitIntegration:
    """Integrates code review with Git workflow."""
    
    def __init__(self, repo_path: str = '.'):
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            print("Not a git repository. Initializing...")
            self.repo = git.Repo.init(repo_path)
        
        self.scanner = SecurityScanner()
    
    def get_staged_files(self) -> List[str]:
        changed_files = []
        
        try:
            staged = self.repo.index.diff("HEAD")
            for item in staged:
                if item.a_path and item.a_path.endswith('.py'):
                    changed_files.append(item.a_path)
        except:
            for item in self.repo.index.entries:
                if item[0].endswith('.py'):
                    changed_files.append(item[0])
        
        return changed_files
    
    def review_staged_files(self) -> Dict:
        results = {
            'files_reviewed': 0,
            'total_issues': 0,
            'files': []
        }
        
        staged_files = self.get_staged_files()
        
        if not staged_files:
            print("No Python files staged for commit")
            return results
        
        for file_path in staged_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    code = f.read()
                
                print(f"\nReviewing {file_path}...")
                security_issues = self.scanner.scan_code(code, file_path)
                
                file_result = {
                    'path': file_path,
                    'security_issues': security_issues,
                    'passed': len(security_issues) == 0
                }
                
                results['files'].append(file_result)
                results['total_issues'] += len(security_issues)
        
        results['files_reviewed'] = len(staged_files)
        return results
    
    def generate_report(self, results: Dict) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append("CODE REVIEW REPORT")
        lines.append("=" * 70)
        lines.append(f"\nFiles Reviewed: {results['files_reviewed']}")
        lines.append(f"Total Issues: {results['total_issues']}")
        
        if results['total_issues'] > 0:
            lines.append("\n" + "=" * 70)
            lines.append("ISSUES FOUND:")
            lines.append("=" * 70)
        
        for file_data in results['files']:
            if not file_data['passed']:
                lines.append(f"\nFile: {file_data['path']}")
                lines.append(f"Status: FAIL")
                
                for issue in file_data['security_issues']:
                    lines.append(f"\n  Line {issue['line']}: {issue['message']}")
                    lines.append(f"  Code: {issue['code']}")
                
                lines.append("\n" + "-" * 70)
        
        if results['total_issues'] == 0:
            lines.append("\nAll files passed security review.")
        
        return '\n'.join(lines)


if __name__ == '__main__':
    git_int = GitIntegration()
    results = git_int.review_staged_files()
    report = git_int.generate_report(results)
    print(report)
