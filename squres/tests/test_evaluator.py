"""
Tests for risk evaluator.
"""

import unittest
from app.analysis.evaluator import RiskEvaluator


class TestRiskEvaluator(unittest.TestCase):
    """Test cases for RiskEvaluator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_analysis = {
            'files': {},
            'summary': {}
        }
    
    def test_complexity_categorization(self):
        """Test cyclomatic complexity categorization."""
        evaluator = RiskEvaluator(self.base_analysis)
        
        self.assertEqual(evaluator.categorize_complexity_risk(5), 'Low')
        self.assertEqual(evaluator.categorize_complexity_risk(8), 'Medium')
        self.assertEqual(evaluator.categorize_complexity_risk(12), 'High')
    
    def test_maintainability_categorization(self):
        """Test maintainability index categorization."""
        evaluator = RiskEvaluator(self.base_analysis)
        
        self.assertEqual(evaluator.categorize_maintainability_risk(90), 'Low')
        self.assertEqual(evaluator.categorize_maintainability_risk(75), 'Medium')
        self.assertEqual(evaluator.categorize_maintainability_risk(50), 'High')
    
    def test_evaluate_file_with_errors(self):
        """Test evaluating a file with errors."""
        analysis = {
            'files': {
                'test.py': {
                    'errors': ['Parse error']
                }
            },
            'summary': {}
        }
        
        evaluator = RiskEvaluator(analysis)
        result = evaluator.evaluate()
        
        self.assertIn('test.py', result['file_risks'])
        self.assertEqual(result['file_risks']['test.py']['risk_level'], 'Unknown')
    
    def test_evaluate_low_risk_file(self):
        """Test evaluating a low-risk file."""
        analysis = {
            'files': {
                'good.py': {
                    'cyclomatic_complexity': 3,
                    'average_complexity': 2,
                    'maintainability_index': 90,
                    'functions': [
                        {'name': 'func1', 'complexity': 2}
                    ],
                    'errors': []
                }
            },
            'summary': {}
        }
        
        evaluator = RiskEvaluator(analysis)
        result = evaluator.evaluate()
        
        self.assertEqual(result['file_risks']['good.py']['risk_level'], 'Low')
    
    def test_defect_prone_identification(self):
        """Test identification of defect-prone modules."""
        analysis = {
            'files': {
                'bad.py': {
                    'cyclomatic_complexity': 20,
                    'average_complexity': 10,
                    'maintainability_index': 50,
                    'functions': [
                        {'name': 'f1', 'complexity': 12},
                        {'name': 'f2', 'complexity': 11}
                    ],
                    'errors': []
                }
            },
            'summary': {}
        }
        
        evaluator = RiskEvaluator(analysis)
        result = evaluator.evaluate()
        
        self.assertGreater(len(result['defect_prone_modules']), 0)
        self.assertEqual(result['defect_prone_modules'][0]['risk_level'], 'High')


if __name__ == '__main__':
    unittest.main()
