# Branch Protection and CI/CD Setup

This repository implements comprehensive branch protection rules and automated quality checks.

## Branch Ruleset

The main branch is protected with the following rules:

### Required Reviews
- At least 1 approving review required
- Stale reviews are dismissed when new commits are pushed
- Review thread resolution is required before merging

### Required Status Checks
- **Code Linting**: Ensures code follows formatting standards using Black
- **Tests**: Validates all tests pass across multiple database backends
- **Security Scan**: Checks for security vulnerabilities using safety and bandit
- Branches must be up to date before merging

### Additional Protections
- Force pushes are disabled
- Branch deletion is disabled
- Non-fast-forward updates are prevented
- Signed commits are required

## CI/CD Pipeline

The repository includes automated workflows that run on:
- Push to `main` and `develop` branches
- Pull requests targeting `main` and `develop` branches

### Workflow Jobs

1. **Code Linting**
   - Runs Black formatter in check mode
   - Ensures consistent code formatting

2. **Tests**
   - Sets up test databases (PostgreSQL, MySQL, MongoDB)
   - Installs dependencies
   - Runs pytest test suite
   - Tests against all supported database backends

3. **Security Scan**
   - Runs `safety` to check for known security vulnerabilities in dependencies
   - Runs `bandit` to scan for common security issues in Python code

## Database Support

The CI pipeline tests against:
- **PostgreSQL 15**: Running on port 5432
- **MySQL 8.0**: Running on port 3306  
- **MongoDB 7**: Running on port 27017

## Local Development

You can run the same checks locally using the provided Makefile:

```bash
# Run tests
make test

# Run linting
make lint

# Start development environment
make up
```

## Bypass Options

Organization administrators can bypass branch protection rules when necessary for emergency fixes or maintenance.

## Configuration Files

- `.github/workflows/ci.yml`: CI/CD pipeline configuration
- `.github/ruleset.yml`: Branch protection ruleset definition