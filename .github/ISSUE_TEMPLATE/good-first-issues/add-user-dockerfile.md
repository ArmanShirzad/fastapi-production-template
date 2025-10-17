# Add USER directive to Dockerfile

## Description
The Dockerfile currently runs as root user. We should add a USER directive to run as a non-root user for better security.

## Tasks
- [ ] Add `RUN groupadd -r appuser && useradd -r -g appuser appuser` 
- [ ] Add `USER appuser` before the CMD instruction
- [ ] Ensure the appuser has proper permissions for the app directory
- [ ] Test that the container still works correctly

## Files to modify
- `Dockerfile`

## Difficulty
Beginner

## Labels
`good first issue`, `help wanted`, `security`, `docker`
