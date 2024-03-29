# Azure DevOps Pipeline Templates

## Overview

This repository holds a set of common pipeline templates that can be used in remote pipelines. They may be changed at any time so if you do want to use them suggest forking or pulling them into your own template repository.

---

## Solution

The resource needs to be included in the AzDo pipeline:

```yaml
resources:
  repositories:
    - repository: ado-pipeline-templates
      type: github
      name: frasermolyneux/ado-pipeline-templates
      endpoint: frasermolyneux
```

The templates can then be used as such:

```yaml
  - template: jobs/terraform-validate-and-plan.yml@ado-pipeline-templates
    parameters:
      workingDirectory: '$(terraformWorkingDirectory)'
      backendServiceArm: '$(backendServiceArm)'
      backendAzureRmResourceGroupName: '$(backendAzureRmResourceGroupName)'
      backendAzureRmStorageAccountName: '$(backendAzureRmStorageAccountName)'
      backendAzureRmContainerName: '$(backendAzureRmContainerName)'
      backendAzureRmKey: '$(backendAzureRmKey)'
      environmentServiceNameAzureRM: '$(environmentServiceNameAzureRM)'
      varFile: '$(varFile)'
      additionalCommandOptions: '-var="b2c_tenant_client_id=$(client-id)" -var="b2c_tenant_client_secret=$(client-secret)"'
```

---

## Contributing

Please read the [contributing](CONTRIBUTING.md) guidance; this is a learning and development project.

---

## Security

Please read the [security](SECURITY.md) guidance; I am always open to security feedback through email or opening an issue.

---

## NuGet.org Package Publishing

For the next time this doesn't work and I get confused as to why.

* `push-nuget-package.yml` and `push-nuget-packages.yml` use a variable group called `NuGet.org` with the following variables:
  * `NUGET-PUSH-KEY-1`
* The variable group is associated with the `kv-mx-nuget-prd-uksouth` Key Vault in the `strategic-prd` subscription
