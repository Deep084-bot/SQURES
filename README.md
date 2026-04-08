# SQURES - Software Quality and Reliability Evaluation System

A Flask-based web application for static analysis of Python source code with comprehensive quality and reliability metrics.

## Features

### Core Functionality
- **File Upload**: Secure upload of compressed Python projects (.zip files)
- **Static Analysis**: No code execution - safe analysis using radon library
- **Quality Metrics**:
  - Cyclomatic Complexity (per file and per function)
  - Maintainability Index (0-100 scale)
  - Lines of Code statistics
  
- **Risk Assessment**: Rule-based evaluation identifying defect-prone modules
- **Comprehensive Reports**: JSON and text format report generation
- **Interactive Dashboard**: Modern web interface with real-time results

### Security Features
- Path traversal prevention in zip files
- Upload size limits (50 MB default)
- No permanent storage of source code
- Temporary file cleanup after analysis
- Input validation and sanitization

## Project Structure

```
SQURES/
├── squres/
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── routes.py                # API and web routes
│   │   ├── config.py                # Configuration management
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── validators.py        # Input validation utilities
│   │   ├── analysis/
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py          # Static code analyzer
│   │   │   ├── evaluator.py         # Risk evaluator
│   │   │   └── report_generator.py  # Report generation
│   │   ├── templates/
│   │   │   └── index.html           # Web interface
│   │   └── static/                  # Static assets
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_analyzer.py         # Analyzer tests
│   │   └── test_evaluator.py        # Evaluator tests
│   └── run.py                       # Application entry point
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**:
```bash
cd /Users/deepmehta/Documents/Projects/SQURES
```

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
cd squres
python run.py
```

The application will be available at: `http://localhost:5000`

### Production Mode

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
python -m flask run --host 0.0.0.0
```

## Usage

### Via Web Interface

1. Open http://localhost:5000 in your browser
2. Click the upload area or drag and drop a .zip file
3. Click "Analyze" to start the analysis
4. View results in the interactive dashboard:
   - **File Metrics**: Detailed metrics for each Python file
   - **Risk Assessment**: Classification of files by risk level
   - **Defect-Prone Modules**: Files requiring attention

5. Download the report in text or JSON format

### Via API

#### Upload and Analyze
```bash
curl -X POST -F "file=@project.zip" http://localhost:5000/api/upload
```

Response:
```json
{
  "status": "success",
  "timestamp": "2026-02-04T...",
  "analysis": {
    "summary": { ... },
    "files": { ... },
    "risk_assessment": { ... },
    "report": { ... }
  }
}
```

#### Download Report
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"analysis": {...}}' \
  http://localhost:5000/api/download-report \
  --output report.txt
```

#### Health Check
```bash
curl http://localhost:5000/api/health
```

## Metrics Explanation

### Cyclomatic Complexity (CC)
Measures the number of independent code paths through a function.
- **Low (≤6)**: Simple, easy to understand code
- **Medium (7-10)**: Moderate complexity, manageable
- **High (>10)**: Complex code, high defect risk

### Maintainability Index (MI)
Composite metric ranging from 0 to 100:
- **90-100**: Highly maintainable
- **70-89**: Maintainable with some concerns
- **50-69**: Low maintainability
- **<50**: Very difficult to maintain

### Risk Levels

**Low Risk**: 
- Average CC ≤ 6
- MI ≥ 85
- Few high-complexity functions

**Medium Risk**:
- Average CC 7-10 or MI 65-84
- Some high-complexity functions

**High Risk**:
- Average CC > 10 or MI < 65
- Multiple functions with CC ≥ 10

## Architecture

### StaticCodeAnalyzer
- Recursively finds Python files
- Computes CC using radon's cc_visit()
- Computes MI using radon's mi_visit()
- Returns structured analysis results

### RiskEvaluator
- Rule-based threshold evaluation
- Categorizes files by risk level
- Identifies defect-prone modules
- Provides clear explanations for each assessment

### ReportGenerator
- Generates comprehensive reports
- Supports JSON and text formats
- Includes project summary and recommendations
- Deterministic and reproducible output

## Configuration

Edit `squres/config.py` to customize:

```python
# Maximum upload size
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

# Temporary upload folder
UPLOAD_FOLDER = '/tmp/squres_uploads'

# Risk thresholds
COMPLEXITY_HIGH = 10
COMPLEXITY_MEDIUM = 7
MI_LOW = 65
MI_MEDIUM = 85
```

## Testing

Run the test suite:

```bash
cd squres
python -m unittest discover tests -v
```

Run specific test:

```bash
python -m unittest tests.test_analyzer.TestStaticCodeAnalyzer -v
```

## Deploying on Render

This repository is deployment-ready for Render using the included `render.yaml`.

### One-time setup

1. Push this repository to GitHub.
2. In Render, choose **New +** -> **Blueprint**.
3. Connect the repository and select this project.
4. Render will detect `render.yaml` and create the web service automatically.

### Runtime details

- Build command: `pip install -r requirements.txt`
- Start command: `cd squres && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
- App entrypoint: `squres/wsgi.py`

### Required environment variables

- `FLASK_ENV=production` (already set in `render.yaml`)
- `SECRET_KEY` (auto-generated in `render.yaml`)
- `PYTHON_VERSION=3.11.9` (set in `render.yaml`)

## Error Handling

The application handles various error scenarios:

- **Invalid file format**: Only .zip files accepted
- **File too large**: 50 MB default limit
- **Path traversal**: Zip files checked for malicious paths
- **Syntax errors**: Individual files skipped with error reporting
- **Missing Python files**: Clear error when no .py files found

## Performance Considerations

- Analysis time depends on code size and complexity
- Large projects (>10,000 LOC) may take 5-30 seconds
- Temporary files cleaned up automatically after analysis
- No database dependencies for fast operation

## Security Best Practices

✅ **Implemented**:
- No code execution (static analysis only)
- Path traversal prevention
- File size limits
- Input validation
- Secure temporary file handling
- Automatic cleanup

⚠️ **Recommendations**:
- Use HTTPS in production
- Set strong SECRET_KEY
- Implement rate limiting
- Run behind a reverse proxy
- Monitor disk space for temp files

## Troubleshooting

### Port Already in Use
```bash
lsof -i :5000  # Find process using port 5000
kill -9 <PID>  # Kill the process
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Temporary Files Not Cleaned
Check `/tmp/squres_uploads` and clean manually if needed:
```bash
rm -rf /tmp/squres_uploads/*
```

## Contributing

To extend SQURES:

1. **Add new metrics**: Extend `analyzer.py`
2. **Add new risk rules**: Modify `evaluator.py`
3. **New report formats**: Extend `report_generator.py`
4. **API endpoints**: Add to `routes.py`

## License

Academic use - All rights reserved

## Support

For issues or questions, refer to:
- Inline code documentation
- Test files for usage examples
- README.md sections above

## Future Enhancements

- [ ] Integration with static analysis tools (pylint, flake8)
- [ ] Historical trend analysis
- [ ] Automated code quality suggestions
- [ ] Team collaboration features
- [ ] Database support for report archival
- [ ] Export to multiple formats (PDF, XLSX)
- [ ] Real-time analysis progress updates
- [ ] Machine learning-based risk prediction

---

**SQURES v1.0** - Built for academic software quality assessment
