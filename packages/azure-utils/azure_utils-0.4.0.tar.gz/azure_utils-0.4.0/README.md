# Azure Utils
[![PyPI version](https://badge.fury.io/py/azure_utils.svg)](https://badge.fury.io/py/azure_utils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Azure Utilities for python

## Documentation
[Technical documentation](https://connor-makowski.github.io/azure_utils/azure_utils/blob_storage.html) can be found [here](https://connor-makowski.github.io/azure_utils/azure_utils/blob_storage.html).

## Setup

Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).
<details>
<summary>
Recommended (but Optional) -> Expand this section to setup and activate a virtual environment.
</summary>

  - Install (or upgrade) virtualenv:
  ```
  python3 -m pip install --upgrade virtualenv
  ```
  - Create your virtualenv named `venv`:
  ```
  python3 -m virtualenv venv
  ```
  - Activate your virtual environment
    - On Unix (Mac or Linux):
    ```
    source venv/bin/activate
    ```
    - On Windows:
    ```
    venv\scripts\activate
    ```
</details>

```
pip install azure_utils
```

### Basic Usage
```py
import os, sys
from azure_utils.blob_storage import AZContainer

# Get the working directory of this file
wd=os.path.abspath(os.path.dirname(sys.argv[0]))

# Create a container object
az = AZContainer(
    account_url="https://<account_name>.blob.core.windows.net",
    account_key="<account_key>",
    container_name="<container_name>"
)

# Get a list of all files in the container and print the first 5
files = az.list_files(remote_folderpath='/')
print(files[:5])

# Upload a file to the container
az.upload_file(
    remote_filepath='/test.csv',
    local_filepath=f'{wd}/test_data/upload/test.csv',
    overwrite=True
)

# Download the file from the container
az.download_file(
    remote_filepath='/test.csv',
    local_filepath=f'{wd}/test_data/download/test.csv',
    overwrite=True,
    smart_sync=True
)

# Delete the file from the container
az.delete_file(
    remote_filepath='/test.csv'
)

# Upload a folder to the container
az.sync_to_remote(
    remote_folderpath='/',
    local_folderpath=f'{wd}/test_data/upload/',
    overwrite=True,
)

# Download the folder from the container
az.sync_to_local(
    remote_folderpath='/',
    local_folderpath=f'{wd}/test_data/download/',
    overwrite=True,
    smart_sync=True,
)

# Delete all files in the container
az.delete_folder(
    remote_folderpath='/',
)

# Delete all local metadata
az.clear_local_meta(f'{wd}/test_data/')
```

Contributors:

- Alice Zhao
- Connor Makowski
