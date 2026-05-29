# 📝 Prompt Log — AI-Based Resume Analyzer

This document logs all the AI prompts used during the development of the AI-Based Resume Analyzer project.

---

## Prompt 1: Initial Project Request

**Prompt:**
```
AI-Based Resume Analyzer
Features:
● Skill extraction
● Keyword matching
● Resume scoring
```

**Response Summary:**
- Created a complete web application (HTML/CSS/JS) with a dual-panel layout
- Built a comprehensive skill database with 400+ skills across 8 categories
- Implemented regex-based skill extraction engine
- Designed keyword matching against job descriptions
- Created a scoring algorithm with 3 sub-scores (Skill Match, Keyword Match, Structure)
- Added premium UI with glassmorphism, dark/light themes, and animations

---

## Prompt 2: Convert to Python

**Prompt:**
```
make this into python language
```

**Response Summary:**
- Converted the entire application from HTML/CSS/JS to a Python console application
- Preserved all 400+ skills in the database
- Added colored terminal output using ANSI escape codes
- Implemented progress bars, spinners, and formatted tables
- Created interactive mode with menu options
- Added `--sample` and `--resume` command-line flags
- All logic runs using only Python standard library (zero dependencies)

---

## Prompt 3: Add File Upload Support

**Prompt:**
```
add the file attachment in this code so I can upload my resume in it
```

**Response Summary:**
- Added native file picker dialog using tkinter (built-in Python)
- Added PDF support via PyPDF2 library
- Added DOCX support via python-docx library
- Implemented auto-install prompts for missing libraries
- Added new menu option `[4] 📎 Browse & attach resume file (PDF/DOCX/TXT)`
- Handles image-based PDFs, encoding issues, and empty files gracefully
- Falls back to manual path entry if file dialog fails

---

## Prompt 4: Create Submission Folder Structure

**Prompt:**
```
├── Source_Code/
├── Screenshots/
├── Prompt_Log/
├── Report.pdf
Antigravity
├── README.md
└── GitHub_Link.txt
make this on same topic
```

**Response Summary:**
- Created the complete submission folder structure
- Generated README.md with features, installation, usage, and architecture
- Created Report.md with detailed project documentation
- Created this Prompt_Log.md
- Created GitHub_Link.txt with push instructions
- Copied source code to Source_Code/
- Generated screenshots of the application

---

## Tools & Technologies Used During Development

| Tool | Purpose |
|------|---------|
| Antigravity AI | Code generation, debugging, and documentation |
| Python 3.13 | Runtime environment |
| VS Code | Code editor |
| Windows Terminal | Testing and execution |

---

## Key Design Decisions Made via AI Prompts

1. **Skill Database Approach**: Used a comprehensive regex-based skill database (400+ entries) instead of ML-based extraction for zero-dependency operation
2. **Scoring Formula**: Weighted scoring — Skill Match (45%) + Keyword Match (30%) + Structure (25%)
3. **File Format Support**: PDF, DOCX, TXT with auto-install for optional libraries
4. **Terminal UI**: ANSI color codes for rich terminal output instead of a GUI framework
5. **Privacy**: All processing runs locally — no data sent to external servers
