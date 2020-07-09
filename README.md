

# Ansible Network Triager

Set repositories of interest and run with `python -m triager -c /path/to/config.yaml`

This tool assists in weekly bug triages by fetching all issues and pull-requests 
from repositories specified in the config file that were created (or updated) 
since a pre-defined number of days (`timedelta`). These are also filtered by the `labels`
set in the config file. In case no `labels` are specified, then items that are
currently unassigned are pulled.

By default, this prints out a table built from the fetched content to the console.
When run with `--send-email` it also emails this table to all the listed maintainers.

## Usage
Options | Usage
--- | ---
'-c'|Path to config file (selects 'config.yaml' in current working directory by default)
'--log'|Print logging information on the console (default level set to INFO)
'--log-to-file'|Dump logging information to a specified file (if no file is specified, the data will be written to /tmp/triager_{{ timestamp }}.log)
'--debug'|Bumps logging level to DEBUG
'--send-email'|Send the triaged table as an email to the list of maintainers

## Notes
- An example config file (example-config.yaml) has been placed in this repository for reference.
- Tested with Python 3.6

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
