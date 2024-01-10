# Unofficial BigQuery Magic Command

## Installation

```python
# from pypi
$ pip install another-bigquery-magic

# alternatively, from github
$ git clone https://github.com/kota7/another-bigquery-magic.git --depth 1
$ pip install -U ./another-bigquery-magic
```


## Usage

```python
# Set the project ID
project_id = "<project-id>"
!gcloud config set project {project_id}

# Load the bq magic command
%load_ext bq

# If already authenticated, we can run a query as below:
%bq SELECT 1 AS test
```

### Example of authentication methods

```python
# Authentication on colab
from google.colab import auth
auth.authenticate_user()

# Authentication by user log-in
# Note: to access external table with google drive, we also need "https://www.googleapis.com/auth/drive" in the scope
!gcloud auth application-default login --scopes="https://www.googleapis.com/auth/bigquery"

# Authentication with a local json file
jsonfile = "<json-file-path>"
%config BigqueryMagic.localjson = jsonfile
```
