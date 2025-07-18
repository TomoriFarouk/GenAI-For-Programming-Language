# backend/app/utils/code_analyzer.py
from typing import Optional
import os
import ast
import re
from typing import Dict, List, Any, Optional


class CodeAnalyzer:
    """Basic static code analysis utilities"""

    def __init__(self):
        self.python_analyzers = {
            'syntax': self._check_python_syntax,
            'complexity': self._check_python_complexity,
            'style': self._check_python_style
        }

    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code and return insights"""
        if language.lower() == 'python':
            return self._analyze_python_code(code)
        elif language.lower() == 'java':
            return self._analyze_java_code(code)
        elif language.lower() == 'javascript':
            return self._analyze_javascript_code(code)
        else:
            return {'issues': [], 'score_adjustment': 0}

    def _analyze_python_code(self, code: str) -> Dict[str, Any]:
        """Analyze Python code"""
        issues = []
        score_adjustment = 0

        # Check syntax
        syntax_issues = self._check_python_syntax(code)
        issues.extend(syntax_issues)

        # Check style
        style_issues = self._check_python_style(code)
        issues.extend(style_issues)

        # Check complexity
        complexity_issues = self._check_python_complexity(code)
        issues.extend(complexity_issues)

        # Calculate score adjustment
        score_adjustment = - \
            len([i for i in issues if i['severity'] == 'high']) * 10
        score_adjustment -= len([i for i in issues if i['severity']
                                == 'medium']) * 5
        score_adjustment -= len([i for i in issues if i['severity'] == 'low']) * 2

        return {
            'issues': issues,
            'score_adjustment': score_adjustment,
            'language': 'python'
        }

    def _check_python_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Check Python syntax"""
        issues = []

        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                'line_number': e.lineno,
                'description': f"Syntax error: {e.msg}",
                'suggestion': "Fix the syntax error to make the code runnable",
                'severity': 'high'
            })

        return issues

    def _check_python_style(self, code: str) -> List[Dict[str, Any]]:
        """Check Python style guidelines (basic PEP 8)"""
        issues = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 79:
                issues.append({
                    'line_number': i,
                    'description': f"Line too long ({len(line)} > 79 characters)",
                    'suggestion': "Break long lines to improve readability",
                    'severity': 'low'
                })

            # Check for missing spaces around operators
            if re.search(r'[a-zA-Z0-9][=+\-*/][a-zA-Z0-9]', line):
                issues.append({
                    'line_number': i,
                    'description': "Missing spaces around operator",
                    'suggestion': "Add spaces around operators (e.g., 'a = b + c')",
                    'severity': 'low'
                })

            # Check for trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append({
                    'line_number': i,
                    'description': "Trailing whitespace",
                    'suggestion': "Remove trailing whitespace",
                    'severity': 'low'
                })

        return issues

    def _check_python_complexity(self, code: str) -> List[Dict[str, Any]]:
        """Check code complexity"""
        issues = []

        try:
            tree = ast.parse(code)

            # Count nested loops/conditions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_cyclomatic_complexity(node)
                    if complexity > 10:
                        issues.append({
                            'line_number': node.lineno,
                            'description': f"Function '{node.name}' has high complexity ({complexity})",
                            'suggestion': "Consider breaking this function into smaller functions",
                            'severity': 'medium'
                        })

                # Check for very deep nesting
                if hasattr(node, 'body'):
                    depth = self._get_nesting_depth(node)
                    if depth > 4:
                        issues.append({
                            'line_number': getattr(node, 'lineno', None),
                            'description': f"Deep nesting detected (depth: {depth})",
                            'suggestion': "Consider reducing nesting depth",
                            'severity': 'medium'
                        })

        except SyntaxError:
            # Already handled in syntax check
            pass

        return issues

    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _get_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Get maximum nesting depth"""
        max_depth = depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With, ast.FunctionDef, ast.ClassDef)):
                child_depth = self._get_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def _analyze_java_code(self, code: str) -> Dict[str, Any]:
        """Basic Java code analysis"""
        issues = []
        lines = code.split('\n')

        # Basic checks
        for i, line in enumerate(lines, 1):
            # Check for missing semicolons (simple heuristic)
            if line.strip() and not line.strip().endswith((';', '{', '}', '//', '/*', '*/')):
                if any(keyword in line for keyword in ['int ', 'String ', 'return ', 'System.out']):
                    issues.append({
                        'line_number': i,
                        'description': "Possible missing semicolon",
                        'suggestion': "Ensure statements end with semicolons",
                        'severity': 'medium'
                    })

        return {'issues': issues, 'score_adjustment': -len(issues) * 3}

    def _analyze_javascript_code(self, code: str) -> Dict[str, Any]:
        """Basic JavaScript code analysis"""
        issues = []
        lines = code.split('\n')

        # Basic checks
        for i, line in enumerate(lines, 1):
            # Check for var usage (prefer let/const)
            if 'var ' in line:
                issues.append({
                    'line_number': i,
                    'description': "Use of 'var' keyword",
                    'suggestion': "Consider using 'let' or 'const' instead of 'var'",
                    'severity': 'low'
                })

            # Check for == instead of ===
            if '==' in line and '===' not in line:
                issues.append({
                    'line_number': i,
                    'description': "Use of loose equality (==)",
                    'suggestion': "Consider using strict equality (===)",
                    'severity': 'medium'
                })

        return {'issues': issues, 'score_adjustment': -len(issues) * 2}


# backend/app/config.py


class Settings:
    """Application configuration"""

    # Model settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "codellama:7b")
    MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0.3"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))

    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # CORS settings
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000").split(",")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Ollama settings
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "localhost")
    OLLAMA_PORT: int = int(os.getenv("OLLAMA_PORT", "11434"))


settings = Settings()
