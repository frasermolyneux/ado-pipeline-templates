# Copilot Instructions

## Project Overview
This repository contains reusable Azure DevOps YAML pipeline templates for builds, deployments, Terraform automation, security scanning, and NuGet publishing. Templates are consumed by other repositories via a template repository resource reference (`ado-pipeline-templates`).

## Architecture and Layout
- `jobs/` — Job-level templates (build, deploy, scan, publish)
- `stages/` — Stage-level orchestration templates (Terraform validate/deploy, function app build)
- `tasks/` — Step-level helper templates (Terraform plan-and-apply with OIDC)
- `docs/` — Documentation (`templates.md` is the template catalogue)
- `.github/workflows/` — GitHub Actions for CI (YAML validation, SonarCloud, dependency review, Dependabot auto-merge)

## Build and Validation
- No application build step; this is a YAML-only template repository.
- CI validates YAML syntax by parsing all `jobs/`, `stages/`, and `tasks/` files with Python's `yaml.safe_load`.
- Run locally: `find jobs stages tasks -name "*.yml" -exec python -c "import yaml; yaml.safe_load(open('{}'))" \;`
- SonarCloud scans run on push to `main` and on pull requests via the `codequality.yml` workflow.

## Key Conventions
- All templates are Azure DevOps YAML (not GitHub Actions); they use `parameters`, `jobs`, `stages`, `steps` schema.
- Parameter names use camelCase (e.g., `projectName`, `azureSubscription`, `codeQlEnabled`).
- .NET SDK defaults to 6.x across build templates.
- CodeQL and dependency scanning are opt-in via boolean parameters (`codeQlEnabled`).
- Artifacts are named deterministically: `${projectName}.zip` for app builds, `database` for SQL dacpac.
- Deployment templates support blue/green slot swaps using a `staging` slot.
- NuGet packages use `majorMinorVersion.BuildId` versioning and require a `nuget-token` secret from a variable group.
- Terraform templates default to version 1.0.7; the task-level template supports OIDC via Azure CLI.

## Dependencies
- No runtime dependencies; templates are consumed by Azure DevOps pipelines in other repositories.
- GitHub Actions workflows use: `actions/checkout@v6`, `SonarSource/sonarcloud-github-action@v5`, `actions/dependency-review-action@v4`, `dependabot/fetch-metadata@v2`.

## Adding or Modifying Templates
- Mirror existing parameter casing and default patterns when adding new templates.
- Keep artifact naming consistent with existing conventions.
- Update `docs/templates.md` and the README documentation list when adding templates.
- Ensure new YAML files pass syntax validation (`yaml.safe_load`).
