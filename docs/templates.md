# Template Catalogue

## Using This Repository
- Reference the repository as a pipeline resource:
  - `resources.repositories`: set `repository: ado-pipeline-templates`, `type: github`, `name: frasermolyneux/ado-pipeline-templates`, `endpoint: <service-connection>`.
- Call templates via `template: <path>@ado-pipeline-templates` and pass required parameters.

## Job Templates (`jobs/`)
- `build-net-core-projects.yml`: restore, build, and test .NET solutions; optional CodeQL/dependency scanning, tool manifest restore, Cobertura coverage, and extension hooks via `additionalBuildSteps`/`additionalPublishSteps`.
- `build-net-library.yml`: restore/build/pack a single library project; publishes NuGet package using `majorMinorVersion` and optional `nugetConfigPath`; CodeQL toggle.
- `build-function-app.yml`: restore/build a function app, optional CodeQL scanning, and optional artifact zip publish.
- `build-web-app.yml`: restore/build a web app, optional CodeQL scanning, and optional artifact zip publish.
- `build-sql-database.yml`: builds a `database.sqlproj` and optionally publishes a `database` artifact.
- `dependency-check.yml`: runs OWASP Dependency-Check with suppression support and publishes JUnit results; configurable `failOnCVSS`.
- `deploy-function-app.yml`: deploys a packaged function app; supports blue/green via staging slot swap; configurable retry count and environment binding.
- `deploy-web-app.yml`: deploys a packaged web app; supports blue/green slot swap with configurable retries.
- `deploy-sql-database.yml`: deploys a dacpac to Azure SQL using service principal auth; optional `sqlCmdArgs`.
- `devops-secure-scanning.yml`: installs PSRule modules and runs Microsoft Security DevOps with configurable tools/break behavior; publishes SARIF artifacts.
- `push-nuget-package.yml`: pushes a single package to NuGet.org using `nuget-token` from a variable group; expects version `majorMinorVersion.BuildId`.
- `push-nuget-packages.yml`: pushes all `.nupkg` files from an artifact using `nuget-token`.

## Stage Templates (`stages/`)
- `build-function-app.yml`: single-stage function app build that archives and publishes an artifact zip.
- `validate-terraform-environment.yml`: installs Terraform 1.0.7, runs init/validate/plan with backend and environment service connection parameters; exposes `commandOptions` with `-var-file` wiring.
- `deploy-terraform-environment.yml`: installs Terraform 1.0.7, runs init/validate/plan/apply, then emits output variables from apply JSON.

## Task Template (`tasks/`)
- `terraform-plan-and-apply.yml`: step template using Azure CLI with OIDC; performs init/validate/plan/apply with either backend file or explicit backend parameters, then captures `terraform output` to pipeline variables and artifact JSON.
