"""
Flask routes for file upload, analysis, and report generation.
Implements clean separation between API and web endpoints.
"""

import os
import zipfile
import tempfile
import shutil
import json
from datetime import datetime
import traceback
import sys

from flask import Blueprint, request, jsonify, render_template, send_file, current_app
from werkzeug.utils import secure_filename

from app.analysis.analyzer import StaticCodeAnalyzer
from app.analysis.evaluator import RiskEvaluator
from app.analysis.report_generator import ReportGenerator
from app.utils.validators import validate_upload, validate_file_size, validate_zip_contents

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')
web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    """Display the main upload page."""
    return render_template('index.html')


@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and initiate analysis.
    
    Returns:
        JSON response with analysis results or error message
    """
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']

        max_file_size = current_app.config.get('MAX_CONTENT_LENGTH', 500 * 1024 * 1024)
        is_valid_upload, upload_error = validate_upload(file, max_file_size)
        if not is_valid_upload:
            return jsonify({'error': upload_error}), 400
        
        # Create temporary directory for extraction
        temp_dir = tempfile.mkdtemp(prefix='squres_')
        
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            zip_path = os.path.join(temp_dir, filename)
            file.save(zip_path)
            
            # Validate saved file size and zip contents
            is_valid_size, size_error = validate_file_size(zip_path, max_file_size)
            if not is_valid_size:
                return jsonify({'error': size_error}), 400

            is_valid_zip, zip_error = validate_zip_contents(zip_path)
            if not is_valid_zip:
                return jsonify({'error': zip_error}), 400
            
            # Extract zip file
            extract_dir = os.path.join(temp_dir, 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Perform static analysis
            analyzer = StaticCodeAnalyzer(extract_dir)
            analysis_results = analyzer.analyze()
            
            if not analysis_results['python_files']:
                return jsonify({'error': 'No Python files found in the uploaded archive'}), 400
            
            # Evaluate risks
            evaluator = RiskEvaluator(analysis_results)
            risk_assessment = evaluator.evaluate()
            
            # Generate report
            report_gen = ReportGenerator(analysis_results, risk_assessment)
            report = report_gen.generate_report()
            
            # Prepare response
            response = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'analysis': {
                    'summary': analysis_results['summary'],
                    'files': analysis_results['files'],
                    'risk_assessment': risk_assessment,
                    'report': report
                }
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            error_msg = str(e)
            traceback.print_exc()
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return jsonify({'error': f'Analysis failed: {error_msg}'}), 500
        
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@api_bp.route('/download-report', methods=['POST'])
def download_report():
    """
    Generate and download analysis report.
    
    Request JSON:
        - analysis: dict containing analysis data
        - format: 'txt', 'pdf', or 'json'
    
    Returns:
        File response with report
    """
    try:
        data = request.get_json()
        
        if not data or 'analysis' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        report_format = data.get('format', 'txt').lower()
        if report_format not in ['txt', 'pdf', 'json']:
            return jsonify({'error': 'Invalid format. Use "txt", "pdf", or "json"'}), 400
        
        analysis_results = data['analysis']
        
        # Generate report
        report_gen = ReportGenerator(
            analysis_results,
            analysis_results.get('risk_assessment', {})
        )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if report_format == 'json':
            content = json.dumps(report_gen.generate_report(), indent=2).encode('utf-8')
            filename = f"squres_report_{timestamp}.json"
            mimetype = 'application/json'
            tmp_suffix = '.json'
        elif report_format == 'pdf':
            content = report_gen.generate_pdf_report()
            filename = f"squres_report_{timestamp}.pdf"
            mimetype = 'application/pdf'
            tmp_suffix = '.pdf'
        else:  # txt
            content = report_gen.generate_text_report().encode('utf-8')
            filename = f"squres_report_{timestamp}.txt"
            mimetype = 'text/plain'
            tmp_suffix = '.txt'
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=tmp_suffix) as tmp:
            if isinstance(content, bytes):
                tmp.write(content)
            else:
                tmp.write(content.encode('utf-8'))
            tmp_path = tmp.name
        
        try:
            return send_file(tmp_path, mimetype=mimetype, as_attachment=True, download_name=filename)
        finally:
            # Clean up will be handled by the response, but ensure proper deletion
            os.unlink(tmp_path)
    
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200
