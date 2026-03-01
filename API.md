# SQURES API Documentation

Complete API reference for the SQURES system.

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Upload and Analyze
**Endpoint**: `POST /api/upload`

Upload a zip file containing Python source code and receive immediate analysis results.

#### Request
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body Parameter**: 
  - `file` (required): .zip file containing Python source code

#### Example
```bash
curl -X POST -F "file=@project.zip" \
  http://localhost:5000/api/upload
```

#### Success Response (200)
```json
{
  "status": "success",
  "timestamp": "2026-02-04T10:30:45.123456",
  "analysis": {
    "summary": {
      "total_files": 5,
      "analyzed_files": 5,
      "files_with_errors": 0,
      "total_lines_of_code": 1250,
      "total_complexity": 45,
      "average_complexity": 9.0,
      "average_maintainability_index": 78.5
    },
    "files": {
      "main.py": {
        "path": "/tmp/squres_uploads/.../main.py",
        "relative_path": "main.py",
        "size_lines": 250,
        "cyclomatic_complexity": 15,
        "average_complexity": 7.5,
        "maintainability_index": 75.2,
        "functions": [
          {
            "name": "process_data",
            "type": "function",
            "complexity": 8,
            "lines": 25
          }
        ],
        "errors": []
      }
    },
    "risk_assessment": {
      "summary": {
        "total_files_evaluated": 5,
        "defect_prone_count": 2,
        "risk_distribution": {
          "High": 1,
          "Medium": 1,
          "Low": 3,
          "Unknown": 0
        }
      },
      "file_risks": {
        "main.py": {
          "risk_level": "Medium",
          "reasons": [
            "Average cyclomatic complexity is medium (7.5)"
          ],
          "high_complexity_functions": []
        }
      },
      "defect_prone_modules": [
        {
          "file": "complex_module.py",
          "risk_level": "High",
          "reasons": [
            "Average cyclomatic complexity is high (12.0)",
            "Contains 2 functions with high complexity (≥10)"
          ],
          "high_complexity_functions": [
            {
              "name": "legacy_process",
              "complexity": 14
            }
          ]
        }
      ]
    },
    "report": {
      "generated_at": "2026-02-04T10:30:45.123456",
      "project_summary": {...},
      "file_metrics": [...],
      "risk_classification": {...},
      "defect_prone_modules": [...],
      "recommendations": [...]
    }
  }
}
```

#### Error Responses

**400 - Bad Request** (No file provided)
```json
{
  "error": "No file provided"
}
```

**400 - Bad Request** (Invalid file type)
```json
{
  "error": "Only .zip files are allowed"
}
```

**400 - Bad Request** (File too large)
```json
{
  "error": "File too large. Maximum size is 50 MB"
}
```

**400 - Bad Request** (Invalid zip)
```json
{
  "error": "Invalid zip file format"
}
```

**400 - Bad Request** (No Python files)
```json
{
  "error": "No Python files found in the uploaded archive"
}
```

**500 - Server Error**
```json
{
  "error": "Analysis failed: <error details>"
}
```

---

### 2. Download Report
**Endpoint**: `POST /api/download-report`

Generate and download a formatted analysis report.

#### Request
- **Method**: POST
- **Content-Type**: application/json
- **Body**:
```json
{
  "analysis": {
    "files": {...},
    "risk_assessment": {...}
  },
  "format": "txt"
}
```

#### Format Options
- `txt` (default): Plain text format
- `json`: JSON format

#### Example
```bash
# Download as text
curl -X POST -H "Content-Type: application/json" \
  -d '{"analysis": {...}, "format": "txt"}' \
  http://localhost:5000/api/download-report \
  --output report.txt

# Download as JSON
curl -X POST -H "Content-Type: application/json" \
  -d '{"analysis": {...}, "format": "json"}' \
  http://localhost:5000/api/download-report \
  --output report.json
```

#### Success Response (200)
File download with appropriate MIME type:
- `text/plain` for .txt format
- `application/json` for .json format

#### Error Responses

**400 - Bad Request**
```json
{
  "error": "Invalid request data"
}
```

**400 - Bad Request** (Invalid format)
```json
{
  "error": "Invalid format. Use \"txt\" or \"json\""
}
```

**500 - Server Error**
```json
{
  "error": "Report generation failed: <error details>"
}
```

---

### 3. Health Check
**Endpoint**: `GET /api/health`

Check if the SQURES API is running and healthy.

#### Request
- **Method**: GET

#### Example
```bash
curl http://localhost:5000/api/health
```

#### Response (200)
```json
{
  "status": "healthy",
  "timestamp": "2026-02-04T10:30:45.123456"
}
```

---

## Web Routes

### Upload Page
**Route**: `GET /`

Returns the main upload interface HTML page.

```bash
curl http://localhost:5000/
```

---

## Response Data Structures

### Summary Object
```json
{
  "total_files": 5,
  "analyzed_files": 5,
  "files_with_errors": 0,
  "total_lines_of_code": 1250,
  "total_complexity": 45,
  "average_complexity": 9.0,
  "average_maintainability_index": 78.5
}
```

### File Metric Object
```json
{
  "path": "/tmp/..../main.py",
  "relative_path": "main.py",
  "size_lines": 250,
  "cyclomatic_complexity": 15,
  "average_complexity": 7.5,
  "maintainability_index": 75.2,
  "functions": [
    {
      "name": "process_data",
      "type": "function",
      "complexity": 8,
      "lines": 25
    }
  ],
  "errors": []
}
```

### Risk Assessment Object
```json
{
  "file": "main.py",
  "risk_level": "Medium",
  "reasons": [
    "Average cyclomatic complexity is medium (7.5)"
  ],
  "high_complexity_functions": [
    {
      "name": "process",
      "complexity": 10
    }
  ]
}
```

### Defect-Prone Module Object
```json
{
  "file": "complex.py",
  "risk_level": "High",
  "reasons": [
    "Average cyclomatic complexity is high (12.0)",
    "Contains 2 functions with high complexity (≥10)"
  ],
  "high_complexity_functions": [
    {
      "name": "legacy_process",
      "complexity": 14
    }
  ]
}
```

### Report Object
```json
{
  "generated_at": "2026-02-04T10:30:45.123456",
  "project_summary": {...},
  "file_metrics": [...],
  "risk_classification": {...},
  "defect_prone_modules": [...],
  "recommendations": [...]
}
```

---

## Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Analysis completed |
| 400 | Bad Request | Invalid file format |
| 500 | Server Error | Unexpected error |

---

## Rate Limiting

Currently no rate limiting. For production use, implement:
- Request limits per IP
- Request limits per user
- Concurrent request limits

---

## Security Headers

Consider adding in production:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000
```

---

## CORS Configuration

Currently accepts same-origin requests only. For cross-origin access:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

---

## File Upload Limits

| Aspect | Value |
|--------|-------|
| Max File Size | 50 MB |
| Max Extract Size | Unlimited* |
| Allowed Types | .zip only |
| Temp Storage | `/tmp/squres_uploads` |

*No explicit limit, but consider system resources.

---

## Performance Metrics

Expected analysis times (approximate):

| Code Size | Time |
|-----------|------|
| < 1,000 LOC | < 1 second |
| 1,000 - 5,000 LOC | 1-3 seconds |
| 5,000 - 10,000 LOC | 3-10 seconds |
| > 10,000 LOC | 10-30 seconds |

---

## Example: Complete Analysis Flow

```bash
# 1. Create a test project
mkdir test_project
cd test_project
echo "def foo(): return 42" > main.py
zip -r project.zip main.py

# 2. Upload for analysis
curl -X POST -F "file=@project.zip" \
  http://localhost:5000/api/upload > analysis.json

# 3. Download report
curl -X POST -H "Content-Type: application/json" \
  -d @analysis.json \
  http://localhost:5000/api/download-report \
  --output report.txt

# 4. View report
cat report.txt
```

---

## Webhook Support

Not currently implemented. For async analysis:

1. Submit upload request
2. Receive job ID
3. Poll `/api/status/<job_id>` for progress
4. Retrieve results when complete

---

## Pagination

Not applicable - all results returned in single response.

For large projects, consider implementing pagination:
```json
{
  "files": [...],
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total": 150
  }
}
```

---

## Cache Headers

Currently no caching. Consider adding for reports:

```
Cache-Control: max-age=3600
ETag: "sha256:..."
Last-Modified: ...
```

---

## Future API Enhancements

- [ ] Batch analysis
- [ ] Scheduled analysis
- [ ] Incremental updates
- [ ] Comparison reports
- [ ] Custom rule sets
- [ ] Webhook notifications
- [ ] API keys for authentication
- [ ] Usage analytics

---

*Last Updated: February 2026*
*SQURES API v1.0*
