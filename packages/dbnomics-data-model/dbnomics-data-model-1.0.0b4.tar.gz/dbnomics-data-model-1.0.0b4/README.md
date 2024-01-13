# DBnomics Data Model

In DBnomics, once data has been downloaded from providers, it is converted in a common format: the DBnomics data model.

This Python package provides:

- model classes defining DBnomics entities (provider, dataset, series, etc.) with their business logic and validation rules
- a data storage abstraction to load and save those entities
- adapters implementing the data storage abstraction (e.g. `dbnomics_data_model.storage.adapters.filesystem`)

This package is used in particular by the convert script of fetchers in order to save data.

## Documentation

Please read <https://db.nomics.world/docs/data-model/>

## Validate data

To validate a directory containing data written by (or compatible with) the "filesystem" adapter:

```sh
dbnomics-validate-storage <storage_dir>
```

This script outputs the data validation errors it finds.

## Code quality

Install the development dependencies:

```sh
pip install -e .[dev]
```

### Run linter

```sh
flake8 .
```

### Run type check

```sh
mypy -p dbnomics_data_model
```

### Run tests

```sh
pytest
```

### Run code coverage

```sh
coverage run
coverage html
```

Then open `htmlcov/index.html` in your browser.

## Publish a new version

For package maintainers:

```bash
git tag x.y.z
git push
git push --tags
```

GitLab CI will publish the package to <https://pypi.org/project/dbnomics-data-model/> (see [`.gitlab-ci.yml`](./.gitlab-ci.yml)).
