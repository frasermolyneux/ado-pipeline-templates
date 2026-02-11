# Copilot Instructions

- Purpose: reusable Azure DevOps YAML templates for builds, deploys, Terraform automation, security scanning, and NuGet publishing. Consume via template repository resource (`ado-pipeline-templates`).
- Layout: job-level templates in `jobs/`, stage-level orchestration in `stages/`, and a step-level helper in `tasks/terraform-plan-and-apply.yml`. Docs live in `docs/templates.md`.
- Usage: add a repository resource pointing at `frasermolyneux/ado-pipeline-templates`, then call templates with `template: <path>@ado-pipeline-templates` and pass required parameters. Artifact names match `projectName` or fixed names (e.g., `database`).

## Template highlights
- `jobs/build-net-core-projects.yml`: restore/build/test .NET solutions; optional CodeQL and dependency scanning; supports tool manifest restore, Cobertura coverage, and `additionalBuildSteps`/`additionalPublishSteps` hook-in.
- `jobs/build-net-library.yml`: restore/build/pack a single library; uses `majorMinorVersion.BuildId` for NuGet packages; optional `nugetConfigPath`; CodeQL toggle.
- `jobs/build-function-app.yml` and `jobs/build-web-app.yml`: restore/build for a named project (defaults `function-app`/`web-app`) on .NET 6; optional CodeQL/dependency scanning; can package and publish zip artifacts when `publishArtifact` is true.
- `jobs/build-sql-database.yml`: builds `database.sqlproj` and optionally publishes a `database` artifact.
- `jobs/dependency-check.yml`: runs OWASP Dependency-Check (HTML+JUnit) with configurable `scanPath`, suppression file, and `failOnCVSS`; always publishes test results.
- `jobs/devops-secure-scanning.yml`: installs PSRule modules then runs Microsoft Security DevOps with configurable tools/break behavior; copies and publishes SARIF logs as `CodeAnalysisLogs`.
- `jobs/deploy-function-app.yml` and `jobs/deploy-web-app.yml`: deployment jobs with optional blue/green slot swap; expect an artifact named after `projectName` containing `{projectName}.zip`; configurable retry count and target environment binding.
- `jobs/deploy-sql-database.yml`: downloads `database` artifact and deploys `database.dacpac` using `SqlAzureDacpacDeployment@1`; accepts extra `sqlCmdArgs`.
- `jobs/push-nuget-package.yml` / `jobs/push-nuget-packages.yml`: push single or multiple `.nupkg` files to NuGet.org using `nuget-token` from a variable group (default `NuGet`).

## Terraform templates
- `stages/validate-terraform-environment.yml`: Terraform 1.0.7 install, init with backend settings, then validate/plan using `environmentServiceNameAzureRM`; `commandOptions` pre-wires `-var-file`.
- `stages/deploy-terraform-environment.yml`: same as validate plus apply and emission of Terraform outputs as pipeline variables from `terraform_apply` JSON output.
- `tasks/terraform-plan-and-apply.yml`: Azure CLI + OIDC; supports backend via file or explicit settings; runs init/validate/plan/apply, writes `terraform-output.json`, and sets pipeline variables for outputs.

## Conventions and tips
- Dotnet SDK defaults to 6.x; CodeQL and dependency scanning are opt-in via `codeQlEnabled` booleans.
- Workspace cleaning is enabled on most jobs; artifacts are named deterministically (`${projectName}.zip`, `database`).
- Blue/green deploys use a `staging` slot then swap to production; ensure slots exist in the target resource group.
- NuGet push jobs assume package versioning `majorMinorVersion.BuildId` and a secret `nuget-token` available via the chosen variable group.
- When adding templates, mirror parameter casing/default patterns, keep artifact naming consistent, and update `docs/templates.md` plus the README documentation list.
