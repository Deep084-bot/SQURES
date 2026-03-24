"""
Tests for static code analyzer.
"""

import unittest
import tempfile
import os
from unittest.mock import patch

try:
    import app.analysis.analyzer as analyzer_module
except ModuleNotFoundError:
    import squres.app.analysis.analyzer as analyzer_module

StaticCodeAnalyzer = analyzer_module.StaticCodeAnalyzer


class TestStaticCodeAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_file(self, name, content):
        path = os.path.join(self.test_dir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return path
    
    def test_find_python_files(self):
        self.create_test_file('test.py', 'x = 1')
        self.create_test_file('subdir/test2.py', 'y = 2')
        
        analyzer = StaticCodeAnalyzer(self.test_dir)
        files = analyzer.find_python_files()
        
        self.assertEqual(len(files), 2)
    
    def test_analyze_simple_file(self):
        code = self.create_test_file('simple.py', code)
        
        analyzer = StaticCodeAnalyzer(self.test_dir)
        result = analyzer.analyze()
        
        self.assertGreater(result['summary']['total_files'], 0)
        self.assertGreater(result['summary']['analyzed_files'], 0)
    
    def test_analyze_complex_file(self):
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

    def test_find_python_files_excludes_virtualenv_directories(self):
        self.create_test_file('src/main.py', 'print("ok")')
        self.create_test_file('venv/lib/ignored.py', 'print("ignore")')
        self.create_test_file('.venv/lib/ignored2.py', 'print("ignore")')
        self.create_test_file('env/lib/ignored3.py', 'print("ignore")')

        analyzer = StaticCodeAnalyzer(self.test_dir)
        files = analyzer.find_python_files()
        relative_files = {os.path.relpath(path, self.test_dir) for path in files}

        self.assertIn('src/main.py', relative_files)
        self.assertNotIn('venv/lib/ignored.py', relative_files)
        self.assertNotIn('.venv/lib/ignored2.py', relative_files)
        self.assertNotIn('env/lib/ignored3.py', relative_files)

    def test_analyze_file_handles_missing_file_error(self):
        analyzer = StaticCodeAnalyzer(self.test_dir)
        result = analyzer.analyze_file(os.path.join(self.test_dir, 'does_not_exist.py'))

        self.assertTrue(any('Failed to read file' in err for err in result['errors']))

    def test_maintainability_index_is_within_range(self):
        self.create_test_file('maintainability.py', 'def add(a, b):\n    return a + b\n')

        analyzer = StaticCodeAnalyzer(self.test_dir)
        result = analyzer.analyze()
        file_result = result['files']['maintainability.py']

        self.assertGreaterEqual(file_result['maintainability_index'], 0)
        self.assertLessEqual(file_result['maintainability_index'], 100)

    def test_maintainability_fallback_on_metric_failure(self):
        code = 'x = 1\ny = 2\n'
        path = self.create_test_file('mi_fallback.py', code)

        analyzer = StaticCodeAnalyzer(self.test_dir)
        with patch.object(analyzer_module, 'mi_visit', side_effect=Exception('mi failed')):
            result = analyzer.analyze_file(path)

        expected_default = 100 - (result['size_lines'] / 100)
        self.assertAlmostEqual(result['maintainability_index'], expected_default)
        self.assertTrue(any('Maintainability analysis encountered issue' in err for err in result['errors']))

    def test_ast_metrics_include_node_and_class_counts(self):
        code = """
class Service:
    def run(self):
        return True

def helper(x):
    return x * 2
"""
        path = self.create_test_file('ast_metrics.py', code)

        analyzer = StaticCodeAnalyzer(self.test_dir)
        result = analyzer.analyze_file(path)

        self.assertGreater(result['ast_node_count'], 0)
        self.assertEqual(result['class_count'], 1)


if __name__ == '__main__':
    unittest.main()
