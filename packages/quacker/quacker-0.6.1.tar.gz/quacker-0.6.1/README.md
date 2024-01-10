# **Quacker**

**Quacker** is a streamlined command-line interface (CLI) tool designed to replicate [dbt](https://www.getdbt.com/) [`sources`](https://docs.getdbt.com/docs/build/sources) as tables from a Cloud Data `Warehouse` into a local `DuckDB` `database`. This allows for faster and more cost-effective local development with dbt.

Quacker currently support syncing from either
* Snowflake
* BigQuery

## Features

- Replicates dbt `sources` to local `DuckDB` files.
- Simplifies local `dbt` development and testing.
- Supports flexible `project` and `manifest` directory paths.
- Supports flexible dbt `targets`.
- Supports multiple `databases` from the same `warehouse`.
- (Optional) syncs `table` copies of selected dbt `models` to a DuckDB file as well.

## Quick terminology
- `warehouse` - A Cloud Data Warehouse e.g. `Snowflake`, `BigQuery`
- `database` - The highest level of data organisation in a `warehouse`. In BigQuery a `database` is called a `project`.
- `schema` - A logical grouping of `tables` within a `database`. In BigQuery a `schema` is called a `dataset`.

## Getting Started

### Prerequisites

Before using **Quacker**, you need to have the following set up:

- `Python` installed
- [**Recommended**] A `venv` virtual environment
- A valid `dbt` project with a `warehouse` `target` profile
- A valid `target` for your `warehouse` in your `dbt` `profiles.yml` file
- (Optional) `environment variables` loaded if you are using them in your dbt project.

#### DuckDB Profile
An example `duckdb` `target` profile in a `profiles.yml` is seen below.

In this example, my `dbt` `sources` exist in two `snowflake` `databases`
* `fivetran_database`
* `snowflake`

Arbitrarily I have chosen`fivetran_database` as the name of the `database` all `dbt` output will materialize in, but any of the `warehouse` `database` names could have been used here. All others need to be `attached` to the `main` `database` (here: the `database` of the name `snowflake`).

```yaml
    dev_duckdb:
      type: duckdb
      path: data_duckdb/fivetran_database.duckdb
      attach:
        - path: data_duckdb/snowflake.duckdb
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
```

#### Environment Variables
If your `dbt` project uses `environment variables`, you will need to load them before running `quack sync`. This is because
* `quack sync` reads your `profile` to find the connection details of your `warehouse`.
* some `dbt` setups use `environment variables` to store these connection details.

Here is an example of a `target` which uses environment variables to store the connection details to the `warehouse` `database`.

```yaml
    dev_snowflake:
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
      threads: 24
      type: snowflake
      user: "{{ env_var('SNOWFLAKE_USERNAME') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
```

#### [Optional] Conditionally persist docs based on context
If you have the below in your `dbt_project.yml`, you will receive the following error when running against duckdb
`ERROR: alter_column_comment macro not implemented for adapter duckdb`:
```yaml
models:
  +persist_docs:
      relation: true
      columns: true
```

Therefore, you need to have it set to only persist when running against your non-duckdb `target`. E.g.:
```yaml
  +persist_docs:
    relation: "{{ target.name == 'dev_snowflake' }}"
    columns: "{{ target.name == 'dev_snowflake' }}"
```

#### [Optional] Make your dbt models agnostic
Some sql syntax is not compatible with `duckdb`. For example, offset() is not supported in `duckdb`. Therefore, if you have a `model` that uses `offset()`, you will need to make it agnostic to the `target` `type`. This can be done using `jinja` and `if` statements. For example, the below code will work for both `duckdb` and `bigquery` `targets`:


```sql
{% if target.type == 'bigquery' -%}
    split(hubspot_contact_email_address, '@')[
        offset(1)
    ] as hubspot_contact_email_domain_extracted,
{%- elif target.type == 'duckdb' -%}
    split_part(hubspot_contact_email_address, '@', 2) as hubspot_contact_email_domain_extracted
{%- endif %}
```

> **Note** If you cannot make your `model` agnostic to the `target` `type`, you can add it to the `models_to_ignore` list in the `quacker_config.yml` file. See [Optional Configuration](#optional-configuration-quacker_configyml) for more details.

### Installation for use
```bash
pip3 install quacker
```

## [Optional] Configuration; `quacker_config.yml`

**Quacker** can be configured using a `quacker_config.yml` file. This file should be placed in the same location as your `dbt_project.yml` file. However, you don't need to create this file if you are happy with the default configuration. Below are the things you can configure in the `quacker_config.yml` file.

### `models_to_ignore`
A list of `dbt` models to "ignore". This is useful for `models` that are not compatible with `DuckDB`. For example, `models` that use `UNNEST` (`BigQuery`) or `Python` `dbt` `models`.

While we are "ignoring" these `dbt` models during we still need to be able to run `dbt` against `DuckDB` after the `sync`. To do this, the ignored `dbt` `models` are replicated as `tables` in the main DuckDB file during the `sync`.

Example config:
```yaml quacker_config.yml
models_to_ignore:
  - model1
  - model2
```

> **Note:** When subsequently running `dbt` against `DuckDB`, you will need to pass the `--exclude` argument during your `dbt runs` to avoid materialising these `models` in your `duckdb` `database` (you need to "ignore" them). Continuing the current example, my command would look like this: `dbt run --exclude stg_shopify__customers int_core__customers`.

If you are configuring `models_to_ignore`, you will also need this setting in `quacker_config.yml` so **Quacker** knows where to `sync` ignored models to. There are plans to remove this requirement in the future.
```yaml quacker_config.yml
main_duckdb_database_name:
  - fivetran_database
  ```

> **Note:** If you are using `models_to_ignore`, make sure that your `duckdb` `target` has the same `schema` name as the `warehouse` `target`. Otherwise your subsequent `dbt runs` might fail because some of the `tables` that your `models` reference with `ref()` are in a differently named `schema` than expected.

## Usage

To start using **Quacker**, run the `quack sync` command with the appropriate **_optional_** flags:

```bash
quack sync \
--project-dir <relative-path-to-your-dbt-project-directory> \
--profiles-dir <full-path-to-your-profiles-directory> \
--manifest-dir <relative-path-to-your-manifest-directory> \
--compile-target <dbt-target-profile-name>

```

### Optional Argument Flags
- `--project-dir`: **Relative** path to the directory containing your `dbt_project.yml` file. If not specified evaluates to the current working directory.
- `--profiles-dir`: **Full** path to the directory containing your `profiles.yml` file. If not specified, path is resolved [using dbt's method](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles#advanced-customizing-a-profile-directory).
- `--manifest-dir`: **Relative** path to the directory containing your `manifest.json` file. If not specified, assumed to be in `target/` relative to the `project-dir`.
- `--compile-target`: The dbt target name to sync the data from. It's also the target **Quacker** uses when running `dbt compile` before extracting identifiers. If not specified, **Quacker** uses the `default` profile.

### Example Usage
```bash
quack sync \
--project-dir . \
--profiles-dir /Users/username/path/to/profiles \
--manifest-dir ../poc_duckdb_for_local_dev/target \
--compile-target dev_snowflake
```

### Help
To see the full list of available commands and arguments, run `quack <subcommand> --help` e.g.

```bash
quack sync --help
```


## How It Works
any `quack` command performs the following steps:
1. Reads and parses the `quacker_config.yml` file if it exists.

`quack sync` performs the following extra steps:

1. Checks for the existence of a folder named `data_duckdb/` and creates it if necessary. This is where the `duckdb` files will be created.
2. Installs the `warehouse` `dbt adapter` (every time `quack sync` is run).
3. Compiles the dbt project.
4. Parses the `manifest.json` file to find identifiers of all dbt `sources` and, optionally, dbt `models` specified `quacker_config.yml`.
5. Queries the `warehouse` `database` for all `sources` and `models_to_ignore` with a cap of 10,000 rows. If any of the `sources` or `models_to_ignore` have more than 10,000 rows, **Quacker** will randomly sample 10,000 rows.
6. Saves the queried data into `DuckDB` `files`. For `sources`, one `duckdb` file is generated with the same name as the `database` in the `warehouse` instance. For`models_to_ignore`, the `main` `DuckDB` file (matching one of the `source` databases) is updated with the `model`'s data. [Here is how the main file is configured in a dbt profile](#duckdb-profile).
1. After quack sync, the `duckdb` files will be stored in a folder named `data_duckdb/`. The folder structure will look something like this:
    ```bash
    data_duckdb/
    ├── fivetran_database.duckdb
    ├── snowflake.duckdb
    └── ...
    ```

## Limitations

### Table names with reserved SQL keywords
Some table names may be reserved and cannot be used within DuckDB e.g. `order`, `select`, `table`, `view`, `where`, `with`. If you encounter this issue, you can either:
* rename the table in the source database
* add it to [models_to_ignore](#models_to_ignore).

Otherwise, the error raised will be something like
```bash
duckdb.duckdb.CatalogException: Catalog Error: Table with name ORDER does not exist!
Did you mean ""ORDER""?
LINE 1: ...an_ra_shopify."ORDER" as select * from "ORDER"
```

### Concurrent access to DuckDB files
You should not attempt to query the DuckDB database files while **Quacker** is running a sync operation. Two processes cannot connect to the same duckdb file at the same time.

The error raised will be something like
```bash
duckdb.duckdb.IOException: IO Error: Could not set lock on file "/Users/amir/Projects/poc_duckdb_for_local_dev/data_duckdb/fivetran_database.duckdb": Resource temporarily unavailable
```

## Possible future enhancements

### More `quacker_config.yml` settings
Customise row limit
- Currently, **Quacker** limits the number of rows it queries from the source database to 10,000. This is to avoid accidentally querying large tables and slowing down the sync process. In the future, we could allow users to customise this limit in the `quacker_config.yml` file.

Customise name of folder where duckdb files are stored
- Currently, **Quacker** uses the hardcoded name 'data_duckdb'

### More efficient adapter installation
Instead of installing the `warehouse` `dbt adapter` each time `quack sync` is run, we could:
- only install the `adapter` if it's not already installed.

Instead of hardcoding the install of `duckdb` and `snowflake adapters`, we could: (Done Jan 2024)
- only install the `adapter` for the `database` type of the `compile target` + `duckdb`. This will allow us to better support other databases in the future.

### DuckDB profile check and creation
If no suitable `duckdb` `target` `profile` exists, we could create one. This would involve:
- finding all `duckdb` `target`s for the `project`'s `profile`
- checking if any of the existing targets have all the `source` `databases` and use `attach` if sources are split across multiple `databases`
- if none of the `targets` are suitable, creating a new `duckdb` `target` in the `project`'s `profile`
- returning a message to the user to inform them of the new `duckdb` `target` `profile`

### Gifs for README
Add gifs to the README to show how to use **Quacker** and what it does.
* Emphasise side-by-side comparison of running dbt against warehouse vs duckdb after **Quacker** sync

### Error messages
Target issues
* When the `--compile-target` is not found in the `profiles.yml` file
* When the `--compile-target` is not of a supported `warehouse` `type`

Profiles.yml issues
* When the `profiles.yml` file is not found in the expected location

TODO write up more relevant error messages to implement as they are discovered

### Extract the main DuckDB database name from the duckdb dbt profile
- This would remove the need for the `main_duckdb_database_name` setting in `quacker_config.yml`.

### Dealing with non-compatible dbt models
- phase 1 solution _**(done Jan 2024)**_
  - Allow users to specify dbt models to ignore in a config file.
  - During `quack sync`, replicate the ignored dbt models as tables in the main DuckDB file.

- phase 2 solution
  - Temporary until phase 4 solution is implemented
  - add subcommand `quack recommend`, which from the config generates the `--exclude` argument so they can manually use it when running dbt against duckdb

- phase 3 solution
  - Add to `quack recommend`: suggest models to ignore based on incompatible syntax, such as UNNEST (BigQuery) or Python dbt models.

- phase 4 solution
  - 3- add a `quack dbt` command with args (for ignore functionality)
    - Run dbt command passed in argument e.g. `run`, `build`
      - To make this seamless use positional arguments if possible. E.g., command is `quack dbt run --full-refresh`. In this example, both `run` and `--full-refresh` are positional arguments.
      - Might need to use some sort of (*args, **kwargs) solution here?
    - Pass as an `--exclude`(?) on all the models which are ignored in the config
      - example dbt command generated and executed by **Quacker**: `dbt run --full-refresh --exclude model1,model5`
    - Stop and inform user if they try to
      - Pass `--exclude` themselves down to dbt
      - Run a dbt command which doesn't accept `--exclude` arg
      - dbt command fails

- phase 5 solution
  - 0- `quack debug`
    - TODO should this functionality be added to `quack recommend` or `quack sync` instead of a new command?
    - Among others, warn if any of the ignored models are not tables in duckdb and suggest re-run of 'quack sync'

- Long-term solution
  - `quack recommend` could generate DuckDB syntax equivalents wrapped in Jinja based on the target. For syntax not yet translated, it would fall back on the ignore recommendation.

### Debugging tools
- Develop `quack debug` to warn users of any ignored models that are not tables in DuckDB and suggest re-running `quack sync`.

### Support for other databases
As needed, we could add support for other databases in addition to the ones we currently support:
* Snowflake added Dec 2023
* BigQuery added Jan 2024

## Completed enhancements

### Retrieve connection details from target profile _**(done Jan 2024)**_
- Extract the Snowflake credentials directly from the dbt profile, avoiding the need for separate environment variables.
- Investigate dbt's source code or dbt power users' methods for retrieving these credentials. _**failed**_
-  Instead, manually code to replicate the order in which dbt searches for the `profiles.yml` file (exact name). [relevant dbt profile documentation](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles#advanced-customizing-a-profile-directory):
1. Specified using the `--profiles-dir` runtime argument
1. Environment Variable `DBT_PROFILES_DIR`: If you have set the DBT_PROFILES_DIR environment variable, dbt will use the directory specified in this variable to look for the profiles.yml file
1. **Current Working Directory**: The current working directory is the directory from which you are running the dbt command (where dbt_project.yml is)
1. Default Directory `~/.dbt/`

### Simplifying sync _**(done Jan 2024)**_
Specify compile sync target, such as `snowflake-prod` or `dev_snwflk` with `--sync_target` argument. 
- this would

## Development and Contribution

We welcome contributions and feedback on our tool! Please reach out to me if you have any questions or would like to contribute: amir.jab.93+quacker@gmail.com

### PyPI
[PyPI](https://pypi.org/project/quacker/)

### Installation for development
Clone the **Quacker** repository and install it using `pip` (ideally in a `venv` virtual environment):

```bash
git clone https://github.com/<your_username>/quacker.git
cd quacker
pip3 install -e .
```

The dot `.` represents the current directory. It can be replaced with a path to the **Quacker** repository if you cloned it elsewhere. No matter where **Quacker** is stored, you can run installed versions of it from anywhere on your machine as long as you are in the same virtual environment that you installed it in.

The `-e` flag is optional and is used to install **Quacker** in editable mode, which is useful during development of **Quacker** itself as it allows changes to be immediately effective without reinstallation. You don't need to use this flag if you are just using **Quacker**.

### Contributors
* Amir Jaber | [GitHub](https://github.com/Terroface) | [LinkedIn](https://www.linkedin.com/in/amirjaber/)

## Support

If you encounter any issues or have questions, please open an issue in the project's [GitHub repository](https://github.com/Terroface/quacker/issues).

## License

**Q** is released under the MIT License.
