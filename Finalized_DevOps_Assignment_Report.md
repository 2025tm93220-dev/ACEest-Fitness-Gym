# Introduction to DevOps Assignment
## ACEest Fitness Application

**GitHub owner:** [2025tm93220-dev](https://github.com/2025tm93220-dev)  
**Expected repository:** [aceest-fitness-devops-assignment](https://github.com/2025tm93220-dev/aceest-fitness-devops-assignment)  
**Date:** 29 September 2026

## 1. Executive Summary

ACEest Fitness is a fitness-management application for maintaining client profiles and workout records. The project includes the original Python application versions supplied for the assignment and a DevOps-ready Flask service in `app.py`.

The service exposes a small REST API, uses SQLite for persistence, hashes administrator passwords, and includes automated tests. The delivery pipeline is represented by GitHub Actions, Jenkins, and Docker configuration.

## 2. Implemented Features

- Health endpoint for service monitoring.
- Administrator login using a configurable username and password.
- Password hashing with Werkzeug rather than storing the administrator password in plain text.
- Client creation and client listing.
- Duplicate client protection with an HTTP 409 response.
- Workout creation and listing for each client.
- SQLite database initialization at application startup.
- Configurable database location through `ACEEST_DATABASE`.
- Configurable administrator credentials through `ACEEST_ADMIN_USERNAME` and `ACEEST_ADMIN_PASSWORD`.

## 3. Technology Stack

- Python 3.12 in CI
- Flask 3.1.2
- SQLite
- Pytest 8.4.2
- Docker using `python:3.12-slim`
- Jenkins Pipeline
- GitHub Actions

## 4. Repository Structure

| Path | Purpose |
| --- | --- |
| `app.py` | Flask application factory and REST API |
| `tests/test_app.py` | Automated API tests |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container image definition |
| `Jenkinsfile` | Jenkins build, test, and Docker stages |
| `.github/workflows/main.yml` | GitHub Actions CI workflow |
| `README.md` | Setup and usage instructions |
| `Aceestver-*.py` and related files | Original application versions |

## 5. Testing Evidence

The following commands were executed locally using the project virtual environment:

```text
.venv/bin/python -m py_compile app.py
.venv/bin/python -m pytest -q
....                                                                     [100%]
4 passed in 0.40s
```

The tests cover:

1. Health endpoint response.
2. Successful login with configured administrator credentials.
3. Client creation and duplicate protection.
4. Workout creation and retrieval.

Docker was not available on the development machine, so the local Docker build was not executed. The GitHub Actions and Jenkins pipelines include the Docker build command for an environment with Docker installed.

## 6. Continuous Integration and Delivery

### GitHub Actions

`.github/workflows/main.yml` runs on pushes and pull requests. It:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies.
4. Compiles `app.py`.
5. Runs Pytest.
6. Builds the Docker image tagged with the commit SHA.

### Jenkins

`Jenkinsfile` provides equivalent stages for checkout, dependency installation, syntax validation, testing, and Docker image creation. The Jenkins agent must provide Python and Docker.

### GitHub setup

The supplied URL identifies the GitHub owner rather than a complete repository. Create or use the repository below before pushing:

```text
https://github.com/2025tm93220-dev/aceest-fitness-devops-assignment
```

Then add it as the project remote and push the default branch:

```bash
git init
git add .
git commit -m "Prepare ACEest Fitness DevOps assignment"
git branch -M main
git remote add origin https://github.com/2025tm93220-dev/aceest-fitness-devops-assignment.git
git push -u origin main
```

## 7. Deployment Notes

For development, the default administrator password is `change-me`. Before deployment, set a strong value for `ACEEST_ADMIN_PASSWORD`; because the account is created on first database initialization, use a new database when changing the initial credential.

The SQLite database is stored in the configured application data directory. For production use, persistent storage should be mounted at `/app/data`, or the application should be migrated to a managed relational database.

## 8. Conclusion

The project now has a testable Flask service, automated API tests, a Docker definition, and CI/CD definitions for GitHub Actions and Jenkins. The verified local result is 4 passing tests. The remaining environment-dependent check is the Docker image build, which is configured in both pipelines and can be executed after Docker is installed or by the CI runner.
