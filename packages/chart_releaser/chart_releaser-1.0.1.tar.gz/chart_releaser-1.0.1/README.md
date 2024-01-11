# Helm chart releaser

This tool **requirement helm binary in machine.**

The utility can create a helm package and upload it to the gitlab registry in the **stable** or **develop** channel.
[More information in gitlab documentation](https://docs.gitlab.com/ee/user/packages/helm_repository/)

When uploading to develop channel, the same versions are allowed to be uploaded. When installing helm will take the last downloaded version.

Uploading identical versions to stable channel is forbidden in the code.

# CLI and default vars

1. **-t || --token** - token for registry. Override if env **CHART_RELEASE_TOKEN** is exist.
2. **--ssl** - path to SSL certificate for registry. Override if env **SSL_PATH** is exist. Default value **/usr/local/share/ca-certificates/CA.crt**.
3. **-u || --registry-url** - registry URL, domain only like gitlab.com. Override if env **REGISTRY_URL** is exist. Default **gitlab.com**.
4. **-p || --project-id** - CI_PROJECT_ID for gitlab registry. Override if env **RELEASE_PROJECT_ID** is exist.
5. **-n || --chart-name** - chart name.
6. **-path** - path to Chart.yaml.
7. **-c || --config** - path to config file. Override if env **TOOL_CONFIG_PATH** is exist. Default **hc-releaser.config**. File exist in repository and need for local development, because for gitlab registy must use headers with **JOB-TOKEN** if you usage **CI_JOB_TOKEN** and **PRIVATE-TOKEN** if you usage your private token. This is dynamic paramenter and by default usage **JOB-TOKEN**. If config does not exist usage **JOB_TOKEN** also. 


# Usage

Run helm lint

```bash
hc-releaser helm linting -p <path to helm chart>
```
Optional key **-d** || **--debug** - bolean. If set, helm running with debug mode.

Create and upload pre release helm package

```bash
hc-releaser helm release_stage -t <gitlab_token> -u <gitlab url. Domain only> -p <gitlab_project_id> -n <chart_name> -path <path to dir with Chart.yaml>
```

Create and upload release helm package

```bash
hc-releaser helm release -t <gitlab_token> -u <gitlab url. Domain only> -p <gitlab_project_id> -n <chart_name> -path <path to dir with Chart.yaml>
```

Check version in package registry

```bash
hc-releaser helm check -t <gitlab_token> -u <gitlab url. Domain only> -p <gitlab_project_id> -n <chart_name> -path <path to dir with Chart.yaml>
```
