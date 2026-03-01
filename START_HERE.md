# SQURES - START HERE 📖

**Software Quality and Reliability Evaluation System**  
*Complete Flask-based static code analysis platform*

---

## 🎯 What is SQURES?

SQURES is a web-based system that analyzes Python source code to:
- Calculate **Cyclomatic Complexity** (code path complexity)
- Measure **Maintainability Index** (code quality score)
- Identify **defect-prone modules** (high-risk files)
- Generate comprehensive **quality reports**

All without executing any code - completely **safe and secure**.

---

## ⚡ Get Started in 5 Minutes

### 1. Setup Environment
```bash
cd /Users/deepmehta/Documents/Projects/SQURES
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Application
```bash
cd squres
python run.py
```

### 3. Open in Browser
Go to: **http://localhost:5000**

### 4. Upload and Analyze
1. Click the upload area
2. Select a `.zip` file containing Python code
3. Click "Analyze"
4. View results!

**That's it!** You're analyzing code.

---

## 📚 Documentation Guide

Choose based on what you need:

### 🚀 For Quick Setup
→ Read **[QUICKSTART.md](QUICKSTART.md)** (5 min read)

### 📖 For Complete Understanding  
→ Read **[README.md](README.md)** (15 min read)

### 🔌 For API Integration
→ Read **[API.md](API.md)** (10 min read)

### 💻 For Development
→ Read **[DEVELOPMENT.md](DEVELOPMENT.md)** (20 min read)

### 💡 For Code Examples
→ Review **[EXAMPLES.py](EXAMPLES.py)** (15 min read)

### 🎯 For Quick Reference
→ Check **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** (2 min read)

### 📊 For System Details
→ See **[PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)** (detailed)

### ✅ For Implementation Summary
→ Review **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** (overview)

---

## 🎓 What You Get

### Web Interface
- Modern, responsive design
- Drag-and-drop file upload
- Real-time analysis results
- Interactive data tables
- Report download functionality

### Analysis Capabilities
- Cyclomatic Complexity (CC)
- Maintainability Index (MI)
- Lines of Code (LOC)
- Function-level metrics
- Risk classification

### Risk Assessment
- Multi-criteria evaluation
- Defect-prone detection
- Actionable recommendations
- Clear explanations

### Reports
- JSON format (API)
- Text format (readable)
- Project summaries
- File-level details
- Risk analysis

---

## 📁 Project Structure

```
SQURES/
├── 📚 Guides & Documentation (8 files)
├── 📦 squres/                 (Flask application)
│   ├── run.py                 (Start here)
│   ├── app/
│   │   ├── routes.py         (API endpoints)
│   │   ├── analysis/         (Core metrics)
│   │   ├── templates/        (Web UI)
│   │   └── utils/            (Validation)
│   └── tests/                (Unit tests)
└── requirements.txt          (Dependencies)
```

**Total:** 23 files | ~192 KB | ~3,500+ lines of code

---

## 🔧 System Requirements

✅ **Python 3.8+**  
✅ **pip package manager**  
✅ **5 MB disk space** (core + docs)  
✅ **50 MB** (per analysis, auto-deleted)  

---

## 🚀 Key Features

| Feature | Details |
|---------|---------|
| **Static Analysis** | Safe - no code execution |
| **Security** | Path traversal prevention, file validation |
| **Metrics** | CC, MI, LOC, function-level |
| **Risk Assessment** | Rule-based, multi-criteria |
| **Reports** | JSON, text, downloadable |
| **Web Interface** | Modern, responsive, interactive |
| **API** | REST endpoints, JSON responses |
| **Testing** | Unit tests included |

---

## 📊 Understanding Results

### Cyclomatic Complexity (CC)
- **≤ 6**: Low - Simple, well-written
- **7-10**: Medium - Some complexity
- **> 10**: High - Needs refactoring

### Maintainability Index (MI)
- **85-100**: Excellent ✅
- **70-84**: Good ✅  
- **50-69**: Fair ⚠️
- **< 50**: Poor ❌

### Risk Levels
- **Green (Low)**: Well-written, maintained code
- **Orange (Medium)**: Some quality concerns
- **Red (High)**: Significant issues

---

## 💻 Command Reference

### Start Application
```bash
cd /Users/deepmehta/Documents/Projects/SQURES/squres
python run.py
```

### Run Tests
```bash
cd squres
python -m unittest discover tests -v
```

### API Example
```bash
curl -X POST -F "file=@project.zip" \
  http://localhost:5000/api/upload
```

### Stop Server
```
Press Ctrl+C in terminal
```

---

## 🎯 Common Tasks

### Analyze a Python Project
1. Create `.zip` file with Python code
2. Upload via web interface
3. Wait for analysis
4. View results
5. Download report

### Check Code Quality
1. Upload project
2. Look at "Defect-Prone Modules" tab
3. Review high-risk files
4. Check recommendations

### Export Results
1. Complete analysis
2. Click "Download Report"
3. Choose format (txt or json)
4. Save file

### View Metrics
1. Click "File Metrics" tab
2. Sort by CC, MI, or Risk
3. Analyze patterns
4. Identify issues

---

## 🔐 Security Features

✅ **No Code Execution** - Static analysis only  
✅ **File Validation** - Type & size checks  
✅ **Path Safety** - Traversal prevention  
✅ **Auto-Cleanup** - Temp files deleted  
✅ **Input Sanitization** - All inputs validated  

---

## 🚦 Typical Workflow

```
1. CREATE/ZIP PROJECT
   Your Python code → Compress to .zip

2. UPLOAD
   Web interface → Select file → Submit

3. ANALYZE
   System runs metrics & evaluation

4. REVIEW
   View results → Check risks → Read recommendations

5. ACT
   Refactor high-risk files → Improve scores

6. DOWNLOAD
   Save report → Share results → Track progress
```

---

## ❓ FAQ

**Q: Is my code safe?**  
A: Yes! No execution, no storage, auto-deleted after analysis.

**Q: What size files can I upload?**  
A: Up to 50 MB (configurable).

**Q: What Python versions does it support?**  
A: Any Python code! Uses static analysis.

**Q: Can I use it offline?**  
A: Yes, run locally. No internet needed.

**Q: How do I integrate it?**  
A: Use REST API or import Python modules directly.

**Q: Can I modify the metrics?**  
A: Yes! See DEVELOPMENT.md for customization.

---

## 🎓 Learn More

| Topic | File | Time |
|-------|------|------|
| Setup | QUICKSTART.md | 5 min |
| Features | README.md | 15 min |
| API | API.md | 10 min |
| Development | DEVELOPMENT.md | 20 min |
| Examples | EXAMPLES.py | 15 min |
| Reference | QUICK_REFERENCE.md | 2 min |

---

## 🎯 Next Steps

### Immediate (Now)
1. ✅ Run: `python run.py` in squres/
2. ✅ Upload: Test project to http://localhost:5000
3. ✅ Review: Analyze the results

### Short-term (Today)
1. Read QUICKSTART.md
2. Try analyzing your own code
3. Download a report
4. Review recommendations

### Long-term (This Week)
1. Read full README.md
2. Study the API (API.md)
3. Integrate with your workflow
4. Customize for your needs

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│         Web Browser / API Client        │
└────────────────────┬────────────────────┘
                     │
┌─────────────────────▼────────────────────┐
│      Flask Web Application (routes.py)   │
│  ┌─────────────────────────────────────┐ │
│  │  Upload → Validation → Extraction   │ │
│  └────────────────┬────────────────────┘ │
└─────────────────────────────────────────┘
                     │
┌─────────────────────▼──────────────────────┐
│     Static Analysis (analyzer.py)          │
│  • Cyclomatic Complexity (radon)           │
│  • Maintainability Index (radon)           │
│  • Metrics calculation                     │
└────────────────────┬──────────────────────┘
                     │
┌─────────────────────▼──────────────────────┐
│   Risk Evaluation (evaluator.py)           │
│  • Rule-based assessment                   │
│  • Risk categorization                     │
│  • Defect detection                        │
└────────────────────┬──────────────────────┘
                     │
┌─────────────────────▼──────────────────────┐
│   Report Generation (report_generator.py)  │
│  • JSON report                             │
│  • Text report                             │
│  • Recommendations                         │
└────────────────────┬──────────────────────┘
                     │
┌─────────────────────▼──────────────────────┐
│      Response → Display / Download         │
└──────────────────────────────────────────┘
```

---

## 📞 Support Resources

**Documentation:**
- README.md - Complete reference
- API.md - Endpoint documentation  
- QUICKSTART.md - Quick setup
- EXAMPLES.py - Code samples

**Code:**
- squres/app/ - Application code
- squres/tests/ - Test examples
- config.py - Configuration

**Help:**
- Check DEVELOPMENT.md for troubleshooting
- Review EXAMPLES.py for integration
- Study test files for usage patterns

---

## ✨ Key Highlights

🎯 **Complete System**
- Fully functional Flask application
- REST API
- Modern web interface
- Comprehensive analysis

📊 **Reliable Metrics**
- Industry-standard calculations
- Using proven radon library
- Configurable thresholds
- Detailed breakdowns

🔒 **Secure by Design**
- No code execution
- File validation
- Automatic cleanup
- Input sanitization

📚 **Well Documented**
- 8 comprehensive guides
- Code examples
- API documentation
- Development setup

🧪 **Test Coverage**
- Unit tests included
- Integration examples
- Test data provided
- Extensible framework

---

## 🚀 Launch Now!

```bash
# Three commands to start analyzing:

cd /Users/deepmehta/Documents/Projects/SQURES
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt && cd squres && python run.py
```

Then open: **http://localhost:5000** 🎉

---

## 📋 Checklist

Before starting, verify:

- ✅ Python 3.8+ installed
- ✅ Virtual environment created
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ You're in `/squres/` directory
- ✅ Port 5000 is available

---

## 🎓 What You'll Learn

Using SQURES, you'll understand:
- How to measure code quality
- What metrics matter
- How to identify problem code
- How to refactor for improvement
- How to build Flask applications
- Static analysis techniques

---

## 📖 Recommended Reading Order

1. **This file** (You are here!) - 5 min
2. **QUICKSTART.md** - Quick setup guide
3. **README.md** - Full documentation
4. **QUICK_REFERENCE.md** - Cheat sheet
5. **API.md** - If using API
6. **DEVELOPMENT.md** - If extending
7. **EXAMPLES.py** - Code samples
8. **PROJECT_STRUCTURE.txt** - Details

---

## 🎯 Your Next Action

**RIGHT NOW:**
```bash
cd /Users/deepmehta/Documents/Projects/SQURES/squres
python run.py
```

**Then open:**
```
http://localhost:5000
```

**And upload:** Any .zip file with Python code!

---

## 🎉 You're Ready!

Everything is set up and ready to use. Start analyzing code with SQURES!

Questions? Check the documentation files above.  
Need help? See DEVELOPMENT.md for troubleshooting.  
Want examples? Review EXAMPLES.py.  

**Happy analyzing!** 🚀

---

**SQURES v1.0** | February 2026  
*Software Quality and Reliability Evaluation System*  
Academic & Research Use

---

*Last Updated: February 4, 2026*
