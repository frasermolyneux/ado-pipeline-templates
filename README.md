# Azure DevOps Pipeline Templates

[![Build and Test](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/build-and-test.yml)
[![Code Quality](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/codequality.yml/badge.svg)](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/codequality.yml)
[![Copilot Setup Steps](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/copilot-setup-steps.yml/badge.svg)](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/copilot-setup-steps.yml)
[![Dependabot Auto-Merge](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/dependabot-automerge.yml/badge.svg)](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/dependabot-automerge.yml)
[![PR Verify](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/pr-verify.yml/badge.svg)](https://github.com/frasermolyneux/ado-pipeline-templates/actions/workflows/pr-verify.yml)

## Documentation

* [Template Catalogue](/docs/templates.md) - Summary of available job, stage, and task templates plus usage notes

## Overview

Reusable Azure DevOps YAML templates for common pipelines: .NET builds, App Service/Function packaging, Azure SQL dacpac deployment, Terraform validate/plan/apply, security scanning, and NuGet publishing. Templates are organized as job-, stage-, and task-level building blocks to be consumed via a template repository resource. Optional CodeQL and dependency scanning toggles are built in; deployment templates support blue/green slot swaps and pipeline variable emission for Terraform outputs.

Example resource reference and template usage:

```yaml
resources:
  repositories:
    - repository: ado-pipeline-templates
      type: github
      name: frasermolyneux/ado-pipeline-templates
      endpoint: frasermolyneux

steps:
  - template: tasks/terraform-plan-and-apply.yml@ado-pipeline-templates
    parameters:
      azureSubscription: '$(azureSubscription)'
      terraformFolder: 'terraform'
      terraformVarFile: 'tfvars/dev.tfvars'
```

## Contributing

Please read the [contributing](CONTRIBUTING.md) guidance; this is a learning and development project.

## Security

Please read the [security](SECURITY.md) guidance; I am always open to security feedback through email or opening an issue.
