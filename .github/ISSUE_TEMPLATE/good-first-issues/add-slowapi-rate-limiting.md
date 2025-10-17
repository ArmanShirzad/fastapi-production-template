# Add slowapi rate limiting

## Description
Add rate limiting to protect the API from abuse using the `slowapi` library.

## Tasks
- [ ] Add `slowapi` to requirements.txt
- [ ] Create rate limiting middleware in `app/core/rate_limit.py`
- [ ] Apply rate limits to root endpoint (`/`) and API routes (`/api/*`)
- [ ] Add configuration options for rate limits in `app/config.py`
- [ ] Add tests for rate limiting functionality
- [ ] Update documentation

## Files to modify
- `requirements.txt`
- `app/config.py`
- `app/core/rate_limit.py` (new file)
- `app/main.py`
- `tests/test_rate_limit.py` (new file)

## Difficulty
Intermediate

## Labels
`good first issue`, `help wanted`, `security`, `enhancement`
