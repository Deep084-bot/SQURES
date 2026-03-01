# SQURES - Quick Start Guide

Get SQURES running in 5 minutes!

## Installation (macOS)

### 1. Navigate to project directory
```bash
cd /Users/deepmehta/Documents/Projects/SQURES
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Output should show:
```
Successfully installed Flask-2.3.0 radon-6.1 Werkzeug-2.3.0
```

### 4. Run the application
```bash
cd squres
python run.py
```

Output should show:
```
WARNING in flask.app: This is a development server. Do not use it in production.
* Running on http://127.0.0.1:5000
```

### 5. Open in browser
Go to: **http://localhost:5000**

## First Analysis

### Create a test Python project

```bash
# Create a test directory
mkdir -p ~/test_project
cd ~/test_project

# Create some Python files
cat > main.py << 'EOF'
def calculate_tax(amount, rate):
    if amount > 0:
        if rate > 0:
            if rate < 1:
                tax = amount * rate
                return tax
            else:
                return amount
        else:
            return 0
    else:
        return -1

def process_data(data):
    results = []
    for item in data:
        if isinstance(item, dict):
            if 'value' in item:
                results.append(item['value'] * 2)
    return results
EOF

cat > utils.py << 'EOF'
def format_number(n):
    return f"${n:,.2f}"

def validate_email(email):
    return '@' in email and '.' in email
EOF

# Create a zip file
zip -r ~/test_project.zip main.py utils.py
```

### Upload to SQURES

1. Go to http://localhost:5000
2. Click the upload area
3. Select `test_project.zip`
4. Click "Analyze"
5. View results!

## Key Results Explained

### Summary Cards
- **Files Analyzed**: Number of Python files processed
- **Lines of Code**: Total LOC across all files
- **Avg Complexity**: Average cyclomatic complexity
- **Avg Maintainability**: Average MI score
- **Defect-Prone**: Count of flagged modules

### File Metrics Table
| Column | Meaning |
|--------|---------|
| File | Python file path |
| LOC | Lines of code |
| Complexity | Cyclomatic complexity |
| Maintainability | MI score (0-100) |
| Risk | Low/Medium/High assessment |

### Risk Levels
- **Green (Low)**: Well-written, maintainable code
- **Orange (Medium)**: Some quality concerns
- **Red (High)**: Needs refactoring

## API Examples

### Upload and Analyze
```bash
curl -X POST -F "file=@test_project.zip" \
  http://localhost:5000/api/upload | python -m json.tool
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Deactivate Virtual Environment
```bash
deactivate
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [Architecture](#architecture) section for code organization
- Run tests: `python -m unittest discover tests -v`
- Explore the web interface for different metrics

## Troubleshooting

**Port 5000 already in use?**
```bash
# Find what's using it
lsof -i :5000

# Kill the process
kill -9 <PID>
```

**Import errors?**
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt
```

**Can't upload file?**
- File must be .zip format
- File must be under 50 MB
- Zip must contain Python files

---

🎉 **You're all set!** Start analyzing Python projects with SQURES.
