"""
Report generator for analysis results.
Supports JSON, text, and PDF-friendly formats.
"""

import json
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER


class ReportGenerator:
    """
    Generates comprehensive analysis reports.
    Supports multiple output formats.
    """
    
    def __init__(self, file_analysis, risk_assessment):
        """
        Initialize report generator.
        
        Args:
            file_analysis (dict): Results from StaticCodeAnalyzer
            risk_assessment (dict): Results from RiskEvaluator
        """
        self.file_analysis = file_analysis
        self.risk_assessment = risk_assessment
    
    def generate_report(self):
        """
        Generate structured report as dictionary.
        
        Returns:
            dict: Comprehensive analysis report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'project_summary': self._generate_summary(),
            'file_metrics': self._generate_file_metrics(),
            'risk_classification': self._generate_risk_classification(),
            'defect_prone_modules': self.risk_assessment.get('defect_prone_modules', []),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_summary(self):
        """Generate project summary section."""
        summary = self.file_analysis.get('summary', {})
        risk_summary = self.risk_assessment.get('summary', {})
        
        return {
            'total_python_files': summary.get('total_files', 0),
            'analyzed_files': summary.get('analyzed_files', 0),
            'files_with_errors': summary.get('files_with_errors', 0),
            'total_lines_of_code': summary.get('total_lines_of_code', 0),
            'total_cyclomatic_complexity': summary.get('total_complexity', 0),
            'average_complexity': summary.get('average_complexity', 0),
            'average_maintainability_index': summary.get('average_maintainability_index', 0),
            'defect_prone_count': risk_summary.get('defect_prone_count', 0),
            'risk_distribution': risk_summary.get('risk_distribution', {})
        }
    
    def _generate_file_metrics(self):
        """Generate detailed file-level metrics."""
        files_data = self.file_analysis.get('files', {})
        metrics = []
        
        for file_path, analysis in files_data.items():
            # Skip venv and cache directories
            if 'venv' in file_path or '__pycache__' in file_path or '.pytest_cache' in file_path:
                continue
            
            metric = {
                'file': file_path,
                'lines_of_code': analysis.get('size_lines', 0),
                'cyclomatic_complexity': analysis.get('cyclomatic_complexity', 0),
                'average_complexity': round(analysis.get('average_complexity', 0), 2),
                'maintainability_index': round(float(analysis.get('maintainability_index', 0)), 2),
                'function_count': len(analysis.get('functions', [])),
                'errors': analysis.get('errors', [])
            }
            
            # Add risk level from risk assessment
            risk_info = self.risk_assessment.get('file_risks', {}).get(file_path, {})
            metric['risk_level'] = risk_info.get('risk_level', 'Unknown')
            metric['risk_reasons'] = risk_info.get('reasons', [])
            
            metrics.append(metric)
        
        return sorted(metrics, key=lambda x: x['cyclomatic_complexity'], reverse=True)
    
    def _generate_risk_classification(self):
        """Generate risk classification details."""
        file_risks = self.risk_assessment.get('file_risks', {})
        
        high_risk = []
        medium_risk = []
        low_risk = []
        unknown_risk = []
        
        for file_path, risk_info in file_risks.items():
            file_entry = {
                'file': file_path,
                'risk_level': risk_info['risk_level'],
                'reasons': risk_info.get('reasons', [])
            }
            
            risk_level = risk_info['risk_level']
            if risk_level == 'High':
                high_risk.append(file_entry)
            elif risk_level == 'Medium':
                medium_risk.append(file_entry)
            elif risk_level == 'Low':
                low_risk.append(file_entry)
            else:
                unknown_risk.append(file_entry)
        
        return {
            'high_risk_files': high_risk,
            'medium_risk_files': medium_risk,
            'low_risk_files': low_risk,
            'unknown_risk_files': unknown_risk
        }
    
    def _generate_recommendations(self):
        """Generate actionable recommendations."""
        summary = self.file_analysis.get('summary', {})
        defect_prone = self.risk_assessment.get('defect_prone_modules', [])
        
        recommendations = []
        
        # Check average complexity
        avg_complexity = summary.get('average_complexity', 0)
        if avg_complexity > 7:
            recommendations.append({
                'priority': 'High',
                'issue': 'High average cyclomatic complexity',
                'details': f'Average complexity is {avg_complexity:.2f}. '
                           'Consider refactoring complex functions into smaller units.',
                'action': 'Refactor complex functions with complexity > 10'
            })
        
        # Check maintainability
        avg_mi = summary.get('average_maintainability_index', 0)
        if avg_mi < 65:
            recommendations.append({
                'priority': 'High',
                'issue': 'Poor maintainability',
                'details': f'Average MI is {avg_mi:.2f}. '
                           'Code is difficult to maintain and should be simplified.',
                'action': 'Improve code documentation and simplify complex logic'
            })
        elif avg_mi < 85:
            recommendations.append({
                'priority': 'Medium',
                'issue': 'Moderate maintainability concerns',
                'details': f'Average MI is {avg_mi:.2f}. '
                           'Consider improving code clarity.',
                'action': 'Add documentation and reduce complexity'
            })
        
        # Defect-prone modules
        high_risk_count = len([m for m in defect_prone if m['risk_level'] == 'High'])
        if high_risk_count > 0:
            recommendations.append({
                'priority': 'High',
                'issue': f'{high_risk_count} high-risk modules identified',
                'details': 'These modules have multiple quality issues and should be reviewed.',
                'action': 'Review and refactor high-risk modules'
            })
        
        return recommendations
    
    def generate_text_report(self):
        """
        Generate human-readable text report.
        
        Returns:
            str: Formatted text report
        """
        report = self.generate_report()
        
        lines = []
        lines.append("=" * 80)
        lines.append("SQARES - Software Quality Analysis and Realiability Evaluation System")
        lines.append("Analysis Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Generated: {report['generated_at']}")
        lines.append("")
        
        # Project Summary
        lines.append("=" * 80)
        lines.append("PROJECT SUMMARY")
        lines.append("=" * 80)
        summary = report['project_summary']
        lines.append(f"Total Python Files:           {summary['total_python_files']}")
        lines.append(f"Analyzed Files:               {summary['analyzed_files']}")
        lines.append(f"Files with Errors:            {summary['files_with_errors']}")
        lines.append(f"Total Lines of Code:          {summary['total_lines_of_code']:,}")
        lines.append(f"Total Cyclomatic Complexity:  {summary['total_cyclomatic_complexity']}")
        lines.append(f"Average Complexity:           {summary['average_complexity']:.2f}")
        lines.append(f"Average Maintainability:      {summary['average_maintainability_index']:.2f}")
        lines.append(f"Defect-Prone Modules:         {summary['defect_prone_count']}")
        lines.append("")
        
        # Risk Distribution
        lines.append("Risk Distribution:")
        risk_dist = summary['risk_distribution']
        for risk_level in ['High', 'Medium', 'Low', 'Unknown']:
            count = risk_dist.get(risk_level, 0)
            lines.append(f"  {risk_level:8} Risk: {count} files")
        lines.append("")
        
        # File Metrics
        lines.append("=" * 80)
        lines.append("FILE METRICS")
        lines.append("=" * 80)
        lines.append("")
        
        file_metrics = report['file_metrics']
        if file_metrics:
            # Header
            lines.append(f"{'File':<45} {'LOC':>6} {'CC':>6} {'MI':>8} {'Risk':>8}")
            lines.append("-" * 80)
            
            # Data rows
            for metric in file_metrics[:25]:  # Limit to top 25
                # Clean up file paths
                filename = metric['file']
                if 'venv' in filename:
                    continue  # Skip venv files
                filename = filename.replace('test_project/', '').replace('extracted/', '')
                filename = filename[:42] + '...' if len(filename) > 45 else filename
                
                loc = metric.get('lines_of_code', 0)
                cc = metric.get('cyclomatic_complexity', 0)
                mi = metric.get('maintainability_index', 0)
                risk = metric.get('risk_level', 'Unknown')
                
                lines.append(
                    f"{filename:<45} {loc:>6} {cc:>6} {mi:>8.2f} {risk:>8}"
                )
            
            if len(file_metrics) > 25:
                lines.append(f"... and {len(file_metrics) - 25} more files")
        
        lines.append("")
        
        # Defect-Prone Modules
        defect_prone = report['defect_prone_modules']
        if defect_prone:
            lines.append("=" * 80)
            lines.append("DEFECT-PRONE MODULES")
            lines.append("=" * 80)
            lines.append("")
            
            for idx, module in enumerate(defect_prone, 1):
                lines.append(f"{idx}. {module['file']} [{module['risk_level'].upper()}]")
                for reason in module['reasons']:
                    lines.append(f"   - {reason}")
                
                high_func = module.get('high_complexity_functions', [])
                if high_func:
                    lines.append(f"   High-Complexity Functions:")
                    for func in high_func[:3]:  # Limit display
                        lines.append(f"     • {func['name']} (CC={func['complexity']})")
                    if len(high_func) > 3:
                        lines.append(f"     • ... and {len(high_func) - 3} more")
                lines.append("")
        
        # Recommendations
        recommendations = report['recommendations']
        if recommendations:
            lines.append("=" * 80)
            lines.append("RECOMMENDATIONS")
            lines.append("=" * 80)
            lines.append("")
            
            for idx, rec in enumerate(recommendations, 1):
                lines.append(f"{idx}. [{rec['priority'].upper()}] {rec['issue']}")
                lines.append(f"   {rec['details']}")
                lines.append(f"   Action: {rec['action']}")
                lines.append("")
        
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def generate_pdf_report(self):
        """
        Generate a professional PDF report.
        
        Returns:
            bytes: PDF document content
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=6,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=12,
            spaceBefore=12
        )
        normal_style = styles['Normal']
        
        # Build document content
        content = []
        
        # Title
        content.append(Paragraph("SQARES - Code Analysis Report", title_style))
        content.append(Spacer(1, 0.2*inch))
        
        # Summary Section
        report = self.generate_report()
        summary = report['project_summary']
        
        content.append(Paragraph("Project Summary", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Python Files', str(summary['total_python_files'])],
            ['Analyzed Files', str(summary['analyzed_files'])],
            ['Total Lines of Code', f"{summary['total_lines_of_code']:,}"],
            ['Total Cyclomatic Complexity', str(summary['total_cyclomatic_complexity'])],
            ['Average Complexity', f"{summary['average_complexity']:.2f}"],
            ['Average Maintainability Index', f"{summary['average_maintainability_index']:.2f}"],
            ['Defect-Prone Modules', str(summary['defect_prone_count'])],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        content.append(summary_table)
        content.append(Spacer(1, 0.3*inch))
        
        # File Metrics Section
        content.append(Paragraph("File Metrics", heading_style))
        file_metrics = report['file_metrics']
        if file_metrics:
            metrics_data = [['File', 'LOC', 'CC', 'MI', 'Risk']]
            
            # Process file metrics, limiting to top 20 most complex files
            for metric in file_metrics[:20]:
                # Clean up file path
                file_display = metric['file']
                if any(x in file_display for x in ['venv', 'site-packages', '__pycache__']):
                    continue  # Skip venv/cache files
                    
                # Shorten path for display
                if '/' in file_display:
                    parts = file_display.split('/')
                    file_display = parts[-1]  # Just filename
                
                if len(file_display) > 30:
                    file_display = file_display[:27] + '...'
                
                cc = metric.get('cyclomatic_complexity', 0)
                mi = float(metric.get('maintainability_index', 0))
                
                metrics_data.append([
                    file_display,
                    str(metric['lines_of_code']),
                    str(cc) if cc > 0 else '-',
                    f"{mi:.1f}" if mi > 0 else '-',
                    metric['risk_level']
                ])
            
            if len(metrics_data) > 1:  # Only show table if there's data
                # Better column widths for improved formatting
                metrics_table = Table(metrics_data, colWidths=[2.0*inch, 0.6*inch, 0.5*inch, 0.5*inch, 0.8*inch])
                metrics_table.setStyle(TableStyle([
                    # Header styling
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    
                    # Data rows styling
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGNMENT', (1, 1), (-1, -1), 'CENTER'),
                    ('ALIGNMENT', (0, 1), (0, -1), 'LEFT'),
                    
                    # Grid styling
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
                    
                    # Risk level coloring
                    ('TEXTCOLOR', (4, 1), (4, -1), colors.black),
                ]))
                
                # Apply risk level background colors per row
                for i in range(1, len(metrics_data)):
                    risk = metrics_data[i][-1]
                    if risk == 'High':
                        metrics_table.setStyle(TableStyle([('BACKGROUND', (4, i), (4, i), colors.HexColor('#ffebee'))]))
                    elif risk == 'Medium':
                        metrics_table.setStyle(TableStyle([('BACKGROUND', (4, i), (4, i), colors.HexColor('#fff3e0'))]))
                    elif risk == 'Low':
                        metrics_table.setStyle(TableStyle([('BACKGROUND', (4, i), (4, i), colors.HexColor('#e8f5e9'))]))
                
                content.append(metrics_table)
        
        content.append(Spacer(1, 0.3*inch))
        risk_class = report['risk_classification']
        content.append(Paragraph("Risk Classification", heading_style))
        
        risk_items = []
        if risk_class['high_risk_files']:
            risk_items.append(f"High Risk: {len(risk_class['high_risk_files'])} files")
        if risk_class['medium_risk_files']:
            risk_items.append(f"Medium Risk: {len(risk_class['medium_risk_files'])} files")
        if risk_class['low_risk_files']:
            risk_items.append(f"Low Risk: {len(risk_class['low_risk_files'])} files")
        if risk_class['unknown_risk_files']:
            risk_items.append(f"Unknown Risk: {len(risk_class['unknown_risk_files'])} files")
        
        for item in risk_items:
            content.append(Paragraph(f"• {item}", normal_style))
        
        content.append(Spacer(1, 0.3*inch))
        
        # Recommendations Section
        recommendations = report['recommendations']
        if recommendations:
            content.append(Paragraph("Recommendations", heading_style))
            for rec in recommendations[:5]:  # Limit to first 5 recommendations
                content.append(Paragraph(
                    f"<b>[{rec['priority'].upper()}] {rec['issue']}</b>",
                    normal_style
                ))
                content.append(Paragraph(f"{rec['details']}", normal_style))
                content.append(Spacer(1, 0.1*inch))
        
        # Footer
        content.append(Spacer(1, 0.2*inch))
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content.append(Paragraph(
            f"<i>Report generated on {timestamp}</i>",
            ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey)
        ))
        
        # Build PDF
        doc.build(content)
        buffer.seek(0)
        return buffer.getvalue()

