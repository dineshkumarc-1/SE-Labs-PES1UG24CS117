# Lab 5: Static Code Analysis

**Project:** Pharmacy Manager  
**Tools Used:** Pylint, Bandit, Flake8  

---

## Issues Identified and Fixes Implemented

The table below documents the issues identified across Bandit, Pylint, and Flake8, their location in the original file, severity/type, and the fix applied.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Shell Command Injection (`os.system`) | Security (Bandit High / CWE-78) | 68 | `os.system("echo Dispensing label: " + name)` uses a shell command with concatenated input, creating a command injection vulnerability. | Replaced `os.system()` with Python's built-in `print(f"Dispensing label: {name}")`. |
| Weak Hash Algorithm (MD5) | Security (Bandit High / CWE-327) | 51 | `hashlib.md5((name + phone).encode()).hexdigest()` uses MD5 to generate patient identifiers, which is vulnerable to collision and preimage attacks. | Replaced MD5 with cryptographically secure SHA-256 (`hashlib.sha256()`). |
| Unrestricted Code Evaluation (`eval`) | Security / Bug (Bandit Med / CWE-78, Pylint W0123) | 48 | `eval(formula)` executes arbitrary Python code from doctor notes, allowing arbitrary code execution. | Replaced `eval()` with an AST-based safe arithmetic parser (`ast.parse()`, `ast.BinOp`, `operator` whitelist) limiting operations to `+`, `-`, `*`, `/`. |
| Insecure Deserialization (`pickle`) | Security (Bandit Med / CWE-502) | 3, 64 | `pickle.load(f)` deserializes untrusted data, enabling arbitrary code execution if the data file is tampered with. | Replaced `pickle` serialization with standard, safe JSON (`json.dump()` and `json.load()`). |
| Hardcoded Database Password | Security (Bandit Low / CWE-259) | 11 | `DB_PASSWORD = "pharma@123"` hardcodes credentials directly into the source code. | Extracted password retrieval to an environment variable via `os.environ.get("PHARMACY_DB_PASSWORD")`. |
| Insecure Pseudo-Random Number Generator | Security (Bandit Low / CWE-330) | 54 | `random.randint(100000, 999999)` produces predictable prescription numbers unsuitable for security/uniqueness. | Replaced `random` with cryptographically secure `secrets.randbelow()` (`secrets` module). |
| Bare `except:` & Silenced Errors | Bug / Security (Bandit Low / CWE-703, Pylint W0702, Flake8 E722) | 27 | Bare `except:` with `pass` silently swallows all exceptions, hiding errors and masking unexpected bugs. | Removed bare `except`; implemented explicit stock quantity validations and proper boolean status returns. |
| Mutable Default Argument | Bug (Pylint W0102) | 13 | `def addMedicine(..., audit=[])` uses a mutable list as default argument, causing audit state to be shared across function calls. | Changed default value to `audit=None` and initialized `if audit is None: audit = []` inside the function body. |
| Non-standard Function Naming (`camelCase`) | Code Quality (Pylint C0103) | 13, 22, 30, 33, 40, 46, 50, 53, 56, 61, 67, 70, 78, 84 | Function names (e.g., `addMedicine`, `dispenseMedicine`, `getQuantity`) did not conform to PEP 8 `snake_case`. | Renamed all functions to `snake_case` (e.g., `add_medicine`, `dispense_medicine`) and updated all invocations. |
| Missing Documentation Docstrings | Documentation (Pylint C0114, C0116) | 1, 13, 22, 30, 33, 40, 46, 50, 53, 56, 61, 67, 70, 78, 84, 89 | Missing module docstring and function docstrings explaining parameters and return values. | Added PEP 257 compliant docstrings to the module and to every function definition. |
| Unused Imports | Code Quality (Pylint W0611, Flake8 F401) | 2, 6 | Unused imports `sys` and `logging` clutter namespace and increase startup overhead. | Removed unused `sys` and `logging` imports. |
| PEP 8 Spacing & Line Length Violations | Formatting (Flake8 E302, E305, E501) | 13, 19, 22, 87, 98, 108 | Lines exceeding 79 characters and missing 2 blank lines between top-level function definitions. | Reformatted code using standard 2 blank lines between functions and wrapped long expressions within 79 characters. |

---

## Results After Fixing the Issues

- **Pylint Score:** **9.93 / 10** (threshold requirement: > 9.5)
- **Bandit Security Scan:** **0 issues identified** (all 8 issues resolved)
- **Flake8 Style Check:** **0 violations** (clean run)

---

## Conclusion

By systematically applying Pylint, Bandit, and Flake8, all identified security vulnerabilities, logic defects, naming inconsistencies, and style violations were resolved. The program behavior remains completely intact while reaching high code quality and security standards.
