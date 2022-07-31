# Azure DevOps Pipeline Templates

This repository holds a set of common pipeline templates that can be used in remote pipelines. They may be changed at any time so if you do want to use them suggest forking or pulling them into your own template repository.

---

## Example Usage

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
