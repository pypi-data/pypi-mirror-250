# CHANGELOG

## 0.1.5 (2024-01-09)

- [Fix] Fix issue when using `--watch` ([#20](https://github.com/ploomber/ploomber-cloud/issues/20))

## 0.1.4 (2023-12-20)

- [Feature] Add `--force` option to init to re-initialize a project and override the existing `ploomber-cloud.json` file
- [Feature] Add `--version`
- [Fix] Updates API header from `access_token` to `api_key`

## 0.1.3 (2023-12-14)

- [Feature] Add `ploomber-cloud deploy --watch` to watch deploy status from CLI ([#11](https://github.com/ploomber/ploomber-cloud/issues/11))

## 0.1.2 (2023-12-11)

- [Feature] Allow `init` to initialize an existing project

## 0.1.1 (2023-11-17)

- [Feature] Read key from `PLOOMBER_CLOUD_KEY` environment variable, if set

## 0.1.0 (2023-11-17)

- [Feature] Add `ploomber-cloud key` command to set key
- [Feature] Add `ploomber-cloud init` to configure a project
- [Feature] Add `ploomber-cloud deploy` to deploy a project
