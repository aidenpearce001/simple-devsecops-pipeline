# Simple DevSecOps Pipeline

A comprehensive DevSecOps CI/CD pipeline demonstrating modern security practices, automated testing, and quality assurance for a FastAPI application.

## 🎯 Overview

This project implements a complete DevSecOps pipeline that runs comprehensive security and quality checks on every pull request from `develop` to `main`. The pipeline integrates multiple security tools and provides detailed feedback directly in GitHub pull requests.

## 🏗️ Architecture & Code Structure

### Project Layout

```
simple-devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Main DevSecOps pipeline
├── .zap/
│   └── rules.tsv               # OWASP ZAP scanning rules
├── src/
│   ├── __init__.py             # Python package initialization
│   └── main.py                 # FastAPI application with security headers
├── tests/
│   └── test_main.py            # Unit tests for FastAPI endpoints
├── Dockerfile                  # Multi-stage Docker build with UV
├── pyproject.toml              # Python project configuration (UV)
├── uv.lock                     # Locked dependencies (UV)
└── README.md                   # This documentation
```

### Code Architecture

#### FastAPI Application (`src/main.py`)

**Design Pattern**: Layered Architecture with Security-First Approach

The application implements comprehensive security headers middleware that addresses common web vulnerabilities:

- **Security Headers Middleware**: Implements OWASP-recommended security headers
- **Pydantic Models**: Type-safe request/response validation  
- **Error Handling**: Structured HTTP exception handling
- **API Design**: RESTful endpoint design with proper HTTP status codes

**Security Headers Implemented**:
- `X-Content-Type-Options: nosniff` - Prevents MIME confusion attacks
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` - Browser XSS protection
- `Strict-Transport-Security` - Forces HTTPS
- `Cross-Origin-*` policies - Mitigates Spectre-style attacks
- `Cache-Control` - Prevents sensitive data caching

#### Testing Strategy (`tests/test_main.py`)

**Pattern**: Comprehensive Test Coverage with Edge Cases

**Test Coverage**:
- ✅ Root endpoint functionality
- ✅ Addition endpoint with various number types (integers, floats, negatives)
- ✅ Input validation and error responses
- ✅ FastAPI automatic validation (422 responses)

## 🚀 DevSecOps Pipeline Flow

### Trigger Conditions

**Strict Branch Policy**: Only `develop` → `main` pull requests

```yaml
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
```

### Pipeline Jobs

#### Job 0: 🔍 **PR Validation** (`validate-pr`)

**Purpose**: Enforces Git Flow and branch policies

**What it does**:
1. Validates source branch is `develop`
2. Validates target branch is `main`
3. Comments on invalid PRs with clear guidance
4. Fails pipeline if branch policy violated

**Security Benefit**: Ensures only release-ready code from develop branch

#### Job 1: 🎨 **Code Formatting & Linting** (`formatting-and-linting`)

**Purpose**: Code quality and style consistency

**Tools Used**:
- **Black**: Python code formatter (PEP 8 compliance)
- **isort**: Import statement organization
- **Ruff**: Fast Python linter (replaces flake8, pylint)

**What it does**:
1. Formats code according to Python standards
2. Organizes imports alphabetically and by type
3. Checks for code smells and potential issues
4. Ensures consistent code style across the project

**Benefits**: Improved readability, maintainability, and team collaboration

#### Job 2: 🧪 **Unit Testing** (`run-pytest`)

**Purpose**: Functional validation and code coverage

**Tools Used**:
- **pytest**: Testing framework
- **coverage**: Code coverage measurement
- **httpx**: HTTP client for testing FastAPI

**What it does**:
1. Runs comprehensive unit test suite
2. Measures code coverage percentage
3. Generates coverage reports (XML format)
4. Posts results as PR comments

**PR Comment Example**:
```markdown
## 🧪 Test Results
✅ Tests passed
📊 **Coverage**: 85.2%
```

#### Job 3: 🔒 **Static Application Security Testing** (`run-bandit`)

**Purpose**: Static code analysis for security vulnerabilities

**Tool Used**: **Bandit** - Python security linter

**What it does**:
1. Scans Python code for security anti-patterns
2. Identifies potential vulnerabilities:
   - SQL injection risks
   - Hard-coded passwords
   - Insecure random generators
   - Shell injection vulnerabilities
   - Import of insecure modules

**Security Categories**:
- **High**: Critical security issues requiring immediate attention
- **Medium**: Important security concerns  
- **Low**: Minor security improvements

**PR Comment Example**:
```markdown
## 🔒 Security Scan Results (Bandit)
✅ No security issues found
```

#### Job 4: 📦 **Software Composition Analysis** (`run-safety`)

**Purpose**: Third-party dependency vulnerability scanning

**Tool Used**: **Safety** - Python dependency vulnerability checker

**What it does**:
1. Generates current dependency list from UV environment
2. Checks dependencies against known vulnerability databases
3. Identifies vulnerable packages and versions
4. Provides remediation guidance

**Database Sources**:
- National Vulnerability Database (NVD)
- PyPI security advisories
- GitHub security advisories

**PR Comment Example**:
```markdown
## 📦 Dependency Security Check (Safety)
⚠️ 2 vulnerable dependencies found
🚨 **Vulnerabilities**: 1 High, 1 Medium, 0 Low
```

#### Job 5: 📊 **Advanced Coverage Reporting** (`coverage`)

**Purpose**: Detailed coverage analysis with trend tracking

**Tool Used**: **insightsengineering/coverage-action**

**What it does**:
1. Downloads coverage data from test job
2. Generates detailed coverage reports
3. Compares coverage with main branch
4. Posts coverage diff in PR comments
5. Enforces minimum coverage thresholds (80%)

**Features**:
- Coverage percentage calculation
- Line-by-line coverage diff
- Historical coverage comparison
- Coverage trend analysis

#### Job 6: 🔍 **Dynamic Application Security Testing** (`dast-zap`)

**Purpose**: Runtime security testing of the running application

**Tool Used**: **OWASP ZAP** (Zed Attack Proxy)

**What it does**:
1. Starts FastAPI application locally
2. Waits for application readiness
3. Runs comprehensive security scans:
   - **Authentication testing**
   - **Authorization bypass attempts** 
   - **Input validation testing**
   - **XSS vulnerability detection**
   - **SQL injection testing**
   - **CSRF protection validation**
   - **Security header analysis**
   - **Information disclosure checks**

**Scan Types**:
- **Baseline Scan**: Fast, essential security checks
- **Active Scan**: Deeper penetration testing (optional)

**Custom Rules** (`.zap/rules.tsv`):
```tsv
10001  OFF  # Backup File Disclosure (too noisy for CI)
10003  OFF  # Vulnerable Libraries (handled by Safety)
90005  OFF  # Sec-Fetch-Dest Header (API-specific)
```

**PR Comment Example**:
```markdown
## 🔍 Dynamic Application Security Testing (ZAP)
⚠️ Medium-risk security issues detected
**Issues Found**: 4 Medium, 0 Low
✅ **Passed Checks**: 68

**Alert Details**:
• **X-Content-Type-Options Header Missing** (medium) - 1 instance(s)
• **Storable and Cacheable Content** (medium) - 3 instance(s)
```

#### Job 7: 📋 **Pipeline Summary** (`pr-summary`)

**Purpose**: Consolidated status reporting

**What it does**:
1. Aggregates results from all jobs
2. Provides overall pipeline status
3. Lists individual job outcomes with status indicators
4. Links to detailed reports and artifacts

**Status Indicators**:
- ✅ Success
- ❌ Failure
- ⏹️ Cancelled  
- ⏭️ Skipped

**PR Comment Example**:
```markdown
## 📋 CI/CD Pipeline Summary
✅ All checks passed

### Job Results:
✅ Code Formatting & Linting
✅ Unit Tests
✅ Coverage Report
✅ Security Scan (Bandit)
✅ Dependency Check (Safety)
✅ DAST Security Scan (ZAP)
```

## 🔧 Technology Stack

### Development Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI | High-performance async API framework |
| **Package Manager** | UV | Ultra-fast Python package manager |
| **Dependency Management** | pyproject.toml + uv.lock | Modern Python project configuration |
| **Container Runtime** | Docker | Application containerization |
| **Testing Framework** | pytest | Comprehensive testing suite |
| **Type Checking** | Pydantic | Runtime type validation |

### DevSecOps Tools

| Category | Tool | Purpose |
|----------|------|---------|
| **SAST** | Bandit | Static code security analysis |
| **SCA** | Safety | Dependency vulnerability scanning |
| **DAST** | OWASP ZAP | Dynamic application security testing |
| **Code Quality** | Black, isort, Ruff | Code formatting and linting |
| **Testing** | pytest, coverage | Unit testing and coverage |
| **Coverage** | insightsengineering/coverage-action | Advanced coverage reporting |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **CI/CD Platform** | GitHub Actions | Automated pipeline execution |
| **Container Registry** | GitHub Container Registry | Docker image storage |
| **Artifact Storage** | GitHub Actions Artifacts | Report and log storage |
| **Security Scanning** | GitHub Security Tab | Centralized vulnerability tracking |

## 🛡️ Security Implementation

### Security-by-Design Principles

1. **Shift-Left Security**: Security checks at every stage
2. **Defense in Depth**: Multiple security layers
3. **Least Privilege**: Minimal required permissions
4. **Fail-Safe Defaults**: Secure default configurations
5. **Security Automation**: Automated vulnerability detection

### Security Layers

#### Application Level
- **Input Validation**: Pydantic models with type checking
- **Security Headers**: OWASP-recommended HTTP headers
- **Error Handling**: Secure error responses without information disclosure

#### Pipeline Level
- **Branch Protection**: Enforced Git Flow policies
- **Dependency Scanning**: Automated vulnerability detection
- **Static Analysis**: Code security pattern analysis
- **Dynamic Testing**: Runtime security verification

#### Infrastructure Level
- **Container Security**: Multi-stage Docker builds with minimal attack surface
- **Secrets Management**: GitHub Secrets for sensitive data
- **Access Control**: Limited GitHub Actions permissions

### Vulnerability Management

1. **Detection**: Automated scanning in CI/CD
2. **Assessment**: Risk-based prioritization
3. **Remediation**: Clear guidance in PR comments
4. **Verification**: Re-scanning after fixes
5. **Tracking**: Historical vulnerability trends

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- Docker
- Git

### Local Development

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd simple-devsecops-pipeline
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Run Application**:
   ```bash
   uv run uvicorn src.main:app --reload
   ```

4. **Run Tests**:
   ```bash
   uv run pytest --cov=./src
   ```

5. **Security Scan**:
   ```bash
   uv run bandit -r src/
   uv run safety check
   ```

### Docker Development

1. **Build Image**:
   ```bash
   docker build -t fastapi-app .
   ```

2. **Run Container**:
   ```bash
   docker run -p 8000:8000 fastapi-app
   ```

## 📋 Development Workflow

### Git Flow Process

1. **Feature Development**:
   ```bash
   git checkout -b feature/new-feature
   # Develop feature
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

2. **Integration to Develop**:
   ```bash
   git checkout develop
   git merge feature/new-feature
   git push origin develop
   ```

3. **Release to Main**:
   ```bash
   # Create PR: develop → main
   # Pipeline automatically runs
   # Review security/quality reports
   # Merge after approval
   ```

### PR Review Checklist

- [ ] All pipeline jobs pass
- [ ] Code coverage maintained/improved
- [ ] No high-severity security issues
- [ ] Dependency vulnerabilities addressed
- [ ] DAST scan shows no critical findings
- [ ] Code review approved

## 🎯 Best Practices Implemented

### Code Quality
- Consistent code formatting (Black)
- Import organization (isort)
- Comprehensive linting (Ruff)
- Type hints and validation (Pydantic)

### Security
- Static code analysis (Bandit)
- Dependency vulnerability scanning (Safety)
- Dynamic security testing (OWASP ZAP)
- Security headers implementation

### Testing
- Comprehensive unit test coverage
- Edge case and error condition testing
- Integration testing with FastAPI TestClient
- Coverage tracking and reporting

### CI/CD
- Branch-based pipeline triggers
- Parallel job execution for efficiency
- Comprehensive artifact collection
- Detailed PR feedback

---

## 📞 Support & Contributing

### Getting Help

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Community support via GitHub Discussions
- **Documentation**: Comprehensive guides in `/docs`

### Contributing

1. Fork the repository
2. Create a feature branch from `develop`
3. Make your changes
4. Ensure all pipeline checks pass
5. Submit a pull request to `develop`

---

**Built with ❤️ for secure, reliable software delivery**