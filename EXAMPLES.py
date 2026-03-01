"""
Example usage of SQURES API and analysis components.
Demonstrates common workflows and integrations.
"""

# ============================================================================
# Example 1: Direct Python Integration
# ============================================================================

from app.analysis.analyzer import StaticCodeAnalyzer
from app.analysis.evaluator import RiskEvaluator
from app.analysis.report_generator import ReportGenerator

# Analyze a local directory
analyzer = StaticCodeAnalyzer('/path/to/python/code')
analysis_results = analyzer.analyze()

print(f"Analyzed {analysis_results['summary']['total_files']} files")
print(f"Average complexity: {analysis_results['summary']['average_complexity']}")

# Evaluate risks
evaluator = RiskEvaluator(analysis_results)
risk_assessment = evaluator.evaluate()

print(f"Defect-prone modules: {len(risk_assessment['defect_prone_modules'])}")

# Generate report
report_gen = ReportGenerator(
    analysis_results['files'],
    risk_assessment
)
report = report_gen.generate_report()

print("\nProject Summary:")
print(f"  Total LOC: {report['project_summary']['total_lines_of_code']}")
print(f"  Risk Distribution: {report['project_summary']['risk_distribution']}")

# Generate text report
text_report = report_gen.generate_text_report()
print(text_report)


# ============================================================================
# Example 2: Flask Application Integration
# ============================================================================

from app import create_app
from flask import jsonify

app = create_app()

@app.route('/custom-analysis', methods=['POST'])
def custom_analysis():
    """Custom endpoint for analysis with additional processing."""
    # Implementation would follow the same pattern as /api/upload
    pass


# ============================================================================
# Example 3: File Upload and Analysis Script
# ============================================================================

import os
import zipfile
import tempfile
import shutil
from app.analysis.analyzer import StaticCodeAnalyzer
from app.analysis.evaluator import RiskEvaluator

def analyze_zip_file(zip_path):
    """Analyze a Python project from a zip file."""
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix='squres_analysis_')
    
    try:
        # Extract zip
        extract_dir = os.path.join(temp_dir, 'extracted')
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Analyze
        analyzer = StaticCodeAnalyzer(extract_dir)
        results = analyzer.analyze()
        
        # Evaluate
        evaluator = RiskEvaluator(results)
        assessment = evaluator.evaluate()
        
        return results, assessment
    
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

# Usage
results, assessment = analyze_zip_file('project.zip')
print(f"Found {len(assessment['defect_prone_modules'])} defect-prone modules")


# ============================================================================
# Example 4: Batch Analysis
# ============================================================================

import os
from pathlib import Path
from app.analysis.analyzer import StaticCodeAnalyzer
from app.analysis.evaluator import RiskEvaluator
from app.analysis.report_generator import ReportGenerator

def analyze_multiple_projects(projects_dir):
    """Analyze multiple projects in a directory."""
    
    results = {}
    
    for project_name in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project_name)
        
        if not os.path.isdir(project_path):
            continue
        
        try:
            # Analyze project
            analyzer = StaticCodeAnalyzer(project_path)
            analysis = analyzer.analyze()
            
            # Evaluate
            evaluator = RiskEvaluator(analysis)
            risk = evaluator.evaluate()
            
            # Generate report
            report_gen = ReportGenerator(analysis['files'], risk)
            report = report_gen.generate_report()
            
            results[project_name] = {
                'status': 'success',
                'analysis': analysis,
                'risk': risk,
                'report': report
            }
        
        except Exception as e:
            results[project_name] = {
                'status': 'error',
                'error': str(e)
            }
    
    return results

# Usage
projects = analyze_multiple_projects('/path/to/projects')
for project_name, result in projects.items():
    if result['status'] == 'success':
        print(f"{project_name}: {result['report']['project_summary']['average_complexity']:.2f} avg CC")
    else:
        print(f"{project_name}: {result['error']}")


# ============================================================================
# Example 5: Custom Risk Rules
# ============================================================================

from app.analysis.evaluator import RiskEvaluator

class CustomRiskEvaluator(RiskEvaluator):
    """Extended evaluator with custom risk rules."""
    
    # Custom thresholds
    COMPLEXITY_HIGH = 8  # Stricter than default
    MI_LOW = 70  # Stricter than default
    
    def evaluate_file_risk(self, file_path, file_analysis):
        """Override to add custom rules."""
        
        base_result = super().evaluate_file_risk(file_path, file_analysis)
        
        # Add custom rule: Flag files with many functions
        function_count = len(file_analysis.get('functions', []))
        if function_count > 15:
            if base_result['risk_level'] == 'Low':
                base_result['risk_level'] = 'Medium'
            base_result['reasons'].append(
                f"File has {function_count} functions (consider splitting)"
            )
        
        return base_result

# Usage
evaluator = CustomRiskEvaluator(analysis_results)
assessment = evaluator.evaluate()


# ============================================================================
# Example 6: Export to Different Formats
# ============================================================================

import json
import csv
from app.analysis.report_generator import ReportGenerator

report_gen = ReportGenerator(analysis['files'], assessment)
report = report_gen.generate_report()

# Export as JSON
with open('report.json', 'w') as f:
    json.dump(report, f, indent=2)

# Export file metrics as CSV
with open('metrics.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['file', 'loc', 'complexity', 'mi', 'risk'])
    writer.writeheader()
    
    for metric in report['file_metrics']:
        writer.writerow({
            'file': metric['file'],
            'loc': metric['lines_of_code'],
            'complexity': metric['cyclomatic_complexity'],
            'mi': metric['maintainability_index'],
            'risk': metric['risk_level']
        })


# ============================================================================
# Example 7: Real-time Analysis with Progress
# ============================================================================

import sys
from app.analysis.analyzer import StaticCodeAnalyzer

class ProgressAnalyzer(StaticCodeAnalyzer):
    """Analyzer with progress reporting."""
    
    def analyze(self):
        """Override analyze with progress output."""
        
        self.python_files = self.find_python_files()
        print(f"Found {len(self.python_files)} Python files")
        
        file_results = {}
        
        for idx, file_path in enumerate(self.python_files):
            print(f"\r[{idx+1}/{len(self.python_files)}] Analyzing...", end='')
            sys.stdout.flush()
            
            analysis = self.analyze_file(file_path)
            file_results[analysis['relative_path']] = analysis
        
        print("\nAnalysis complete!")
        
        # Return results (same as parent)
        return super().analyze()

# Usage
analyzer = ProgressAnalyzer('/path/to/code')
results = analyzer.analyze()


# ============================================================================
# Example 8: Configuration from Environment
# ============================================================================

import os
from app import create_app
from config import Config

# Configure from environment
class EnvConfig(Config):
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 50 * 1024 * 1024))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/squres_uploads')

# Create app with environment config
app = create_app(config=EnvConfig.__dict__)


# ============================================================================
# Example 9: Analysis Comparison
# ============================================================================

def compare_analyses(analysis1, analysis2):
    """Compare two analysis results."""
    
    summary1 = analysis1['summary']
    summary2 = analysis2['summary']
    
    comparison = {
        'files_analyzed': {
            'before': summary1['analyzed_files'],
            'after': summary2['analyzed_files'],
            'change': summary2['analyzed_files'] - summary1['analyzed_files']
        },
        'complexity': {
            'before': summary1['average_complexity'],
            'after': summary2['average_complexity'],
            'improvement': summary1['average_complexity'] - summary2['average_complexity']
        },
        'maintainability': {
            'before': summary1['average_maintainability_index'],
            'after': summary2['average_maintainability_index'],
            'improvement': summary2['average_maintainability_index'] - summary1['average_maintainability_index']
        }
    }
    
    return comparison

# Usage
before = analyzer.analyze()
# ... refactor code ...
after = analyzer.analyze()
comparison = compare_analyses(before, after)

print(f"Complexity improvement: {comparison['complexity']['improvement']:.2f}")
print(f"Maintainability improvement: {comparison['maintainability']['improvement']:.2f}")


# ============================================================================
# Example 10: Integration Tests
# ============================================================================

import unittest
import tempfile
import os

class IntegrationTest(unittest.TestCase):
    """Integration tests for SQURES."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_full_analysis_pipeline(self):
        """Test complete analysis pipeline."""
        
        # Create test file
        code = """
def process(data):
    results = []
    for item in data:
        if item:
            results.append(item * 2)
    return results
"""
        test_file = os.path.join(self.test_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write(code)
        
        # Analyze
        analyzer = StaticCodeAnalyzer(self.test_dir)
        results = analyzer.analyze()
        
        self.assertGreater(results['summary']['analyzed_files'], 0)
        
        # Evaluate
        evaluator = RiskEvaluator(results)
        assessment = evaluator.evaluate()
        
        self.assertIsNotNone(assessment)
        
        # Generate report
        report_gen = ReportGenerator(results['files'], assessment)
        report = report_gen.generate_report()
        
        self.assertIn('project_summary', report)
        self.assertIn('recommendations', report)

if __name__ == '__main__':
    unittest.main()

