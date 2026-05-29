# AI-Based Resume Analyzer — Project Report

---

## 1. Introduction

### 1.1 Project Title
**AI-Based Resume Analyzer**

### 1.2 Project Overview
The AI-Based Resume Analyzer is a Python-based command-line application that intelligently analyzes resumes against job descriptions. It extracts skills, matches keywords, evaluates resume structure, and provides a comprehensive score with actionable improvement suggestions.

### 1.3 Objective
The primary objectives of this project are:
- **Skill Extraction**: Automatically identify technical and soft skills from resume text
- **Keyword Matching**: Compare resume content against job description requirements
- **Resume Scoring**: Provide a quantitative score (0-100) based on multiple evaluation criteria
- **Error Handling**: Gracefully handle various input formats, edge cases, and user errors

### 1.4 Problem Statement
Job seekers often struggle to tailor their resumes to specific job descriptions. Manual comparison between a resume and a job posting is time-consuming and error-prone. This tool automates the process, providing instant feedback on how well a resume aligns with a target position.

---

## 2. System Design

### 2.1 Architecture

```
┌──────────────────────────────────────────────────────┐
│                   INPUT LAYER                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ Text Paste  │  │ File Upload  │  │ Sample Data│  │
│  │             │  │ PDF/DOCX/TXT │  │            │  │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘  │
│         └────────────────┼────────────────┘          │
│                          ▼                           │
│  ┌───────────────────────────────────────────────┐   │
│  │            TEXT EXTRACTION ENGINE              │   │
│  │  • PyPDF2 (PDF)  • python-docx (DOCX)        │   │
│  │  • UTF-8/Latin-1 (TXT)                        │   │
│  └───────────────────────┬───────────────────────┘   │
└──────────────────────────┼───────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────┐
│                 ANALYSIS ENGINE                      │
│                                                      │
│  ┌─────────────────┐  ┌──────────────────────────┐   │
│  │ Skill Extractor │  │ Keyword Extractor        │   │
│  │ (400+ regex DB) │  │ (Phrases + Action Verbs) │   │
│  └────────┬────────┘  └────────────┬─────────────┘   │
│           ▼                        ▼                 │
│  ┌─────────────────────────────────────────────┐     │
│  │          MATCHING ENGINE                    │     │
│  │  • Skill Match (Resume vs JD)               │     │
│  │  • Keyword Match (Found vs Missing)         │     │
│  │  • Structure Analysis (Sections, Bullets)   │     │
│  └─────────────────────┬───────────────────────┘     │
│                        ▼                             │
│  ┌─────────────────────────────────────────────┐     │
│  │          SCORING ENGINE                     │     │
│  │  Score = Skill(45%) + KW(30%) + Struct(25%) │     │
│  └─────────────────────┬───────────────────────┘     │
│                        ▼                             │
│  ┌─────────────────────────────────────────────┐     │
│  │       SUGGESTION GENERATOR                  │     │
│  │  Actionable tips based on gap analysis      │     │
│  └─────────────────────────────────────────────┘     │
└──────────────────────────┬───────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────┐
│                   OUTPUT LAYER                       │
│  • Score Display (colored progress bars)             │
│  • Skill Chips (matched ✓ / extra ◦)                │
│  • Keyword Grid (found ● / missing ○)               │
│  • Missing Skills List                               │
│  • Improvement Tips                                  │
└──────────────────────────────────────────────────────┘
```

### 2.2 Modules

| Module | Function | Lines of Code |
|--------|----------|:------------:|
| `SKILL_DATABASE` | 400+ regex patterns across 8 categories | ~120 |
| `SKILL_CAPITALIZATION` | Proper name formatting for 150+ skills | ~80 |
| `extract_skills()` | Regex-based skill extraction from text | ~25 |
| `extract_keywords()` | JD keyword/phrase extraction | ~45 |
| `analyze_structure()` | Resume format & quality scoring | ~50 |
| `analyze_resume()` | Main analysis orchestrator | ~45 |
| `generate_suggestions()` | Actionable tip generation | ~55 |
| `Terminal UI` | Colored output, progress bars, formatting | ~130 |
| `File I/O` | PDF/DOCX/TXT reading + file dialog | ~100 |
| **Total** | | **~1100** |

---

## 3. Features in Detail

### 3.1 Skill Extraction

The skill extraction engine uses a curated database of **400+ skills** organized into 8 categories:

| Category | Examples | Count |
|----------|----------|:-----:|
| Programming Languages | JavaScript, Python, Java, C++, SQL | 40+ |
| Frameworks & Libraries | React, Django, Spring Boot, Flutter | 50+ |
| Cloud & DevOps | AWS, Docker, Kubernetes, Terraform | 70+ |
| Databases | PostgreSQL, MongoDB, Redis, Firebase | 30+ |
| Data & AI/ML | TensorFlow, PyTorch, Pandas, Spark | 60+ |
| Tools & Practices | Git, Jira, Jest, Webpack, npm | 50+ |
| Soft Skills | Leadership, Agile, Communication | 35+ |
| Security & Architecture | Microservices, CI/CD, OAuth, DDD | 50+ |

**How it works:**
- Each skill has a regex pattern designed to match variations (e.g., `react`, `React.js`, `ReactJS` all map to `React`)
- Word boundary detection prevents false matches (e.g., `Java` doesn't match `JavaScript`)
- Results are normalized to proper capitalization using a lookup table

### 3.2 Keyword Matching

The keyword matcher extracts three types of keywords from job descriptions:

1. **Important Phrases** — "full stack", "server-side rendering", "high availability", etc.
2. **Action Verbs** — "develop", "design", "architect", "scale", etc. (with conjugation matching)
3. **Requirements** — Years of experience, degree requirements, certifications

### 3.3 Resume Scoring

The scoring formula evaluates three dimensions:

```
Overall Score = (Skill Match × 0.45) + (Keyword Match × 0.30) + (Structure × 0.25)
```

**Structure Analysis checks for:**
- Contact information (email, LinkedIn, GitHub, phone)
- Key sections (Experience, Education, Skills, Summary, Projects, Certifications)
- Word count (optimal: 150-1200 words)
- Bullet points usage
- Quantifiable achievements (numbers, percentages)
- Action verbs at start of bullet points

**Score Verdicts:**
| Score Range | Verdict | Color |
|:-----------:|---------|-------|
| 80-100 | 🎯 Excellent Match | Green |
| 60-79 | ✅ Good Match | Cyan |
| 40-59 | ⚠️ Fair Match | Yellow |
| 0-39 | ❌ Poor Match | Red |

### 3.4 File Upload Support

| Feature | Implementation |
|---------|---------------|
| File Picker | Native OS dialog via `tkinter.filedialog` |
| PDF Reading | `PyPDF2` with page-by-page text extraction |
| DOCX Reading | `python-docx` paragraph extraction |
| TXT Reading | UTF-8 with Latin-1 fallback |
| Auto-Install | Prompts user to install missing libraries |
| Error Handling | Scanned PDFs, empty files, unsupported formats |

### 3.5 Error Handling

| Scenario | Handling |
|----------|---------|
| Input too short (< 20 chars) | Error message + exit |
| File not found | Clear error with file path |
| Unsupported file format | Lists supported formats |
| Scanned/image-based PDF | Warning + suggestion to paste text |
| Empty DOCX file | Warning message |
| Unicode encoding errors | Automatic fallback to Latin-1 |
| Missing Python library | Prompts to auto-install |
| Division by zero (0 JD skills) | Defaults to 50% score |
| tkinter unavailable | Falls back to manual path entry |

---

## 4. Testing

### 4.1 Sample Data Test

The built-in sample data produces the following results:

```
Overall Score:    85/100  (Excellent Match)
Skill Match:      91%     (32 skills matched)
Keyword Match:    65%     (11/17 found)
Structure Score:  100%    (All sections present)
Skills Extracted: 53 total
Missing Skills:   3 (Agile, Communication, NoSQL)
```

### 4.2 Test Cases

| Test Case | Input | Expected | Result |
|-----------|-------|----------|--------|
| Sample resume + JD | Built-in data | Score 80+ | ✅ 85 |
| Empty resume | "" | Error message | ✅ Pass |
| Short resume | "Hi" | Too short error | ✅ Pass |
| PDF file upload | .pdf file | Text extracted | ✅ Pass |
| DOCX file upload | .docx file | Text extracted | ✅ Pass |
| TXT file upload | .txt file | Text loaded | ✅ Pass |
| Unsupported file | .jpg file | Format error | ✅ Pass |
| No matching skills | Unrelated resume | Low score | ✅ Pass |

---

## 5. Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.8+ | Core programming language |
| `re` | Standard lib | Regular expression matching |
| `tkinter` | Standard lib | Native file picker dialog |
| `os`, `sys` | Standard lib | File and system operations |
| `textwrap` | Standard lib | Text formatting |
| `time` | Standard lib | Loading animations |
| `subprocess` | Standard lib | Auto-install packages |
| PyPDF2 | Latest | PDF text extraction (optional) |
| python-docx | Latest | DOCX text extraction (optional) |

---

## 6. How to Run

### Quick Start
```bash
# Demo with sample data
python resume_analyzer.py --sample

# Interactive mode
python resume_analyzer.py

# Load resume from file
python resume_analyzer.py --resume myresume.pdf
```

### Interactive Menu
```
Choose an option:
  [1] Paste resume & job description manually
  [2] Use sample data (demo)
  [3] Enter resume file path
  [4] 📎 Browse & attach resume file (PDF/DOCX/TXT)
```

---

## 7. Limitations

1. **Text-based PDFs only** — Cannot extract text from scanned/image-based PDFs (would need OCR)
2. **English language only** — Skill database and patterns are in English
3. **No AI/ML model** — Uses pattern matching, not a trained NLP model
4. **Console-based UI** — No graphical interface (terminal colors only)
5. **Single-page resumes work best** — Very long resumes may have duplicate matches

---

## 8. Future Scope

1. **AI Integration** — Connect to OpenAI/Gemini API for context-aware suggestions
2. **Web Interface** — Build a Flask/Streamlit GUI version
3. **ATS Compatibility** — Check resume formatting for Applicant Tracking Systems
4. **Multi-language** — Support resumes in other languages
5. **PDF Report Export** — Generate analysis results as a downloadable PDF
6. **Resume Templates** — Suggest templates based on industry and role

---

## 9. Conclusion

The AI-Based Resume Analyzer successfully demonstrates the core features of skill extraction, keyword matching, and resume scoring. With a database of 400+ skills, intelligent pattern matching, and a weighted scoring algorithm, it provides meaningful and actionable feedback to job seekers. The tool runs entirely offline, ensuring complete data privacy, and supports multiple file formats for maximum accessibility.

---

## 10. References

1. Python Documentation — https://docs.python.org/3/
2. Regular Expressions (re module) — https://docs.python.org/3/library/re.html
3. PyPDF2 Documentation — https://pypdf2.readthedocs.io/
4. python-docx Documentation — https://python-docx.readthedocs.io/
5. ANSI Escape Codes — https://en.wikipedia.org/wiki/ANSI_escape_code

---

*Report prepared by: Abhinav Singh*
*Date: May 2026*
*Tool: AI-Based Resume Analyzer v1.0*
