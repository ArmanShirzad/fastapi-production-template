# Add security headers middleware

## Description
Add security headers middleware to protect against common web vulnerabilities (XSS, clickjacking, etc.).

## Tasks
- [ ] Create security headers middleware in `app/core/security.py`
- [ ] Add headers: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security
- [ ] Add Content Security Policy (CSP) header
- [ ] Integrate middleware into FastAPI app
- [ ] Add configuration options for security headers
- [ ] Add tests for security headers
- [ ] Update documentation

## Files to modify
- `app/core/security.py` (new file)
- `app/main.py`
- `app/config.py`
- `tests/test_security.py` (new file)

## Difficulty
Intermediate

## Labels
`good first issue`, `help wanted`, `security`, `enhancement`
