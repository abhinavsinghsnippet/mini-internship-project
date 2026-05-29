

import re
import os
import sys
import math
import textwrap
import time
import subprocess
from collections import OrderedDict


# ═══════════════════════════════════════════════════════════════
#  ANSI COLOR HELPERS
# ═══════════════════════════════════════════════════════════════

class Colors:
    """ANSI escape codes for terminal styling."""
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"
    ITALIC     = "\033[3m"
    UNDERLINE  = "\033[4m"

    # Foreground
    BLACK      = "\033[30m"
    RED        = "\033[31m"
    GREEN      = "\033[32m"
    YELLOW     = "\033[33m"
    BLUE       = "\033[34m"
    MAGENTA    = "\033[35m"
    CYAN       = "\033[36m"
    WHITE      = "\033[37m"

    # Bright foreground
    B_RED      = "\033[91m"
    B_GREEN    = "\033[92m"
    B_YELLOW   = "\033[93m"
    B_BLUE     = "\033[94m"
    B_MAGENTA  = "\033[95m"
    B_CYAN     = "\033[96m"
    B_WHITE    = "\033[97m"

    # Background
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"

    @staticmethod
    def enable():
        """Enable ANSI colors on Windows."""
        if sys.platform == "win32":
            os.system("")  # Enables ANSI escape sequences on Windows 10+


def c(text, *styles):
    """Apply color/style codes to text."""
    return "".join(styles) + str(text) + Colors.RESET


# ═══════════════════════════════════════════════════════════════
#  SKILL DATABASE — comprehensive taxonomy (400+ skills)
# ═══════════════════════════════════════════════════════════════

SKILL_DATABASE = {
    "Programming Languages": [
        r"javascript", r"typescript", r"python", r"java(?!script)", r"c\+\+", r"c#",
        r"\bc\b", r"ruby", r"\bgo\b", r"golang", r"rust", r"swift",
        r"kotlin", r"php", r"scala", r"perl", r"\br\b", r"matlab", r"dart",
        r"lua", r"haskell", r"elixir", r"clojure", r"objective-c",
        r"groovy", r"julia", r"f#", r"vba",
        r"\bsql\b", r"nosql", r"graphql", r"\bhtml\b", r"\bcss\b",
        r"sass", r"scss", r"less", r"\bxml\b", r"\bjson\b", r"\byaml\b",
    ],
    "Frameworks & Libraries": [
        r"react(?:\.js|js)?", r"angular(?:js)?", r"vue(?:\.js|js)?", r"svelte",
        r"next\.js|nextjs", r"nuxt(?:\.js)?", r"gatsby", r"remix", r"astro",
        r"express(?:\.js)?", r"fastify", r"nest\.?js|nestjs", r"koa",
        r"django", r"flask", r"fastapi", r"spring\s*boot|spring",
        r"rails|ruby on rails", r"laravel", r"symfony",
        r"\.net|asp\.net", r"blazor", r"flutter", r"react native", r"ionic", r"electron",
        r"three\.js", r"d3(?:\.js)?", r"chart\.js",
        r"tailwind(?:\s*css)?", r"bootstrap", r"material\s*ui|mui",
        r"redux", r"mobx", r"zustand", r"vuex", r"pinia", r"rxjs",
        r"jquery", r"backbone", r"ember", r"alpine\.js", r"htmx",
        r"hibernate", r"mybatis", r"micronaut", r"quarkus",
    ],
    "Cloud & DevOps": [
        r"\baws\b|amazon web services", r"\bazure\b|microsoft azure",
        r"\bgcp\b|google cloud(?:\s*platform)?",
        r"heroku", r"vercel", r"netlify", r"digitalocean", r"cloudflare",
        r"\bec2\b", r"\bs3\b", r"\blambda\b", r"\becs\b", r"\beks\b",
        r"\brds\b", r"dynamodb", r"\bsqs\b", r"\bsns\b", r"cloudfront",
        r"api gateway", r"cloudwatch", r"\biam\b", r"route\s*53",
        r"elastic beanstalk", r"cloudformation",
        r"azure\s*devops", r"azure\s*functions", r"cosmos\s*db",
        r"cloud\s*functions", r"cloud\s*run", r"bigquery", r"\bgke\b",
        r"docker", r"kubernetes|k8s", r"openshift", r"rancher", r"helm", r"istio",
        r"terraform", r"ansible", r"puppet", r"chef", r"pulumi",
        r"jenkins", r"github\s*actions", r"gitlab\s*ci", r"circleci",
        r"travis\s*ci", r"argo\s*cd", r"spinnaker",
        r"prometheus", r"grafana", r"datadog", r"new\s*relic", r"splunk",
        r"\belk\b", r"elasticsearch", r"logstash", r"kibana",
        r"nginx", r"apache", r"caddy", r"traefik", r"consul", r"vault",
    ],
    "Databases": [
        r"mysql", r"postgresql|postgres", r"sqlite", r"mariadb",
        r"oracle", r"sql\s*server|mssql",
        r"mongodb", r"couchdb", r"cassandra", r"redis", r"memcached",
        r"neo4j", r"cockroachdb", r"clickhouse", r"timescaledb", r"influxdb",
        r"firebase", r"supabase", r"prisma", r"sequelize",
        r"typeorm", r"mongoose", r"knex", r"drizzle", r"planetscale",
    ],
    "Data & AI/ML": [
        r"machine\s*learning", r"deep\s*learning", r"artificial\s*intelligence",
        r"neural\s*network", r"natural\s*language\s*processing|\bnlp\b",
        r"computer\s*vision", r"reinforcement\s*learning",
        r"generative\s*ai", r"large\s*language\s*model|\bllm\b",
        r"tensorflow", r"pytorch", r"keras", r"scikit-learn|sklearn",
        r"xgboost", r"lightgbm", r"catboost",
        r"pandas", r"numpy", r"scipy", r"matplotlib", r"seaborn", r"plotly",
        r"jupyter", r"opencv", r"spacy", r"nltk",
        r"hugging\s*face|huggingface", r"transformers", r"\bbert\b", r"\bgpt\b",
        r"langchain", r"llamaindex", r"\brag\b",
        r"pinecone", r"weaviate", r"chroma",
        r"\bspark\b|pyspark", r"hadoop", r"hive", r"kafka", r"airflow",
        r"\bdbt\b", r"snowflake", r"databricks", r"redshift",
        r"tableau", r"power\s*bi", r"looker", r"metabase",
        r"data\s*warehouse", r"\betl\b", r"data\s*pipeline",
        r"mlops", r"mlflow", r"kubeflow", r"sagemaker", r"vertex\s*ai",
    ],
    "Tools & Practices": [
        r"\bgit\b", r"github", r"gitlab", r"bitbucket",
        r"jira", r"confluence", r"trello", r"asana", r"notion", r"linear",
        r"figma", r"sketch", r"adobe\s*xd",
        r"vs\s*code|visual\s*studio", r"intellij", r"pycharm",
        r"postman", r"swagger|openapi",
        r"webpack", r"vite", r"rollup", r"parcel", r"esbuild", r"babel",
        r"\bjest\b", r"mocha", r"chai", r"cypress", r"playwright",
        r"selenium", r"puppeteer", r"vitest",
        r"eslint", r"prettier", r"sonarqube",
        r"\bnpm\b", r"\byarn\b", r"pnpm", r"\bpip\b", r"poetry",
        r"conda", r"cargo", r"maven", r"gradle", r"composer",
        r"storybook",
    ],
    "Soft Skills": [
        r"leadership", r"team\s*management", r"project\s*management",
        r"agile", r"scrum", r"kanban",
        r"communication", r"collaboration", r"problem\s*solving",
        r"critical\s*thinking", r"mentoring", r"coaching",
        r"stakeholder\s*management", r"cross-functional",
        r"presentation", r"public\s*speaking", r"technical\s*writing",
        r"time\s*management", r"strategic\s*planning", r"decision\s*making",
        r"conflict\s*resolution", r"negotiation", r"adaptability",
        r"creativity", r"innovation", r"design\s*thinking",
        r"remote\s*work", r"distributed\s*team",
    ],
    "Security & Architecture": [
        r"cybersecurity|information\s*security", r"penetration\s*testing|pentest",
        r"owasp", r"oauth", r"openid", r"saml", r"\bjwt\b",
        r"encryption", r"cryptography",
        r"\bgdpr\b", r"\bhipaa\b", r"pci-dss", r"iso\s*27001", r"compliance",
        r"microservices", r"monolith", r"serverless", r"event-driven",
        r"\bcqrs\b", r"event\s*sourcing",
        r"\brest\b|restful", r"\bsoap\b", r"\bgrpc\b", r"websocket",
        r"api\s*design", r"domain-driven\s*design|\bddd\b",
        r"clean\s*architecture", r"mvvm|mvc|mvp",
        r"ci/cd|continuous\s*integration|continuous\s*deployment",
        r"\btdd\b", r"\bbdd\b", r"pair\s*programming", r"code\s*review",
        r"design\s*patterns", r"system\s*design", r"distributed\s*systems",
        r"high\s*availability", r"load\s*balancing",
        r"caching", r"\bcdn\b", r"message\s*queue",
        r"solid\s*principles",
    ],
}


# ─── Proper capitalization map ───
SKILL_CAPITALIZATION = {
    "javascript": "JavaScript", "typescript": "TypeScript", "python": "Python",
    "java": "Java", "ruby": "Ruby", "go": "Go", "golang": "Go", "rust": "Rust",
    "swift": "Swift", "kotlin": "Kotlin", "php": "PHP", "scala": "Scala",
    "dart": "Dart", "perl": "Perl", "lua": "Lua", "haskell": "Haskell",
    "elixir": "Elixir", "julia": "Julia", "c": "C", "c++": "C++", "c#": "C#", "f#": "F#",
    "react": "React", "react.js": "React", "reactjs": "React",
    "angular": "Angular", "angularjs": "Angular",
    "vue": "Vue.js", "vue.js": "Vue.js", "vuejs": "Vue.js",
    "svelte": "Svelte", "next.js": "Next.js", "nextjs": "Next.js",
    "nuxt": "Nuxt.js", "nuxt.js": "Nuxt.js", "gatsby": "Gatsby",
    "express": "Express", "express.js": "Express",
    "nestjs": "NestJS", "nest.js": "NestJS",
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI",
    "spring": "Spring", "spring boot": "Spring Boot",
    "rails": "Rails", "ruby on rails": "Ruby on Rails",
    "laravel": "Laravel", "flutter": "Flutter", "react native": "React Native",
    "docker": "Docker", "kubernetes": "Kubernetes", "k8s": "Kubernetes",
    "terraform": "Terraform", "ansible": "Ansible",
    "aws": "AWS", "amazon web services": "AWS",
    "azure": "Azure", "microsoft azure": "Azure",
    "gcp": "GCP", "google cloud": "GCP", "google cloud platform": "GCP",
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "mysql": "MySQL", "mongodb": "MongoDB", "redis": "Redis",
    "sqlite": "SQLite", "cassandra": "Cassandra",
    "graphql": "GraphQL", "rest": "REST", "restful": "RESTful",
    "grpc": "gRPC", "websocket": "WebSocket",
    "git": "Git", "github": "GitHub", "gitlab": "GitLab",
    "jira": "Jira", "figma": "Figma", "notion": "Notion",
    "jest": "Jest", "mocha": "Mocha", "cypress": "Cypress",
    "playwright": "Playwright", "selenium": "Selenium",
    "webpack": "Webpack", "vite": "Vite",
    "tailwind": "Tailwind CSS", "tailwind css": "Tailwind CSS",
    "bootstrap": "Bootstrap", "redux": "Redux",
    "storybook": "Storybook", "eslint": "ESLint", "prettier": "Prettier",
    "npm": "npm", "yarn": "Yarn", "pnpm": "pnpm",
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "artificial intelligence": "AI", "nlp": "NLP",
    "natural language processing": "NLP", "computer vision": "Computer Vision",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "keras": "Keras",
    "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
    "pandas": "Pandas", "numpy": "NumPy", "scipy": "SciPy",
    "opencv": "OpenCV", "spacy": "spaCy",
    "spark": "Apache Spark", "pyspark": "PySpark",
    "kafka": "Kafka", "airflow": "Apache Airflow",
    "snowflake": "Snowflake", "databricks": "Databricks",
    "tableau": "Tableau", "power bi": "Power BI",
    "ci/cd": "CI/CD", "agile": "Agile", "scrum": "Scrum", "kanban": "Kanban",
    "microservices": "Microservices", "serverless": "Serverless",
    "tdd": "TDD", "bdd": "BDD",
    "html": "HTML", "css": "CSS", "sass": "SASS", "scss": "SCSS",
    "sql": "SQL", "nosql": "NoSQL", "json": "JSON", "yaml": "YAML", "xml": "XML",
    "oauth": "OAuth", "jwt": "JWT", "saml": "SAML",
    "prometheus": "Prometheus", "grafana": "Grafana", "datadog": "Datadog",
    "elasticsearch": "Elasticsearch", "kibana": "Kibana", "logstash": "Logstash",
    "nginx": "Nginx", "apache": "Apache",
    "ec2": "EC2", "s3": "S3", "lambda": "Lambda", "ecs": "ECS", "rds": "RDS",
    "cloudfront": "CloudFront", "cloudformation": "CloudFormation",
    "jenkins": "Jenkins", "github actions": "GitHub Actions",
    "gitlab ci": "GitLab CI", "circleci": "CircleCI",
    "d3": "D3.js", "d3.js": "D3.js", "three.js": "Three.js",
    "chart.js": "Chart.js",
    "leadership": "Leadership", "communication": "Communication",
    "collaboration": "Collaboration", "mentoring": "Mentoring",
    "problem solving": "Problem Solving", "project management": "Project Management",
    "ddd": "DDD", "domain-driven design": "DDD",
    "system design": "System Design", "distributed systems": "Distributed Systems",
    "design patterns": "Design Patterns", "clean architecture": "Clean Architecture",
    "etl": "ETL", "data pipeline": "Data Pipeline",
    "llm": "LLM", "rag": "RAG", "langchain": "LangChain",
    "hugging face": "Hugging Face", "huggingface": "Hugging Face",
    "sagemaker": "SageMaker", "owasp": "OWASP", "gdpr": "GDPR", "hipaa": "HIPAA",
    "remote work": "Remote Work", "pair programming": "Pair Programming",
    "code review": "Code Review", "firebase": "Firebase", "supabase": "Supabase",
    "prisma": "Prisma", "helm": "Helm", "istio": "Istio",
    "continuous integration": "CI/CD", "continuous deployment": "CI/CD",
}


# ═══════════════════════════════════════════════════════════════
#  SAMPLE DATA
# ═══════════════════════════════════════════════════════════════

SAMPLE_RESUME = """SARAH CHEN
Senior Full Stack Engineer | San Francisco, CA
Email: sarah.chen@email.com | LinkedIn: linkedin.com/in/sarahchen | GitHub: github.com/sarahchen

PROFESSIONAL SUMMARY
Innovative Senior Full Stack Engineer with 6+ years of experience building scalable web applications. Expert in React, TypeScript, Node.js, and cloud technologies (AWS). Proven track record of leading engineering teams, improving system performance by 40%, and delivering products used by 2M+ users. Passionate about clean code, mentoring junior developers, and adopting modern development practices.

TECHNICAL SKILLS
Languages: JavaScript, TypeScript, Python, SQL, HTML, CSS, GraphQL
Frontend: React, Next.js, Redux, Tailwind CSS, Storybook, Cypress, Jest
Backend: Node.js, Express, NestJS, FastAPI, PostgreSQL, Redis, MongoDB
Cloud & DevOps: AWS (EC2, S3, Lambda, ECS, RDS, CloudFront), Docker, Kubernetes, Terraform, GitHub Actions, CI/CD
Tools: Git, Jira, Figma, Datadog, Prometheus, Grafana

PROFESSIONAL EXPERIENCE
Senior Full Stack Engineer — Acme Tech Inc. (2021 – Present)
• Led a team of 8 engineers to design and build a microservices platform serving 2M+ daily active users
• Architected a React + TypeScript frontend with server-side rendering (Next.js) that improved page load speed by 55%
• Designed RESTful APIs and GraphQL endpoints using NestJS, handling 10K+ requests per second
• Implemented CI/CD pipelines with GitHub Actions and Docker, reducing deployment time from 2 hours to 15 minutes
• Migrated legacy monolith to AWS-based microservices with Kubernetes, achieving 99.99% uptime
• Mentored 4 junior developers through pair programming and code reviews

Full Stack Developer — StartupXYZ (2019 – 2021)
• Built a real-time collaboration platform using React, WebSocket, and Node.js
• Developed automated testing suites with Jest and Cypress, achieving 92% code coverage
• Optimized PostgreSQL queries, reducing database response time by 60%
• Collaborated with UX designers using Figma to implement pixel-perfect responsive interfaces

Software Engineer — DataFlow Solutions (2017 – 2019)
• Developed data visualization dashboards using D3.js and React
• Built ETL pipelines using Python and Apache Airflow
• Managed deployments on AWS EC2 and S3 with automated scripts

EDUCATION
B.S. Computer Science — University of California, Berkeley (2017)
GPA: 3.8/4.0, Dean's List

CERTIFICATIONS
• AWS Certified Solutions Architect – Associate
• Google Cloud Professional Cloud Developer

PROJECTS
• Open-source React component library (500+ GitHub stars)
• Machine learning-powered recommendation engine using Python and TensorFlow"""

SAMPLE_JD = """Senior Full Stack Engineer — TechCorp Inc.

About the Role:
We are seeking a talented Senior Full Stack Engineer to join our growing engineering team. You will be responsible for designing, building, and maintaining scalable web applications that serve millions of users worldwide.

Requirements:
• 5+ years of professional experience in full stack web development
• Strong proficiency in React, TypeScript, and modern JavaScript (ES6+)
• Experience with Node.js backend frameworks (Express, NestJS, or similar)
• Solid understanding of RESTful APIs, GraphQL, and microservices architecture
• Experience with cloud platforms (AWS preferred: EC2, Lambda, S3, RDS, ECS)
• Proficiency in SQL databases (PostgreSQL preferred) and NoSQL (MongoDB, Redis)
• Experience with containerization (Docker) and orchestration (Kubernetes)
• Familiarity with CI/CD pipelines and infrastructure as code (Terraform)
• Strong understanding of Git, code review practices, and agile methodologies
• Excellent communication and collaboration skills

Nice to Have:
• Experience with Next.js or server-side rendering
• Knowledge of machine learning or data engineering concepts
• Contributions to open-source projects
• Experience with monitoring tools (Datadog, Prometheus, Grafana)
• AWS or GCP cloud certifications
• Experience mentoring junior engineers

Education:
• Bachelor's degree in Computer Science, Engineering, or related field

We offer competitive salary, equity, comprehensive benefits, and a collaborative remote-first culture."""


# ═══════════════════════════════════════════════════════════════
#  CORE ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════

def extract_skills(text: str) -> list[str]:
    """Extract skills from text using regex against the skill database."""
    found = set()
    text_lower = text.lower()

    for category, patterns in SKILL_DATABASE.items():
        for pattern in patterns:
            try:
                regex = re.compile(
                    rf"(?:^|[\s,;|•\-/(])"
                    rf"({pattern})"
                    rf"(?=[\s,;|•\-/).$]|$)",
                    re.IGNORECASE | re.MULTILINE
                )
                for match in regex.finditer(text_lower):
                    raw = match.group(1).strip()
                    normalized = normalize_skill(raw)
                    if len(normalized) >= 1:
                        found.add(normalized)
            except re.error:
                pass

    return sorted(found)


def normalize_skill(name: str) -> str:
    """Normalize skill name to proper capitalization."""
    lower = name.lower().strip()
    if lower in SKILL_CAPITALIZATION:
        return SKILL_CAPITALIZATION[lower]
    # Default: title case
    return name.strip().title()


def extract_keywords(jd_text: str) -> list[str]:
    """Extract important keywords and phrases from a job description."""
    keywords = set()
    jd_lower = jd_text.lower()

    # Important phrases
    important_phrases = [
        "full stack", "front end", "frontend", "back end", "backend",
        "server-side rendering", "ssr", "single page application", "spa",
        "responsive design", "mobile first", "cross-browser",
        "unit testing", "integration testing", "end-to-end", "e2e",
        "version control", "code review", "pair programming",
        "open source", "open-source", "scalable", "performance",
        "security", "authentication", "authorization",
        "data structures", "algorithms", "object-oriented",
        "functional programming", "real-time", "high availability",
        "fault tolerant", "load balancing", "caching", "optimization",
        "monitoring", "logging", "debugging", "troubleshooting",
        "infrastructure as code", "containerization", "orchestration",
        "api design", "database design", "schema design",
        "cloud-native", "cloud native", "stakeholder", "cross-functional",
    ]

    for phrase in important_phrases:
        if phrase in jd_lower:
            keywords.add(phrase.title())

    # Action verbs
    action_verbs = [
        "develop", "design", "implement", "build", "create", "maintain",
        "optimize", "deploy", "test", "debug", "collaborate", "lead",
        "mentor", "manage", "architect", "scale", "automate", "integrate",
        "analyze", "deliver", "contribute", "review",
    ]

    for verb in action_verbs:
        regex = re.compile(rf"\b{verb}(?:e[ds]?|ing|ed)?\b", re.IGNORECASE)
        if regex.search(jd_text):
            keywords.add(verb.capitalize())

    # Years of experience
    years_match = re.search(r"(\d+)\+?\s*years?\s*(?:of\s+)?experience", jd_text, re.IGNORECASE)
    if years_match:
        keywords.add(f"{years_match.group(1)}+ Years Experience")

    # Education
    if re.search(r"bachelor", jd_text, re.IGNORECASE):
        keywords.add("Bachelor's Degree")
    if re.search(r"master", jd_text, re.IGNORECASE):
        keywords.add("Master's Degree")
    if re.search(r"certif", jd_text, re.IGNORECASE):
        keywords.add("Certification")

    return sorted(keywords)


def analyze_structure(resume_text: str) -> int:
    """Analyze resume structure and return a score 0-100."""
    score = 0
    lines = [l for l in resume_text.split("\n") if l.strip()]

    # Contact info
    if re.search(r"[\w.\-]+@[\w.\-]+\.\w+", resume_text):
        score += 8
    if re.search(r"linkedin\.com", resume_text, re.IGNORECASE):
        score += 5
    if re.search(r"github\.com", resume_text, re.IGNORECASE):
        score += 5
    if re.search(r"\+?\d[\d\s\-()]{8,}", resume_text):
        score += 4

    # Key sections
    section_checks = {
        "experience": 15, "education": 10, "skills": 12,
        "summary": 8, "projects": 6, "certifications": 5,
    }
    for section, pts in section_checks.items():
        regex = re.compile(
            rf"(?:^|\n)\s*(?:{section}|professional {section}|technical {section}|work {section}|core {section})",
            re.IGNORECASE
        )
        if regex.search(resume_text):
            score += pts

    # Word count
    word_count = len(resume_text.split())
    if 150 <= word_count <= 1200:
        score += 10
    elif word_count >= 100:
        score += 5

    # Bullet points
    bullet_lines = [l for l in lines if re.match(r"^\s*[•\-\*▸▹➤]", l)]
    if len(bullet_lines) >= 5:
        score += 8
    elif len(bullet_lines) >= 2:
        score += 4

    # Quantifiable achievements
    numbers = re.findall(r"\d+[%+KMB]?", resume_text)
    if len(numbers) >= 5:
        score += 7
    elif len(numbers) >= 2:
        score += 4

    # Action verbs at start of bullets
    action_starts = [
        l for l in bullet_lines
        if re.match(
            r"^\s*[•\-\*▸▹➤]\s*(Led|Built|Designed|Developed|Implemented|Created|Managed|"
            r"Improved|Optimized|Delivered|Architected|Deployed|Reduced|Increased|Automated|"
            r"Mentored|Collaborated|Migrated|Scaled)",
            l, re.IGNORECASE
        )
    ]
    if len(action_starts) >= 3:
        score += 7
    elif len(action_starts) >= 1:
        score += 3

    return min(score, 100)


def generate_suggestions(resume_text, all_skills, matched, missing, struct_score, overall, kw_pct):
    """Generate actionable improvement suggestions."""
    suggestions = []

    # Missing skills
    if 0 < len(missing) <= 5:
        suggestions.append((
            "warn",
            f"Add these {len(missing)} missing skills to your resume: {', '.join(missing[:5])}. "
            f"These are explicitly mentioned in the job description."
        ))
    elif len(missing) > 5:
        suggestions.append((
            "warn",
            f"You're missing {len(missing)} key skills. Focus on adding: {', '.join(missing[:5])}."
        ))

    # Skill match praise
    if len(matched) > 5:
        suggestions.append((
            "good",
            f"Strong skill alignment! {len(matched)} of your skills match the job requirements."
        ))

    # Structure
    if struct_score < 40:
        suggestions.append((
            "warn",
            "Your resume structure needs improvement. Add clear sections: Experience, Education, Skills, Summary."
        ))

    # Contact info
    if not re.search(r"linkedin\.com", resume_text, re.IGNORECASE):
        suggestions.append((
            "info",
            "Consider adding your LinkedIn profile URL. Most recruiters check LinkedIn."
        ))
    if not re.search(r"github\.com", resume_text, re.IGNORECASE):
        suggestions.append((
            "info",
            "Adding a GitHub profile can showcase your coding activity and open-source contributions."
        ))

    # Quantifiable achievements
    numbers = re.findall(r"\d+[%+KMB]?", resume_text)
    if len(numbers) < 4:
        suggestions.append((
            "warn",
            'Add more quantifiable achievements (e.g., "improved performance by 40%", "served 2M+ users").'
        ))
    else:
        suggestions.append((
            "good",
            "Great use of quantifiable metrics! Your achievements are backed by concrete numbers."
        ))

    # Bullet points
    bullet_lines = [l for l in resume_text.split("\n") if re.match(r"^\s*[•\-\*]", l)]
    if len(bullet_lines) < 5:
        suggestions.append((
            "info",
            "Use more bullet points starting with action verbs (Led, Built, Designed, Optimized)."
        ))

    # Length
    word_count = len(resume_text.split())
    if word_count < 150:
        suggestions.append((
            "warn",
            f"Your resume seems short ({word_count} words). Aim for 300-700 words."
        ))
    elif word_count > 1200:
        suggestions.append((
            "info",
            f"Your resume is quite long ({word_count} words). Consider trimming to 600-800 words."
        ))

    # Certifications
    if re.search(r"certif", resume_text, re.IGNORECASE):
        suggestions.append((
            "good",
            "Including certifications strengthens your credibility. Make sure they're relevant."
        ))

    # Overall
    if overall >= 80:
        suggestions.append((
            "good",
            "Excellent overall match! Your resume is well-tailored for this position."
        ))
    elif overall >= 60:
        suggestions.append((
            "info",
            "Good match overall. Addressing missing keywords could push your score higher."
        ))

    return suggestions


def analyze_resume(resume_text: str, jd_text: str) -> dict:
    """Run the full analysis pipeline and return results."""
    resume_lower = resume_text.lower()

    # 1. Extract skills
    extracted_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    jd_keywords = extract_keywords(jd_text)

    # 2. Compute matches
    resume_skills_lower = {s.lower() for s in extracted_skills}
    matched_skills = []
    missing_skills = []
    extra_skills = []

    for skill in jd_skills:
        if skill.lower() in resume_skills_lower or skill.lower() in resume_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    jd_skills_lower = {s.lower() for s in jd_skills}
    for skill in extracted_skills:
        if skill.lower() not in jd_skills_lower:
            extra_skills.append(skill)

    # 3. Keyword matching
    keyword_results = []
    for kw in jd_keywords:
        found = kw.lower() in resume_lower
        keyword_results.append({"keyword": kw, "found": found})

    # 4. Structure score
    structure_score = analyze_structure(resume_text)

    # 5. Compute scores
    skill_match_pct = round((len(matched_skills) / len(jd_skills) * 100)) if jd_skills else 50
    kw_found = sum(1 for k in keyword_results if k["found"])
    kw_total = len(keyword_results)
    keyword_match_pct = round((kw_found / kw_total * 100)) if kw_total else 50

    overall_score = round(
        skill_match_pct * 0.45 +
        keyword_match_pct * 0.30 +
        structure_score * 0.25
    )

    # 6. Suggestions
    suggestions = generate_suggestions(
        resume_text, extracted_skills, matched_skills,
        missing_skills, structure_score, overall_score, keyword_match_pct
    )

    return {
        "overall_score": overall_score,
        "skill_match_pct": skill_match_pct,
        "keyword_match_pct": keyword_match_pct,
        "structure_score": structure_score,
        "extracted_skills": extracted_skills,
        "matched_skills": matched_skills,
        "extra_skills": extra_skills,
        "missing_skills": missing_skills,
        "keyword_results": keyword_results,
        "suggestions": suggestions,
    }


# ═══════════════════════════════════════════════════════════════
#  TERMINAL UI — Pretty Output
# ═══════════════════════════════════════════════════════════════

def print_banner():
    """Print the application banner."""
    banner = f"""
{c("╔══════════════════════════════════════════════════════════════╗", Colors.B_CYAN)}
{c("║", Colors.B_CYAN)}  {c("🔍 AI-BASED RESUME ANALYZER", Colors.BOLD, Colors.B_WHITE)}                                {c("║", Colors.B_CYAN)}
{c("║", Colors.B_CYAN)}  {c("Skill Extraction • Keyword Matching • Resume Scoring", Colors.DIM)}       {c("║", Colors.B_CYAN)}
{c("╚══════════════════════════════════════════════════════════════╝", Colors.B_CYAN)}
"""
    print(banner)


def print_section(title: str, icon: str = "─"):
    """Print a section header."""
    print(f"\n{c(f'  {icon} {title}', Colors.BOLD, Colors.B_WHITE)}")
    print(f"  {c('─' * 56, Colors.DIM)}")


def progress_bar(value: int, width: int = 40, fill_color=Colors.B_GREEN) -> str:
    """Create a colored progress bar string."""
    filled = round(width * value / 100)
    empty = width - filled
    bar = fill_color + "█" * filled + Colors.DIM + "░" * empty + Colors.RESET
    return f"  [{bar}] {c(f'{value}%', Colors.BOLD, fill_color)}"


def score_color(score: int) -> str:
    """Return appropriate color for a score value."""
    if score >= 80:
        return Colors.B_GREEN
    elif score >= 60:
        return Colors.B_CYAN
    elif score >= 40:
        return Colors.B_YELLOW
    else:
        return Colors.B_RED


def print_score_dial(score: int):
    """Print a large score display."""
    clr = score_color(score)
    if score >= 80:
        verdict = "🎯 EXCELLENT MATCH"
        desc = "Your resume is highly aligned with this role!"
    elif score >= 60:
        verdict = "✅ GOOD MATCH"
        desc = "A few improvements will make it even stronger."
    elif score >= 40:
        verdict = "⚠️  FAIR MATCH"
        desc = "Significant gaps exist. Review suggestions below."
    else:
        verdict = "❌ POOR MATCH"
        desc = "Major revisions needed to align with this role."

    print(f"""
  {c("┌────────────────────────────────────────────┐", Colors.DIM)}
  {c("│", Colors.DIM)}         {c("OVERALL RESUME SCORE", Colors.BOLD)}              {c("│", Colors.DIM)}
  {c("│", Colors.DIM)}                                            {c("│", Colors.DIM)}
  {c("│", Colors.DIM)}              {c(f"  {score:>3} / 100  ", Colors.BOLD, clr)}              {c("│", Colors.DIM)}
  {c("│", Colors.DIM)}                                            {c("│", Colors.DIM)}
  {c("│", Colors.DIM)}      {c(f"{verdict:^36}", Colors.BOLD, clr)}  {c("│", Colors.DIM)}
  {c("│", Colors.DIM)}  {c(f"{desc:^42}", Colors.DIM)}  {c("│", Colors.DIM)}
  {c("└────────────────────────────────────────────┘", Colors.DIM)}
""")


def print_results(results: dict):
    """Render analysis results to the terminal."""

    # ── Overall Score ──
    print_score_dial(results["overall_score"])

    # ── Sub-Scores ──
    print_section("SCORE BREAKDOWN", "📊")
    print(f"  {c('Skill Match:', Colors.BOLD)}     ", end="")
    print(progress_bar(results["skill_match_pct"], 30, score_color(results["skill_match_pct"])))
    print(f"  {c('Keyword Match:', Colors.BOLD)}   ", end="")
    print(progress_bar(results["keyword_match_pct"], 30, score_color(results["keyword_match_pct"])))
    print(f"  {c('Structure:', Colors.BOLD)}        ", end="")
    print(progress_bar(results["structure_score"], 30, score_color(results["structure_score"])))

    # ── Extracted Skills ──
    print_section(f"EXTRACTED SKILLS ({len(results['extracted_skills'])} found)", "⭐")
    matched_lower = {s.lower() for s in results["matched_skills"]}

    matched_display = []
    extra_display = []
    for s in results["extracted_skills"]:
        if s.lower() in matched_lower:
            matched_display.append(c(f"  ✓ {s}", Colors.B_GREEN))
        else:
            extra_display.append(c(f"  ◦ {s}", Colors.B_BLUE))

    if matched_display:
        print(c("  Matched with JD:", Colors.DIM))
        # Print in columns
        _print_columns(matched_display, 2)

    if extra_display:
        print(c("\n  Additional skills:", Colors.DIM))
        _print_columns(extra_display, 2)

    # ── Keyword Matching ──
    kw_results = results["keyword_results"]
    kw_found = [k for k in kw_results if k["found"]]
    kw_missing = [k for k in kw_results if not k["found"]]

    print_section(f"KEYWORD MATCHING ({len(kw_found)}/{len(kw_results)} found)", "🔍")

    if kw_found:
        found_strs = [c(f"  ● {k['keyword']}", Colors.B_GREEN) for k in kw_found]
        _print_columns(found_strs, 2)

    if kw_missing:
        print(c(f"\n  Missing ({len(kw_missing)}):", Colors.B_YELLOW))
        missing_strs = [c(f"  ○ {k['keyword']}", Colors.B_YELLOW) for k in kw_missing]
        _print_columns(missing_strs, 2)

    # ── Missing Skills ──
    if results["missing_skills"]:
        print_section(f"MISSING SKILLS ({len(results['missing_skills'])})", "⚠️ ")
        print(c("  Add these to improve your match score:", Colors.DIM))
        for s in results["missing_skills"]:
            print(c(f"    ✗ {s}", Colors.B_YELLOW))
    else:
        print_section("MISSING SKILLS", "✅")
        print(c("  🎉 No missing skills — great job!", Colors.B_GREEN))

    # ── Suggestions ──
    print_section("IMPROVEMENT TIPS", "💡")
    for stype, text in results["suggestions"]:
        if stype == "good":
            icon = c("  ✓", Colors.B_GREEN)
        elif stype == "warn":
            icon = c("  !", Colors.B_YELLOW)
        else:
            icon = c("  ℹ", Colors.B_CYAN)

        wrapped = textwrap.fill(text, width=54, initial_indent="    ", subsequent_indent="    ")
        print(f"{icon}")
        print(f"{c(wrapped, Colors.DIM)}")
        print()


def _print_columns(items: list[str], cols: int):
    """Print items in columns."""
    # Approximate: strip ANSI for width calculation
    for i in range(0, len(items), cols):
        row = items[i:i + cols]
        # Pad each item
        line_parts = []
        for item in row:
            # Pad to ~30 visible chars
            line_parts.append(item.ljust(55))
        print("".join(line_parts))


def loading_animation(message: str, duration: float = 1.5):
    """Show a simple loading animation."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        print(f"\r  {c(frame, Colors.B_CYAN)} {c(message, Colors.DIM)}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r  {c('✓', Colors.B_GREEN)} {c(message + ' Done!', Colors.DIM)}    ")


# ═══════════════════════════════════════════════════════════════
#  INPUT HANDLING
# ═══════════════════════════════════════════════════════════════

def get_multiline_input(prompt: str) -> str:
    """Get multi-line text input from the user."""
    print(c(f"\n  {prompt}", Colors.BOLD, Colors.B_WHITE))
    print(c("  (Paste your text, then type 'END' on a new line to finish)\n", Colors.DIM))
    lines = []
    while True:
        try:
            line = input(c("  │ ", Colors.DIM))
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def _install_package(package_name: str, import_name: str = None) -> bool:
    """Prompt user to install a missing package, return True if installed."""
    if import_name is None:
        import_name = package_name
    print(c(f"\n  ⚠ The '{package_name}' library is required to read this file format.", Colors.B_YELLOW))
    answer = input(c(f"  → Install it now? (y/n): ", Colors.B_CYAN)).strip().lower()
    if answer in ("y", "yes"):
        try:
            print(c(f"  ⏳ Installing {package_name}...", Colors.DIM))
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            print(c(f"  ✓ {package_name} installed successfully!\n", Colors.B_GREEN))
            return True
        except subprocess.CalledProcessError:
            print(c(f"  ✗ Failed to install {package_name}. Install manually: pip install {package_name}", Colors.B_RED))
            return False
    else:
        print(c(f"  ✗ Cannot read this file without '{package_name}'. Exiting.", Colors.B_RED))
        return False


def _read_pdf(filepath: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        import PyPDF2
    except ImportError:
        if not _install_package("PyPDF2"):
            sys.exit(1)
        import PyPDF2

    try:
        text_parts = []
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        text = "\n".join(text_parts)
        if not text.strip():
            print(c("  ⚠ PDF appears to be image-based (scanned). Text extraction returned empty.", Colors.B_YELLOW))
            print(c("    Tip: Use a text-based PDF or paste your resume text manually.", Colors.DIM))
            sys.exit(1)
        return text
    except Exception as e:
        print(c(f"  ✗ Error reading PDF: {e}", Colors.B_RED))
        sys.exit(1)


def _read_docx(filepath: str) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        import docx
    except ImportError:
        if not _install_package("python-docx", "docx"):
            sys.exit(1)
        import docx

    try:
        doc = docx.Document(filepath)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        text = "\n".join(paragraphs)
        if not text.strip():
            print(c("  ⚠ DOCX file appears to be empty or contains only images.", Colors.B_YELLOW))
            sys.exit(1)
        return text
    except Exception as e:
        print(c(f"  ✗ Error reading DOCX: {e}", Colors.B_RED))
        sys.exit(1)


def _read_txt(filepath: str) -> str:
    """Read plain text file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding
        with open(filepath, "r", encoding="latin-1") as f:
            return f.read()


def read_file(filepath: str) -> str:
    """Read text content from a file (.txt, .md, .pdf, .docx)."""
    if not os.path.exists(filepath):
        print(c(f"\n  ✗ File not found: {filepath}", Colors.B_RED))
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()
    supported = {".txt", ".text", ".md", ".pdf", ".docx", ".doc"}

    if ext not in supported:
        print(c(f"\n  ✗ Unsupported file format: '{ext}'", Colors.B_RED))
        print(c(f"    Supported formats: {', '.join(sorted(supported))}", Colors.DIM))
        sys.exit(1)

    try:
        if ext == ".pdf":
            return _read_pdf(filepath)
        elif ext in (".docx", ".doc"):
            return _read_docx(filepath)
        else:
            return _read_txt(filepath)
    except SystemExit:
        raise
    except Exception as e:
        print(c(f"\n  ✗ Error reading file: {e}", Colors.B_RED))
        sys.exit(1)


def open_file_dialog() -> str:
    """Open a native file picker dialog and return the selected file path."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        # Create and hide the root window
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)  # Bring dialog to front

        filepath = filedialog.askopenfilename(
            title="Select your Resume file",
            filetypes=[
                ("All Supported", "*.pdf *.docx *.doc *.txt *.md"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx *.doc"),
                ("Text Files", "*.txt *.md"),
                ("All Files", "*.*"),
            ]
        )

        root.destroy()

        if not filepath:
            print(c("\n  ✗ No file selected.", Colors.B_YELLOW))
            return None

        return filepath

    except ImportError:
        print(c("\n  ⚠ tkinter not available. Please enter the file path manually.", Colors.B_YELLOW))
        return None
    except Exception as e:
        print(c(f"\n  ⚠ Could not open file dialog: {e}", Colors.B_YELLOW))
        print(c("    Falling back to manual path entry.", Colors.DIM))
        return None


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    Colors.enable()
    print_banner()

    # Parse command-line arguments
    use_sample = "--sample" in sys.argv
    resume_file = None

    for i, arg in enumerate(sys.argv):
        if arg == "--resume" and i + 1 < len(sys.argv):
            resume_file = sys.argv[i + 1]

    # ─── Get Resume Text ───
    if use_sample:
        print(c("  📝 Using sample resume and job description...\n", Colors.B_CYAN))
        resume_text = SAMPLE_RESUME
        jd_text = SAMPLE_JD
    elif resume_file:
        print(c(f"  📂 Loading resume from: {resume_file}", Colors.B_CYAN))
        resume_text = read_file(resume_file)
        print(c(f"  ✓ Loaded {len(resume_text)} characters\n", Colors.B_GREEN))
        jd_text = get_multiline_input("📋 Paste the Job Description:")
    else:
        # Interactive mode
        print(c("  Choose an option:", Colors.BOLD))
        print(c("    [1] Paste resume & job description manually", Colors.B_WHITE))
        print(c("    [2] Use sample data (demo)", Colors.B_WHITE))
        print(c("    [3] Enter resume file path", Colors.B_WHITE))
        print(c("    [4] 📎 Browse & attach resume file (PDF/DOCX/TXT)\n", Colors.B_WHITE))

        choice = input(c("  → Your choice (1/2/3/4): ", Colors.B_CYAN)).strip()

        if choice == "2":
            resume_text = SAMPLE_RESUME
            jd_text = SAMPLE_JD
            print(c("\n  📝 Loaded sample data!\n", Colors.B_GREEN))
        elif choice == "3":
            filepath = input(c("  📂 Enter resume file path: ", Colors.B_CYAN)).strip().strip('"')
            resume_text = read_file(filepath)
            print(c(f"  ✓ Loaded {len(resume_text)} characters\n", Colors.B_GREEN))
            jd_text = get_multiline_input("📋 Paste the Job Description:")
        elif choice == "4":
            print(c("\n  📎 Opening file browser...", Colors.B_CYAN))
            filepath = open_file_dialog()
            if filepath is None:
                # Fallback to manual path entry
                filepath = input(c("  📂 Enter resume file path instead: ", Colors.B_CYAN)).strip().strip('"')
            filename = os.path.basename(filepath)
            ext = os.path.splitext(filename)[1].lower()
            print(c(f"  📄 Selected: {filename}  ({ext} file)", Colors.B_WHITE))
            resume_text = read_file(filepath)
            word_count = len(resume_text.split())
            print(c(f"  ✓ Loaded successfully — {len(resume_text)} characters, ~{word_count} words\n", Colors.B_GREEN))
            jd_text = get_multiline_input("📋 Paste the Job Description:")
        else:
            resume_text = get_multiline_input("📄 Paste your Resume:")
            jd_text = get_multiline_input("📋 Paste the Job Description:")

    # ─── Validate Input ───
    if len(resume_text.strip()) < 20:
        print(c("\n  ✗ Resume text is too short. Please provide a valid resume.", Colors.B_RED))
        sys.exit(1)

    if len(jd_text.strip()) < 20:
        print(c("\n  ✗ Job description is too short. Please provide a valid JD.", Colors.B_RED))
        sys.exit(1)

    # ─── Run Analysis ───
    print()
    loading_animation("Parsing resume text...", 0.6)
    loading_animation("Extracting skills...", 0.5)
    loading_animation("Matching keywords...", 0.5)
    loading_animation("Evaluating structure...", 0.4)
    loading_animation("Computing score...", 0.3)

    results = analyze_resume(resume_text, jd_text)

    loading_animation("Generating insights...", 0.4)

    # ─── Display Results ───
    print_results(results)

    # ─── Summary ───
    print(f"\n  {c('═' * 56, Colors.DIM)}")
    print(c("  Analysis complete! All processing was done locally.", Colors.DIM))
    print(c("  Your data never left this machine. ✨\n", Colors.DIM))


if __name__ == "__main__":
    main()
