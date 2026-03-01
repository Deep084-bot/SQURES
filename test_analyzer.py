import sys
sys.path.insert(0, '/Users/deepmehta/Documents/Projects/SQURES/squres')

import zipfile
import tempfile
import os
from app.analysis.analyzer import StaticCodeAnalyzer

# Extract the test zip
with tempfile.TemporaryDirectory() as temp_dir:
    with zipfile.ZipFile('/Users/deepmehta/Documents/Projects/SQURES/test_project.zip', 'r') as z:
        z.extractall(temp_dir)
    
    # Run analyzer
    analyzer = StaticCodeAnalyzer(os.path.join(temp_dir, 'test_project'))
    results = analyzer.analyze()
    
    print("Summary:", results['summary'])
    print("\nFiles found:", len(results['python_files']))
    for fname, data in results['files'].items():
        print(f"\n{fname}:")
        print(f"  - Lines: {data['size_lines']}")
        print(f"  - Complexity: {data['cyclomatic_complexity']}")
        print(f"  - Avg Complexity: {data['average_complexity']}")
        print(f"  - MI: {data['maintainability_index']}")
        print(f"  - Functions: {len(data['functions'])}")
        if data['functions']:
            for func in data['functions']:
                print(f"    * {func['name']}: CC={func['complexity']}")
        if data['errors']:
            print(f"  - Errors: {data['errors']}")
