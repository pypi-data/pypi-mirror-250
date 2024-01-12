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
# Note: to access external table with google drive, we also need "https://www.googleapis.com/auth/drive" in the scope
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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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




```python
%%bq
/* Cell magic is also defined */
SELECT
  1 AS x,
  2 AS y
```

    Start query at 2024-01-12 15:31:10.848227
    End query at 2024-01-12 15:31:13.636390 (Execution time: 0:00:02.788163, Processed: 0.0 GB)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Change the limit to the number of rows to get (default is 50000 rows)
%config BigqueryMagic.autolimit = 2  # at most two rows to return

q = """
SELECT 1 AS x
UNION ALL
SELECT 2 AS x
UNION ALL
SELECT 3 AS x
"""
%bq {q}

# Reset to a reasonable number
%config BigqueryMagic.autolimit = 10000
```

    Start query at 2024-01-12 15:31:13.948559
    End query at 2024-01-12 15:31:16.773933 (Execution time: 0:00:02.825374, Processed: 0.0 GB)
    Result is truncated at the row 2 of 3



```python
# Control the amount of messages
%config BigqueryMagic.showbytes = False
x = %bq SELECT false AS showbytes
display(x)

%config BigqueryMagic.showbytes = True
%config BigqueryMagic.showtime = False
x = %bq SELECT true AS showbytes, false AS showtime
display(x)

%config BigqueryMagic.showtime = True
%config BigqueryMagic.quiet = True
x = %bq SELECT true AS showbytes, true AS showtime, true AS quiet
display(x)
```

    Start query at 2024-01-12 15:31:17.086035
    End query at 2024-01-12 15:31:19.910281 (Execution time: 0:00:02.824246)



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>showbytes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>


    Processed: 0.0 GB



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>showbytes</th>
      <th>showtime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>True</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>showbytes</th>
      <th>showtime</th>
      <th>quiet</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>True</td>
      <td>True</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



```python

```
