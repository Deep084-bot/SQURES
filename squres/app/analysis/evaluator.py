"""
Risk evaluator using rule-based assessment.
Identifies defect-prone modules based on static analysis metrics.
"""


class RiskEvaluator:
    """
    Evaluates reliability risks based on computed metrics.
    Uses rule-based thresholds (no machine learning).
    """
    
    # Risk thresholds
    COMPLEXITY_HIGH = 10
    COMPLEXITY_MEDIUM = 7
    
    MI_LOW = 65
    MI_MEDIUM = 85

    LOC_HIGH = 500
    
    # Number of high-risk functions to flag a file as defect-prone
    HIGH_RISK_FUNCTION_THRESHOLD = 2
    
    def __init__(self, analysis_results):
        """
        Initialize evaluator with analysis results.
        
        Args:
            analysis_results (dict): Output from StaticCodeAnalyzer.analyze()
        """
        self.analysis_results = analysis_results
        self.file_risks = {}
        self.defect_prone_modules = []
    
    def categorize_complexity_risk(self, complexity):
        """
        Categorize cyclomatic complexity risk level.
        
        Args:
            complexity (float): Cyclomatic complexity value
            
        Returns:
            str: Risk level ('Low', 'Medium', 'High')
        """
        if complexity >= self.COMPLEXITY_HIGH:
            return 'High'
        elif complexity >= self.COMPLEXITY_MEDIUM:
            return 'Medium'
        else:
            return 'Low'
    
    def categorize_maintainability_risk(self, mi):
        """
        Categorize maintainability index risk level.
        
        Args:
            mi (float): Maintainability index value
            
        Returns:
            str: Risk level ('Low', 'Medium', 'High')
        """
        if mi < self.MI_LOW:
            return 'High'
        elif mi < self.MI_MEDIUM:
            return 'Medium'
        else:
            return 'Low'
    
    def evaluate_file_risk(self, file_path, file_analysis):
        """
        Evaluate risk level for a single file.
        
        Args:
            file_path (str): File path
            file_analysis (dict): Analysis results for the file
            
        Returns:
            dict: Risk assessment for the file
        """
        if file_analysis['errors']:
            return {
                'risk_level': 'Unknown',
                'reasons': file_analysis['errors']
            }
        
        reasons = []
        risk_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        max_risk_score = 1
        
        # Evaluate complexity risk
        complexity_risk = self.categorize_complexity_risk(
            file_analysis['average_complexity']
        )
        if complexity_risk != 'Low':
            reasons.append(
                f"Average cyclomatic complexity is {complexity_risk.lower()} "
                f"({file_analysis['average_complexity']:.2f})"
            )
            max_risk_score = max(max_risk_score, risk_scores[complexity_risk])
        
        # Evaluate maintainability risk
        mi_risk = self.categorize_maintainability_risk(
            file_analysis['maintainability_index']
        )
        if mi_risk != 'Low':
            reasons.append(
                f"Maintainability Index is {mi_risk.lower()} "
                f"({file_analysis['maintainability_index']:.2f})"
            )
            max_risk_score = max(max_risk_score, risk_scores[mi_risk])

        # Flag very large files
        file_loc = file_analysis.get('size_lines', 0)
        if file_loc > self.LOC_HIGH:
            reasons.append(
                f"File is very large ({file_loc} LOC, threshold > {self.LOC_HIGH})"
            )
            # Large files are harder to review/maintain; at least medium risk.
            max_risk_score = max(max_risk_score, risk_scores['Medium'])
        
        # Check for high-complexity functions
        high_complexity_functions = [
            f for f in file_analysis['functions']
            if f['complexity'] >= self.COMPLEXITY_HIGH
        ]
        
        if len(high_complexity_functions) >= self.HIGH_RISK_FUNCTION_THRESHOLD:
            reasons.append(
                f"Contains {len(high_complexity_functions)} functions with high complexity (≥{self.COMPLEXITY_HIGH})"
            )
            max_risk_score = 3
        
        # Map score to risk level
        risk_mapping = {1: 'Low', 2: 'Medium', 3: 'High'}
        risk_level = risk_mapping.get(max_risk_score, 'Low')
        
        return {
            'risk_level': risk_level,
            'reasons': reasons,
            'high_complexity_functions': high_complexity_functions
        }
    
    def evaluate(self):
        """
        Perform complete risk evaluation across all files.
        
        Returns:
            dict: Risk assessment results
        """
        files_data = self.analysis_results.get('files', {})
        
        # Evaluate each file
        for file_path, file_analysis in files_data.items():
            risk_assessment = self.evaluate_file_risk(file_path, file_analysis)
            self.file_risks[file_path] = risk_assessment
            
            # Flag as defect-prone if risk level is Medium or High
            if risk_assessment['risk_level'] in ['Medium', 'High']:
                self.defect_prone_modules.append({
                    'file': file_path,
                    'risk_level': risk_assessment['risk_level'],
                    'reasons': risk_assessment['reasons'],
                    'high_complexity_functions': risk_assessment.get('high_complexity_functions', [])
                })
        
        # Sort defect-prone modules by risk level
        risk_priority = {'High': 0, 'Medium': 1, 'Low': 2}
        self.defect_prone_modules.sort(
            key=lambda x: risk_priority.get(x['risk_level'], 3)
        )
        
        # Calculate summary statistics
        risk_distribution = {'High': 0, 'Medium': 0, 'Low': 0, 'Unknown': 0}
        for risk_info in self.file_risks.values():
            risk_level = risk_info['risk_level']
            risk_distribution[risk_level] += 1
        
        summary = {
            'total_files_evaluated': len(self.file_risks),
            'defect_prone_count': len(self.defect_prone_modules),
            'risk_distribution': risk_distribution
        }
        
        return {
            'summary': summary,
            'file_risks': self.file_risks,
            'defect_prone_modules': self.defect_prone_modules
        }
