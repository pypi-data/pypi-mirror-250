# another-bigquery-magic
Unofficial bigquery magic Command for IPython notebook

[![](https://badge.fury.io/py/another-bigquery-magic.svg)](https://badge.fury.io/py/another-bigquery-magic)

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
project_id = "<google-cloud-project-id>"
!gcloud config set project {project_id}
```


```python
# If you are authenticated to the google cloud already, skip this cell.
# Otherwise, authenticate with your choice of method.

# Example 1. Authentication on colab
from google.colab import auth
auth.authenticate_user()

# Example 2. Authentication by user log-in
# Note: to access external table with google drive,
#       we also need "https://www.googleapis.com/auth/drive" in the scope
!gcloud auth application-default login --scopes="https://www.googleapis.com/auth/bigquery"

# Example 3. Authentication with a local json file
jsonfile = "<json-file-path>"
%config BigqueryMagic.localjson = jsonfile
```


```python
# Load the bq magic command
%load_ext bq

# %bq magic command runs the query and returns the pandas data frame
%bq SELECT 1 AS test
```

    Start query at 2024-01-12 15:31:07.286991
    End query at 2024-01-12 15:31:10.047083 (Execution time: 0:00:02.760092, Processed: 0.0 GB)


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>test</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


See [example.ipynb](./example.ipynb) for more examples.
