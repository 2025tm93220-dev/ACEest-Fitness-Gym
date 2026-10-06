# ACEest-Fitness-Gym

## Fitness Management DevOps Assignment

Repository owner: [2025tm93220-dev](https://github.com/2025tm93220-dev)

GitHub repository: [ACEest-Fitness-Gym](https://github.com/2025tm93220-dev/ACEest-Fitness-Gym)

## Overview

This project packages the ACEest Fitness application as a small Flask service. It provides health checks, administrator login, client management, and workout tracking backed by SQLite.

The original Tkinter versions are retained as historical versions. The DevOps-ready service is `app.py`.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

The service listens on `http://localhost:5000`.

Default development login:

- Username: `admin`
- Password: `change-me`

Set `ACEEST_ADMIN_PASSWORD` before first startup when using a non-development environment.

## Test

```bash
python -m py_compile app.py
pytest -q
```

## Docker

```bash
docker build -t aceest-fitness .
docker run --rm -p 5000:5000 aceest-fitness
```

## CI/CD

- GitHub Actions: `.github/workflows/main.yml`
- Jenkins: `Jenkinsfile`
- Container definition: `Dockerfile`

The GitHub Actions workflow runs syntax validation, Pytest, and a Docker image build on pushes and pull requests.

## API endpoints

- `GET /health`
- `POST /login`
- `GET /clients`
- `POST /clients`
- `GET /clients/<client_id>/workouts`
- `POST /clients/<client_id>/workouts`

See `Finalized_DevOps_Assignment_Report.md` for the submission summary, implementation details, evidence, and setup instructions.

# Membership module added
