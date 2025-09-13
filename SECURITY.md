# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this FastAPI application, please report it responsibly:

1. **Do not** create a public GitHub issue for security vulnerabilities
2. Email the maintainers directly or use GitHub's Security Advisories feature
3. Include a detailed description of the vulnerability
4. Provide steps to reproduce the issue
5. If possible, include a suggested fix

## Security Features

This repository implements several security measures:

### Automated Security Scanning
- **Dependency Scanning**: Uses `safety` to check for known vulnerabilities in Python packages
- **Code Security Analysis**: Uses `bandit` to scan for common security issues in Python code
- **CI/CD Integration**: Security scans run automatically on all pull requests

### Branch Protection
- Required code reviews before merging
- Automated status checks must pass
- No force pushes to protected branches
- Signed commits required

### Development Security
- Dependencies are pinned to specific versions
- Regular automated dependency updates
- Secure database connection practices
- Input validation using Pydantic models

## Security Best Practices

When contributing to this project:

1. **Dependencies**: Keep dependencies up to date and avoid packages with known vulnerabilities
2. **Secrets**: Never commit secrets, API keys, or credentials to the repository
3. **Input Validation**: Always validate and sanitize user inputs
4. **Database Security**: Use parameterized queries to prevent SQL injection
5. **Authentication**: Implement proper authentication and authorization mechanisms
6. **HTTPS**: Always use HTTPS in production environments

## Security Tools Used

- `safety`: Python dependency vulnerability scanner
- `bandit`: Python security linter
- `black`: Code formatter (helps maintain consistent, readable code)
- `pytest`: Testing framework for security test coverage

## Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Update**: Within 1 week of initial response
- **Resolution**: Varies based on complexity, but prioritized based on severity

Thank you for helping keep this project secure!