# Lab 03 - Secure Coding Practices

## Project
**Scenario 2: SmartCampus Fee Payment Service**

This project demonstrates secure coding practices using Python, Flask, and Semgrep static analysis.

## Security Improvements
- Moved application secrets and gateway token to environment variables.
- Added student invoice ownership verification.
- Restricted `/refund` and `/import` routes to bursar role.
- Replaced MD5 receipt generation with HMAC-SHA256.
- Enabled TLS certificate verification and request timeout.
- Removed unsafe `eval()` and `pickle.loads()` usage.
- Secured template rendering and receipt file access.

## Semgrep Results
- Baseline findings: 16
- Final findings: 0
- Custom rule: `rules/no-md5.yml`

## Project Structure
- `app/` - Secure Flask application
- `reports/baseline.json` - Initial Semgrep scan
- `reports/after.json` - Final Semgrep scan
- `rules/no-md5.yml` - Custom Semgrep rule
- `tests/` - Manual security tests

## Manual Security Tests
1. Student cannot access another student's invoice.
2. Student cannot access the refund route.
3. Receipt path traversal is rejected.
4. Discount input is validated.
5. Template input is displayed literally.

## Tools
- Python
- Flask
- Semgrep
- Git and GitHub

**Course Lab:** Lab 03 - Secure Coding Practices and Static Analysis
