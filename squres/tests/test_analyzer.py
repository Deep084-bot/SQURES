"""
Tests for static code analyzer.
"""

import unittest
import tempfile
import os
from app.analysis.analyzer import StaticCodeAnalyzer


class TestStaticCodeAnalyzer(unittest.TestCase):
    """Test cases for StaticCodeAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_file(self, name, content):
        """Create a test Python file."""
        path = os.path.join(self.test_dir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return path
    
    def test_find_python_files(self):
        """Test finding Python files."""
        self.create_test_file('test.py', 'x = 1')
        self.create_test_file('subdir/test2.py', 'y = 2')
        
        analyzer = StaticCodeAnalyzer(self.test_dir)
        files = analyzer.find_python_files()
        
        self.assertEqual(len(files), 2)
    
    def test_analyze_simple_file(self):
        """Test analyzing a simple Python file."""
        code = """
def simple_function():
    return 42
"""
        self.create_test_file('simple.py', code)
        
        analyzer = StaticCodeAnalyzer(self.test_dir)
        result = analyzer.analyze()
        
        self.assertGreater(result['summary']['total_files'], 0)
        self.assertGreater(result['summary']['analyzed_files'], 0)
    
    def test_analyze_complex_file(self):
        """Test analyzing a complex Python file."""
        code = """
def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 100:
                return 'large'
            else:
                return 'medium'
        else:
            return 'small'
    else:
        return 'negative'
"""
        self.create_test_file('complex.py', code)
        
        analyzer = StaticCodeAnalyzer(self.test_dir)
        result = analyzer.analyze()
        
        files = result['files']
        self.assertGreater(len(files), 0)
        
        for file_analysis in files.values():
            if not file_analysis['errors']:
                self.assertGreater(file_analysis['cyclomatic_complexity'], 0)


if __name__ == '__main__':
    unittest.main()
