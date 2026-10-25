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
- `validate-terraform-environment.yml`: installs the committed root CLI, runs read-only-lock init/validate/plan with backend and environment service connection parameters, and publishes a plan execution receipt.
- `deploy-terraform-environment.yml`: installs the committed root CLI, runs read-only-lock init/validate/plan/apply, then publishes an apply receipt and emits output variables from apply JSON.

## Task Template (`tasks/`)
- `terraform-plan-and-apply.yml`: step template using Azure CLI with OIDC; performs init/validate/plan/apply with either backend file or explicit backend parameters, then captures `terraform output` to pipeline variables and artifact JSON.
- `terraform-toolchain.yml`: rejects missing/untracked root pins and locks, floating versions, and explicit version mismatches before installing the exact CLI.
- `terraform-execution-receipt.yml`: publishes only actual CLI/provider selections, lock digest, source/build identity, operation and timestamp; never publishes state, plan, output or environment contents.

## Terraform migration boundary

Commit `.terraform-version` and a Terraform-generated `.terraform.lock.hcl` in every
consumer root before adopting this revision. Optional `terraformVersion` is a
compatibility assertion and must equal the root pin; there is no `latest` fallback.
Include Linux/Windows checksums when regenerating locks in a reviewed update PR.
Normal init is read-only; Dependabot owns provider/module updates, not the CLI pin.

The stage templates retain the legacy `TerraformTaskV2@2` extension and must not be
assumed to support modern federated service connections. The Azure CLI task template
requires a workload-identity-federated service connection. No active GitHub estate
consumer was found; external Azure DevOps installations and extension versions cannot
be verified by this repository's GitHub checks. Pin the template repository revision,
validate template expansion in the consuming ADO project and review environment plans
before changing a live pipeline.

ADO receipts use `azure-devops-terraform-execution-v1`, not GitHub's receipt trust
contract. Radar does not currently import them or treat them as verified production
evidence. A plan receipt is not an apply, and apply metadata does not establish
application runtime state. Existing output-variable handling remains a separate,
potentially sensitive pipeline contract; do not include it in the receipt artifact.
