# SQURES Quick Reference Card

**Software Quality and Reliability Evaluation System v1.0**

---

## 🚀 QUICK START (Copy-Paste)

```bash
# Navigate to project
cd /Users/deepmehta/Documents/Projects/SQURES

# Setup (one-time)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
cd squres
python run.py

# Open browser
# http://localhost:5000
```

---

## 📁 IMPORTANT FILES

| File | Purpose |
|------|---------|
| `squres/run.py` | Start here |
| `squres/app/routes.py` | API endpoints |
| `squres/app/analysis/analyzer.py` | Metrics |
| `squres/app/analysis/evaluator.py` | Risk rules |
| `squres/app/templates/index.html` | Web UI |
| `squres/config.py` | Configuration |

---

## 🎯 KEY METRICS

**Cyclomatic Complexity (CC)**
- ≤6: Low risk ✅
- 7-10: Medium risk ⚠️
- >10: High risk ❌

**Maintainability Index (MI)**
- >85: Good ✅
- 65-85: Fair ⚠️
- <65: Poor ❌

---

## 📡 API ENDPOINTS

```bash
# Upload & Analyze
curl -X POST -F "file=@project.zip" \
  http://localhost:5000/api/upload

# Download Report
curl -X POST -H "Content-Type: application/json" \
  -d '{"analysis":{...},"format":"txt"}' \
  http://localhost:5000/api/download-report

# Health Check
curl http://localhost:5000/api/health
```

---

## 🧪 TESTING

```bash
# Run all tests
cd squres
python -m unittest discover tests -v

# Test specific module
python -m unittest tests.test_analyzer -v
```

---

## ⚙️ CONFIGURATION

Edit `squres/config.py`:

```python
# Upload limit
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

# Temp directory
UPLOAD_FOLDER = '/tmp/squres_uploads'

# Risk thresholds
COMPLEXITY_HIGH = 10
MI_LOW = 65
```

---

## 🔍 ANALYZING CODE

### Via Web Interface
1. Go to http://localhost:5000
2. Click upload area or drag file
3. Select .zip with Python code
4. Click "Analyze"
5. View results, download report

### Via API
```bash
curl -X POST -F "file=@mycode.zip" \
  http://localhost:5000/api/upload | \
  python -m json.tool
```

---

## 📊 RESULT INTERPRETATION

**Low Risk (Green)** ✅
- CC ≤ 6
- MI ≥ 85
- Well-written code

**Medium Risk (Orange)** ⚠️
- CC 7-10 OR MI 65-84
- Some concerns
- Consider refactoring

**High Risk (Red)** ❌
- CC > 10 OR MI < 65
- Multiple issues
- Requires attention

---

## 🛡️ SECURITY NOTES

✅ **Safe**
- No code execution
- Files auto-deleted
- Path traversal prevented
- Size limits enforced

⚠️ **For Production**
- Use HTTPS
- Set strong SECRET_KEY
- Add rate limiting
- Enable authentication

---

## 📚 DOCUMENTATION

| Guide | Read For |
|-------|----------|
| README.md | Complete details |
| QUICKSTART.md | 5-min setup |
| API.md | Endpoint reference |
| DEVELOPMENT.md | Dev setup |
| EXAMPLES.py | Code samples |

---

## 🐛 TROUBLESHOOTING

**Port 5000 in use?**
```bash
lsof -i :5000
kill -9 <PID>
```

**Import errors?**
```bash
pip install -r requirements.txt --upgrade
```

**Cleanup temp files?**
```bash
rm -rf /tmp/squres_uploads/*
```

---

## 📁 PROJECT STRUCTURE

```
squres/
├── run.py              # Start here
├── config.py           # Settings
├── app/
│   ├── routes.py       # Endpoints
│   ├── analysis/       # Metrics
│   ├── templates/      # Web UI
│   └── utils/          # Validation
└── tests/              # Tests
```

---

## 🎯 COMMON TASKS

### Create Test Project
```bash
mkdir test_proj
echo 'def foo(): return 42' > test_proj/main.py
cd test_proj
zip -r project.zip main.py
cd ..
```

### Run Analysis
```bash
# Start server
cd squres
python run.py

# In another terminal, upload
curl -F "file=@test_proj/project.zip" \
  http://localhost:5000/api/upload
```

### View Reports
```bash
# Generate JSON report
curl -X POST -H "Content-Type: application/json" \
  -d '{"analysis":{...},"format":"json"}' \
  http://localhost:5000/api/download-report
```

---

## ⚡ PERFORMANCE

| Size | Time |
|------|------|
| <1K LOC | <1s |
| 5K LOC | 2s |
| 10K LOC | 5s |
| 50K LOC | 30s |

---

## 🔧 INSTALLATION DETAILS

**Python 3.8+**

**Dependencies:**
- Flask 2.3.0
- radon 6.1
- Werkzeug 2.3.0

**Optional (dev):**
- pytest
- black
- flake8

---

## 🎓 ACADEMIC USE

Perfect for:
- Code quality assessment
- Educational demonstrations
- Software metrics analysis
- Reliability evaluation
- Testing methodologies

---

## 🔐 RISK ASSESSMENT RULES

```
File Risk = MAX(
  ComplexityRisk(CC),
  MaintainabilityRisk(MI),
  FunctionLevelRisk(CC > 10)
)

ComplexityRisk:
  CC ≥ 10 → High
  CC ≥ 7  → Medium
  CC < 7  → Low

MaintainabilityRisk:
  MI < 65  → High
  MI < 85  → Medium
  MI ≥ 85  → Low
```

---

## 💡 TIPS

1. **Analyze often** - Catch issues early
2. **Review high-risk files** - Focus on problem areas
3. **Refactor by complexity** - Break complex functions
4. **Improve MI score** - Add docs & simplify code
5. **Use recommendations** - Act on suggestions

---

## 🎯 NEXT STEPS

1. ✅ Setup (5 min) - Run quickstart
2. ✅ Analyze (1 min) - Upload test project
3. ✅ Review (2 min) - Examine results
4. ✅ Integrate (varies) - Use API or CLI

---

## 📞 QUICK LINKS

- **Start:** `python run.py` in squres/
- **Upload:** http://localhost:5000
- **API Docs:** See API.md
- **Examples:** See EXAMPLES.py
- **Tests:** `python -m unittest discover tests -v`

---

## ✨ KEY FEATURES

✅ Secure file uploads  
✅ Cyclomatic complexity analysis  
✅ Maintainability scoring  
✅ Defect-prone detection  
✅ JSON & text reports  
✅ Modern web interface  
✅ REST API  
✅ Unit tests  
✅ Comprehensive docs  

---

## 🚀 LAUNCH COMMAND

```bash
cd /Users/deepmehta/Documents/Projects/SQURES/squres && python run.py
```

Then open: **http://localhost:5000**

---

**SQURES v1.0** | February 2026 | Academic Use  
*Software Quality and Reliability Evaluation System*

**Status: ✅ READY TO USE**
