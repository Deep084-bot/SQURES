"""
Static code analyzer using radon for Python code metrics.
Computes cyclomatic complexity and maintainability index.
"""

import os
import ast
from radon.complexity import cc_visit
from radon.metrics import mi_visit


class StaticCodeAnalyzer:
    """
    Performs static analysis on Python source code.
    
    Uses radon library to compute:
    - Cyclomatic Complexity (CC)
    - Maintainability Index (MI)
    """
    
    def __init__(self, source_dir):
        """
        Initialize analyzer with source directory.
        
        Args:
            source_dir (str): Path to directory containing Python files
        """
        self.source_dir = source_dir
        self.python_files = []
        self.analysis_results = {}
    
    def find_python_files(self):
        """
        Recursively find all Python files in source directory.
        Excludes virtual environments, caches, and other non-essential directories.
        
        Returns:
            list: List of Python file paths
        """
        python_files = []
        exclude_dirs = {
            '.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv', 'ENV',
            'site-packages', 'dist-info', '.tox', '.mypy_cache', '.hypothesis',
            'node_modules', '.idea', '.vscode', '.egg-info'
        }
        
        for root, dirs, files in os.walk(self.source_dir):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            
            # Skip if we're in an excluded path
            if any(x in root for x in ['venv', 'env', 'site-packages', '__pycache__', '.egg-info']):
                continue
            
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    python_files.append(full_path)
        
        return sorted(python_files)
    
    def analyze_file(self, file_path):
        """
        Analyze a single Python file for complexity and maintainability.
        
        Args:
            file_path (str): Path to Python file
            
        Returns:
            dict: Analysis results for the file
        """
        result = {
            'path': file_path,
            'relative_path': os.path.relpath(file_path, self.source_dir),
            'size_lines': 0,
            'ast_node_count': 0,
            'class_count': 0,
            'cyclomatic_complexity': 0,
            'average_complexity': 0,
            'maintainability_index': 0,
            'functions': [],
            'errors': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source_code = f.read()
            
            # Count lines
            result['size_lines'] = len(source_code.splitlines())

            # Parse AST for structural metrics
            try:
                syntax_tree = ast.parse(source_code)
                result['ast_node_count'] = sum(1 for _ in ast.walk(syntax_tree))
                result['class_count'] = sum(
                    1 for node in ast.walk(syntax_tree) if isinstance(node, ast.ClassDef)
                )
            except Exception as e:
                result['errors'].append(f"AST parsing failed: {str(e)}")
            
            # Calculate cyclomatic complexity
            try:
                cc_results = cc_visit(source_code)
                
                if cc_results:
                    # Extract function-level complexity
                    for item in cc_results:
                        if hasattr(item, 'classname') and item.classname:
                            # Method in a class
                            func_name = f"{item.classname}.{item.name}"
                        else:
                            func_name = item.name
                        
                        result['functions'].append({
                            'name': func_name,
                            'type': item.type if hasattr(item, 'type') else 'function',
                            'complexity': item.complexity,
                            'lines': item.endline - item.lineno + 1 if hasattr(item, 'lineno') else 0
                        })
                        
                        result['cyclomatic_complexity'] += item.complexity
                    
                    # Calculate average complexity
                    if result['functions']:
                        result['average_complexity'] = result['cyclomatic_complexity'] / len(result['functions'])
                else:
                    # No functions found, but this might be OK (module-level code)
                    # Set a default complexity of 1 for files with no detectable functions
                    result['cyclomatic_complexity'] = 1
                    result['average_complexity'] = 1
            
            except Exception as e:
                result['errors'].append(f"Complexity analysis failed: {str(e)}")
                # Set default complexity even if radon fails
                result['cyclomatic_complexity'] = 1
                result['average_complexity'] = 1
            
            # Calculate maintainability index
            try:
                mi_result = mi_visit(source_code, multi=True)
                
                if mi_result is not None:
                    # mi_visit returns a single float or tuple
                    if isinstance(mi_result, (tuple, list)):
                        mi_val = float(mi_result[0]) if mi_result else None
                    else:
                        mi_val = float(mi_result) if mi_result else None
                    
                    # Ensure MI is in valid range (0-100)
                    if mi_val is not None and 0 <= mi_val <= 100:
                        result['maintainability_index'] = mi_val
                    else:
                        # If MI is out of range or invalid, calculate a default based on LOC
                        result['maintainability_index'] = max(0, min(100, 100 - (result['size_lines'] / 100)))
                else:
                    # Default MI calculation if radon returns None
                    result['maintainability_index'] = max(0, min(100, 100 - (result['size_lines'] / 100)))
            
            except Exception as e:
                result['errors'].append(f"Maintainability analysis encountered issue: {str(e)}")
                # Provide a reasonable default based on file size
                result['maintainability_index'] = max(0, min(100, 100 - (result['size_lines'] / 100)))
        
        except Exception as e:
            result['errors'].append(f"Failed to read file: {str(e)}")
        
        return result
    
    def analyze(self):
        """
        Perform complete analysis on all Python files.
        
        Returns:
            dict: Comprehensive analysis results
        """
        self.python_files = self.find_python_files()
        
        # Analyze each file
        file_results = {}
        total_complexity = 0
        total_files = 0
        total_lines = 0
        avg_mi = 0
        files_with_errors = 0
        
        for file_path in self.python_files:
            analysis = self.analyze_file(file_path)
            file_results[analysis['relative_path']] = analysis
            
            # Count all successfully analyzed files (even if they had some errors)
            # Only skip files that had critical errors like read failure
            if "Failed to read file" not in str(analysis['errors']):
                total_complexity += analysis['cyclomatic_complexity']
                total_lines += analysis['size_lines']
                avg_mi += analysis['maintainability_index']
                total_files += 1
            
            if analysis['errors']:
                files_with_errors += 1
        
        # Calculate averages
        if total_files > 0:
            avg_complexity = total_complexity / total_files
            avg_mi = avg_mi / total_files
        else:
            avg_complexity = 0
            avg_mi = 0
        
        summary = {
            'total_files': len(self.python_files),
            'analyzed_files': total_files,
            'files_with_errors': files_with_errors,
            'total_lines_of_code': total_lines,
            'total_complexity': total_complexity,
            'average_complexity': round(avg_complexity, 2),
            'average_maintainability_index': round(avg_mi, 2)
        }
        
        return {
            'python_files': self.python_files,
            'summary': summary,
            'files': file_results
        }
