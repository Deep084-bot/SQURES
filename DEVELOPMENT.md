# Development Setup Guide

Complete guide for setting up SQURES for development.

## Prerequisites

- Python 3.8+
- macOS, Linux, or Windows
- git (optional, for version control)

## Initial Setup

### 1. Virtual Environment

```bash
cd /Users/deepmehta/Documents/Projects/SQURES

# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Development Dependencies (Optional)

For development, testing, and code quality:

```bash
pip install pytest pytest-cov flake8 pylint black
```

## Project Structure

```
SQURES/
├── squres/                      # Main package
│   ├── app/
│   │   ├── __init__.py         # Flask factory
│   │   ├── config.py           # Configuration
│   │   ├── routes.py           # API and web routes
│   │   ├── templates/
│   │   │   └── index.html      # Main UI
│   │   ├── static/             # CSS, JS, images
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── validators.py   # Input validation
│   │   └── analysis/
│   │       ├── __init__.py
│   │       ├── analyzer.py     # Static analysis
│   │       ├── evaluator.py    # Risk evaluation
│   │       └── report_generator.py
│   ├── tests/                  # Test suite
│   │   ├── __init__.py
│   │   ├── test_analyzer.py
│   │   └── test_evaluator.py
│   └── run.py                  # Entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick start guide
├── API.md                     # API documentation
├── EXAMPLES.py                # Code examples
├── DEVELOPMENT.md             # This file
└── .gitignore
```

## Running the Application

### Development Mode

```bash
cd squres
python run.py
```

Server starts at `http://localhost:5000`

### Testing Mode

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_analyzer -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Production Mode

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
python -m flask run --host 0.0.0.0 --port 5000
```

## Code Quality

### Format Code

```bash
black squres/
```

### Lint Code

```bash
flake8 squres/ --max-line-length=100
```

### Check Code

```bash
pylint squres/app --disable=C0111
```

## Adding New Features

### 1. New Analysis Metric

Add to `app/analysis/analyzer.py`:

```python
def analyze_file(self, file_path):
    # ... existing code ...
    
    # Add new metric
    result['new_metric'] = compute_new_metric(source_code)
    
    return result
```

### 2. New Risk Rule

Extend `app/analysis/evaluator.py`:

```python
class CustomEvaluator(RiskEvaluator):
    def evaluate_file_risk(self, file_path, file_analysis):
        result = super().evaluate_file_risk(file_path, file_analysis)
        
        # Add custom rule
        if file_analysis['size_lines'] > 500:
            result['risk_level'] = 'High'
            result['reasons'].append('File exceeds 500 lines')
        
        return result
```

### 3. New API Endpoint

Add to `app/routes.py`:

```python
@api_bp.route('/custom', methods=['POST'])
def custom_endpoint():
    # Implementation
    return jsonify({'result': '...'}), 200
```

### 4. New Route Handler

Add to `app/routes.py`:

```python
@web_bp.route('/custom-page')
def custom_page():
    return render_template('custom.html', data=...)
```

## Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug(f"Variable value: {variable}")
```

### Debug with IDE

For VS Code `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "SQURES",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "squres/run.py",
                "FLASK_ENV": "development"
            },
            "args": ["run"],
            "jinja": true,
            "cwd": "${workspaceFolder}/squres"
        }
    ]
}
```

## Database Integration (Future)

To add database support:

```bash
pip install flask-sqlalchemy
```

Create `app/models.py`:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255))
    # ... other fields
```

## API Documentation

### Auto-generate with Swagger

```bash
pip install flask-restx flasgger
```

Use `@swag_from` decorators:

```python
@api_bp.route('/upload', methods=['POST'])
@swag_from('upload_spec.yml')
def upload_file():
    pass
```

## Performance Optimization

### Cache Results

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    return result
```

### Async Analysis

```python
from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379')

@celery.task
def analyze_async(file_path):
    return analyzer.analyze()
```

## Deployment

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "squres/run.py"]
```

Build and run:

```bash
docker build -t squres .
docker run -p 5000:5000 squres
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3'
services:
  squres:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
    volumes:
      - ./squres:/app/squres
```

Run:

```bash
docker-compose up
```

## Monitoring

### Request Logging

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('squres.log', maxBytes=1024*1024*10, backupCount=10)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
```

### Error Tracking

```bash
pip install sentry-sdk
```

Configure:

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

## Troubleshooting Development

### Port Already in Use

```bash
lsof -i :5000
kill -9 <PID>
```

### Module Import Errors

```bash
# Ensure in correct directory
cd squres

# Reinstall dependencies
pip install -r ../requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Database Migrations

If using database:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Contributing Guidelines

1. **Code Style**: Follow PEP 8
2. **Docstrings**: Add docstrings to all functions
3. **Tests**: Write tests for new features
4. **Commit Messages**: Use clear, descriptive messages
5. **Pull Requests**: Link to issues, include tests

Example commit:

```
feat: Add new complexity metric

- Implement XXX analysis
- Add unit tests
- Update documentation

Closes #123
```

## Useful Commands

```bash
# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=term-missing

# Format code
black squres/ --line-length=100

# Sort imports
isort squres/

# Type check
mypy squres/

# Security audit
bandit -r squres/

# Generate requirements
pip freeze > requirements.txt

# Create distribution
python setup.py sdist bdist_wheel
```

## Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... code to profile ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

## Documentation

### Build docs with Sphinx

```bash
pip install sphinx sphinx-rtd-theme

sphinx-quickstart docs
cd docs
make html
```

View at `docs/_build/html/index.html`

## Version Control

### Initialize git

```bash
git init
git add .
git commit -m "Initial commit: SQURES application"
```

### Branch strategy

```bash
# Feature branch
git checkout -b feature/new-metric
# ... work ...
git commit -am "Add new metric"
git checkout main
git merge feature/new-metric

# Hotfix branch
git checkout -b hotfix/security-patch
# ... fix ...
git commit -am "Fix security issue"
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [QUICKSTART.md](QUICKSTART.md) to run the app
3. Review [API.md](API.md) for API details
4. Study [EXAMPLES.py](EXAMPLES.py) for code samples

---

Happy developing! 🚀
