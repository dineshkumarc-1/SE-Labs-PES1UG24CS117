# Lab 5: Reflection

**Student:** Dinesh Kumar C  
**Roll Number:** PES1UG24CS117  
**Project:** Pharmacy Manager  
**Tools Used:** Pylint, Bandit, Flake8

---

## Reflection Questions

### 1. What types of issues did each tool identify?

**Pylint** identified code-quality issues such as:
- Function names not following `snake_case` naming conventions (e.g., `addMedicine`, `dispenseMedicine`).
- Missing module and function docstrings.
- Dangerous mutable default argument (`[]`) in `addMedicine`.
- Use of `eval()` (flagged as `eval-used`).
- Unused imports (`sys`, `logging`).
- Inconsistent return statements and unnecessary `else` blocks after `return`.

**Bandit** identified security vulnerabilities such as:
- Use of `os.system()` for shell command injection risk (High).
- Use of weak MD5 hashing algorithm for patient IDs (High).
- Use of `eval()` for formula evaluation (Medium).
- Use of `pickle` for insecure deserialization (Medium).
- Hardcoded password (`"pharma@123"`) in source code (Low).
- Use of `random.randint()` for prescription numbers instead of a cryptographically secure generator (Low).
- Bare `except` clause silencing all exceptions (Low).

**Flake8** identified formatting and style violations such as:
- Lines exceeding 79 characters (`E501`).
- Missing two blank lines between top-level function definitions (`E302`).
- Missing two blank lines after the last function before module-level code (`E305`).
- Unused imports (`F401`).
- Bare `except` clause (`E722`).

---

### 2. Which issues were most critical and why?

The most critical issues were identified by **Bandit**:

- **`os.system()` for shell commands (High severity):** Passing user-controlled data to a shell command can allow command injection attacks, potentially giving an attacker full system access.
- **MD5 hashing for patient IDs (High severity):** MD5 is a cryptographically broken algorithm. Using it to hash sensitive patient data (name + phone) means the hashes can be reversed or forged using precomputed rainbow tables.
- **`eval()` for dosage formulas (Medium severity):** `eval()` executes arbitrary Python code. If a malicious formula is passed (e.g., from a doctor's note field), an attacker could execute system commands or exfiltrate data.
- **`pickle` deserialization (Medium severity):** Loading a pickle file from disk is unsafe if the file has been tampered with, as it can execute arbitrary code during deserialization.

---

### 3. How did you fix the issues, and what did you learn?

| Issue | Fix Applied | What I Learned |
|---|---|---|
| `os.system()` shell injection | Replaced with Python's `print()` | Shell commands from Python are a major injection vector; pure Python alternatives are always safer. |
| Weak MD5 hashing | Replaced with SHA-256 (`hashlib.sha256`) | Hash algorithm strength matters for security; SHA-256 is the minimum acceptable standard for non-password hashing. |
| `eval()` for formulas | Replaced with an AST-based safe evaluator using `ast.parse()` and `operator` | You can evaluate arithmetic safely by walking the AST and only permitting whitelisted operations. |
| `pickle` persistence | Replaced with `json.dump` / `json.load` | JSON is human-readable, language-agnostic, and cannot execute code during loading. |
| Hardcoded password | Moved to `os.environ.get("PHARMACY_DB_PASSWORD")` | Secrets should never appear in source code; environment variables are the standard alternative. |
| Weak random for Rx numbers | Replaced `random.randint` with `secrets.randbelow` | The `secrets` module is designed for cryptographically secure tokens and should be used wherever unpredictability matters. |
| Bare `except` and silenced errors | Added specific exception types and meaningful error handling | Broad `except` clauses hide bugs; catching specific exceptions makes the code more maintainable and debuggable. |
| `camelCase` function names | Renamed all functions to `snake_case` | Following PEP 8 naming conventions improves readability and ensures consistency across Python projects. |
| Missing docstrings | Added module and function docstrings | Docstrings are essential for maintainability; they document intent and serve as the first line of API documentation. |
| Mutable default argument | Changed `audit=[]` to `audit=None` with `if audit is None: audit = []` | Mutable default arguments are shared across all calls to a function, which leads to subtle and hard-to-find bugs. |

---

### 4. How do static analysis tools improve software quality?

Static analysis tools improve software quality in several ways:

1. **Early defect detection:** Issues are caught before the code is even run, saving debugging time.
2. **Security hardening:** Tools like Bandit surface known vulnerability patterns (CWEs) that developers might overlook.
3. **Consistent style:** Tools like Flake8 enforce a shared coding standard, making code easier for teams to read and review.
4. **Knowledge transfer:** The tool warnings link to documentation that teaches developers *why* a pattern is dangerous, building long-term skills.
5. **Automated gatekeeping:** Static analysis can be integrated into CI/CD pipelines to block insecure or low-quality code from being merged.

---

### 5. What is the difference between code quality, security, and formatting tools?

| Dimension | Tool | Focus |
|---|---|---|
| **Code Quality** | Pylint | Detects logical errors, naming violations, missing documentation, and style anti-patterns that reduce maintainability. |
| **Security** | Bandit | Detects known insecure coding patterns (e.g., `eval`, `pickle`, hardcoded secrets, weak crypto) mapped to CVEs and CWEs. |
| **Formatting** | Flake8 | Enforces PEP 8 style rules — indentation, line length, blank lines, and import ordering — without evaluating logic or security. |

Each tool operates at a different layer: Flake8 is purely syntactic, Pylint reasons about structure and semantics, and Bandit reasons about security implications of specific API calls and patterns.
