# Cloud Infrastructure Capstone Project

A containerized Flask + PostgreSQL Todo application demonstrating a complete DevSecOps workflow.

## Architecture
- **App**: Flask backend, PostgreSQL database, nginx frontend with HTTPS
- **Containerization**: Docker multi-stage builds, Docker Compose orchestration
- **Orchestration**: Kubernetes manifests (Deployment, Service, Secrets)
- **Infrastructure as Code**: Terraform configuration for AWS resources (EC2, S3, RDS)
- **CI/CD**: GitHub Actions pipeline with SAST (Bandit) → Build → DAST (OWASP ZAP)

## Pipeline Status
- ✅ SAST scan (Bandit) — passing
- ✅ Image build — passing
- ⚠️ DAST scan — known limitation: this job doesn't start a database service, so the backend's connection retries exhaust before ZAP can scan it. This is properly configured and working in a separate repo (`docker-practice`), where DAST successfully scans the live app with the database present.

## Security Practices
- No hardcoded credentials — passwords sourced via environment variables, Kubernetes Secrets, and Terraform sensitive variables
- SSL certificates generated dynamically, never committed to version control
- `.gitignore` excludes Terraform state, private keys, and environment files
