# Lab 5: Static Code Analysis

**Project:** Pharmacy Manager  
**Tools Used:** Pylint, Bandit, Flake8

## Issues Identified and Fixes Implemented

| No. | Tool | Issue Identified | Severity/Type | Fix Implemented |
|---:|---|---|---|---|
| 1 | Bandit | Use of `os.system()` to print a dispensing label | High security risk | Replaced the shell command with Python's `print()`. |
| 2 | Bandit | Use of the weak MD5 hashing algorithm | High security risk | Replaced MD5 with SHA-256. |
| 3 | Bandit/Pylint | Use of `eval()` to evaluate a dosage formula | Medium security risk | Replaced unrestricted evaluation with a safer arithmetic evaluation approach. |
| 4 | Bandit | Use of `pickle` to load stock data | Medium security risk | Replaced pickle persistence with JSON. |
| 5 | Bandit | Hardcoded database password | Low security risk | Moved the password to an environment variable. |
| 6 | Bandit | Use of a standard pseudo-random generator for prescription numbers | Low security risk | Used a cryptographically secure random-number approach. |
| 7 | Bandit/Pylint/Flake8 | Bare `except` and silently ignored errors | Low security risk / code quality | Improved exception handling. |
| 8 | Pylint | Mutable list used as a default function argument | Code quality | Changed the default argument approach to avoid sharing mutable state. |
| 9 | Pylint | Function names did not follow `snake_case` | Code quality | Renamed functions and updated their calls to follow Python naming conventions. |
| 10 | Pylint | Missing module and function docstrings | Code quality | Added documentation strings. |
| 11 | Pylint | Unused imports and other code-quality warnings | Code quality | Removed unused imports and improved the code structure. |
| 12 | Flake8 | Incorrect spacing and overly long lines | Formatting | Used `autopep8` and corrected formatting issues. |

## Results After Fixing the Issues

- **Pylint:** 9.93/10.
- **Bandit:** No issues identified.
- **Flake8:** No formatting issues reported in the after-report.

## Conclusion

The changes improved the Pharmacy Manager project's code readability, maintainability, and security. Running Pylint, Bandit, and Flake8 after making the fixes helped verify the improvements.