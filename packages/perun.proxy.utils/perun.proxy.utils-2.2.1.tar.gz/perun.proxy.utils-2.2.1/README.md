# Perun proxy utils

Scripts and monitoring probes related to Perun ProxyIdP.

## Installation

Install via pip:

```sh
pip install perun.proxy.utils
```

There are several extras which are required only for some scripts:

- `[ldap]` for check_ldap and check_ldap_syncrepl
  - this also requires
    installing [build prerequisites of the python-ldap library](https://www.python-ldap.org/en/latest/installing.html#build-prerequisites)
- `[postgresql]` for check_pgsql

## Scripts

### run_probes

- script designed to execute multiple monitoring probes
- output is compatible with CheckMK
- it is required to put configuration file to `/etc/run_probes_cfg.yaml`

For usage instructions, run:

```sh
run_probes
```

### separate_ssp_script.py

- Script for remove all logs from test accounts from SimpleSAMLlogs

- Params:
  - 1 - The file name

### backup_database.sh

- Do mysqldump into `/opt/mariadb_backup` and remove all dump file older than 7 days

### separate_oidc_logs.py

- Script for remove all logs from test accounts from OIDC logs

### metadata_expiration.py

- This script checks whether there are some metadata close to expiration date

- Params:
  - 1 - url to a page which prints a time when expires the metadata closest to
    expiration

### print_docker_versions.py

- This script collects system info, docker engine info and the versions of running
  containers and then prints it to the stdout in the JSON format
- A python [docker library](https://pypi.org/project/docker/) is needed to run the
  script

- Options:
  - -e,--exclude NAMES - space delimited string of container names to exclude from the
    listing

### run_version_script.py

- This scripts runs the print_docker_version.py script on the given machines. The
  collected versions are then printed as a MD table to the stdout

- Options:
  - -e,--exclude NAMES - space delimited string of container names to exclude from the
    listing
- Params:
  - 1... - machines to run the script on in the form of user@adress, the user needs
    root privileges to execute the script

## Nagios probes

All nagios scripts are located under `nagios` directory.

### check_mongodb

Nagios monitoring probe for mongodb.

Tested options:

- connect
- connections
- replication_lag
- replset_state

(some possible options may not work since there are constructs which are not supported
by the latest mongodb versions)

For usage instructions, run:

```sh
check_mongodb --help
```

### check_saml.py

SAML authentication check compatible with SimpleSAMLphp and mitreID.

Basic OIDC check can be triggered by adding `--basic-oidc-check` switch. This checks
for `state` and `code` parameters in the result url after a log in attempt.

For more usage instructions, run:

```sh
check_saml --help
```

Example:

```sh
python3 check_saml.py
    --username "my_username"
    --password "my_password"
    --username-field "j_username"
    --password-field "j_password"
    --postlogout-string "Successful logout"
```

### check_user_logins.py

Check users which login in repeatedly more often than a specified threshold (logins per
seconds).

For usage instructions, run:

```sh
check_user_logins --help
```

Example:

```sh
python3 check_user_logins.py
    -p /var/log/proxyaai/simplesamlphp/simplesamlphp/simplesamlphp.log
    -l 5
    -s 60
    -r "^(?P<datetime>.{20}).*audit-login.* (?P<userid>[0-9]+)@muni\.cz$"
    -d "%b %d %Y %H:%M:%S"
```

### check_ldap

Check whether an LDAP server is available.

For usage instructions, run:

```sh
check_ldap --help
```

### check_ldap_syncrepl

Check whether an LDAP replica is up to date with the provider.

#### Usage

```sh
check_ldap_syncrepl --help
```

### check_privacyidea

Check whether privacyidea is available by performing TOTP authentication via the API.
Use caching arguments for avoiding failure when one TOTP code is used two times.

For usage instructions, run:

```sh
check_privacyidea --help
```

### check_pgsql

Check connection to PostgreSQL using a configurable query.

For usage instructions, run:

```sh
check_pgsql --help
```
