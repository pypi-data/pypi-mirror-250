# GENERAL INDEX PYTHON SDK #

This document describes the General Index Python SDK which enables external users to use the GX platform tools within
their python scripts.

The Python SDK can be used within:

- a single python script that is run thanks to the Python Runner task within a pipeline in the GX application

- a single Jupyter Notebook that is run thanks to the Jupyter Runner task within a pipeline in the GX application

- an ensemble of python scripts that are part of a container, for a Task created by the user, used in a pipeline in the
  GX application

Note that the SDK does not cover everything from API documentation but rather commonly used features.

The scope of the SDK:

- **GX API** - retrieves data directly from GX API endpoints
- **Datalake Handler** - downloading / uploading / reading files from the data lake
- **Time Series Handler** - retrieves data directly from the time series database

## How to install and set the package:

### Install

```text
pip3 install generalindex==0.1.13
```

As the library is available from pip, it can be installed as a specific version within a Python Task from within
requirements.txt just by adding:

```text
generalindex==0.1.13
```

The package relies on the other libraries so, in the project, the user must install this library in the requirements.txt
file.

```text
pip3 install requests==2.31.0
pip3 install urllib3==2.1.0
pip3 install deprecated==1.2.14
```

### Environment Variables

The package uses information from the environment variables. They are automatically provided when running a script
within a pipeline (as a Task or within the Python/Jupyter Runners).
If running locally the script, users must set them in the project to be able to run the project locally.

Mandatory environment variables to set:

- Credentials:
  -
      - LOGIN → login received from GX
      - PASSWORD → password to log in.
       or:
      - NG_API_AUTHTOKEN → api-token received from GX 
- Credentials are used to generate the token so that each request is authenticated.
- NG_API_ENDPOINT → the URL to the GX platform API (by default, the url is set to https://api.g-x.co)

This allows to pass the authentication process and directs users' requests to the GX environment API.

Other variables may be useful when creating the tasks within the platform:

- NG_STATUS_GROUP_NAME → the group on the data lake where the pipeline is located, and is used to display the statuses
- NG_COMPONENT_NAME → the name of the pipeline, and is used to display the statuses
- EID → any value; when the pipeline is executed, this value is set by the GX platform

- JOBID → any value; when the pipeline is executed, this value is set by the GX platform

- PIPELINE_ID → any value; when the pipeline is created, this value is set by the GX platform

--- - 

# GX API

## Index endpoint

### How to get the list of existing symbols for a given group ?

Data saved in the time series database is structured by group, keys and timestamp.
Each set of keys has unique dates entries in the database, with corresponding columns values.

To explore what are the available symbols for a given group, the following method can be used:

```python
import generalindex as gx

# Instantiate GxApi class
gx_api = gx.GxApi()

# Get the list of symbols for given group
group = 'My Group'
group_symbols = gx_api.get_symbols(group_name=group)
```

The default size of the returned list is 1 000 items.

Note that the return object from the get_symbols() method is a JSON (python dict) where the keys and columns are
accessible in the *items* key of the JSON.

### How to query by metadata or descriptions?

In order to find the symbols querying by the metadata, column or symbol names, search_for parameter may be used.
It will look for passed string in the whole time series database and return the JSON with keys and columns where
searched string appears.

```python
import generalindex as gx

# Instantiate Timeseries class
gx_api = gx.GxApi()

# Get the list of symbols for given group
search = 'symbols.code=GX0000001'
searched_symbols = gx_api.get_symbols(search_for=search)
```

Passing both group_name and search_for parameters of the get_symbols() method allows to narrow down the results from
selected group.
The user must provide either group_name or search_for to the method in order to obtain the symbols.

If trying to get the list of symbols from a group that contains more than 1 000 items, the results will be paginated (by
default into chunks of 1 000 items).
To navigate in the large results the *get_symbols()* method takes as extra arguments the size of the returned list and
the from page:

```python
import generalindex as gx

# Instantiate Timeseries class
gx_api = gx.GxApi()

# Get the list of symbols for given group
group = 'My Group'

# Get the results into chunks of 200 items for page 5
# meaning the results from the 1000th till the 1200th 
group_symbols = gx_api.get_symbols(group_name=group, _size=200, _from=5)
```

By default, these parameters are _size=1000 (the maximum limit for the items lengths) and _from=0.

### How to read data from GX API endpoints?

It is possible to use the SDK to directly query the GX API endpoints for data, using the index symbol fields (code,
period, periodType, timeRef),
the datalake group it is stored on and additional params.

The retrieved data can be:

- streamed directly to memory as a BytesIO object, both in CSV and JSON format,
- saved as a file locally with the provided path and name, both in CSV and JSON format.

Extra settings are as well available to query data:
- code: Symbol code (default '*' )
-  period: Symbol period (default '*' ).
-  period_type: Symbol periodType (default '*' )
-  time_ref: Symbol timeRef (default '*' )
-  group: Name of the group (default Prod_Indexes)
-  module: Name of the IndexModule. Can't use with 'code','period','periodType' and 'timeRef' parameter
- _from: Start date (default beginning of the day) Accepted values (where * is a number):
  - today
  - *d - specific amount of days
  - *m - specific amount of months
  - *y - specific amount of years
  - all- no specified starting point
  - {x}v- only x last values for each index
  - ISO date ex. 2022-11-21T00:00:00 
- to: End date (default end of the day) Accepted values (where * is a number):
  - today
  - *d - specific amount of days
  - *m - specific amount of months
  - *y - specific amount of years
  - ISO date ex. 2022-11-21T00:00:00
- delta: Delta will filter timeseries by insertion date instead of the actual timestamp of data (default false)
- metadata: to either return it in the response or not (default false) Accepted values: true, false, only
- metadata_fields: Filter by metadata field e.g. {"metadata.tradinghub":"NWE"} 
- order: Order of results by date (default desc)
- timezone: Timezone as string used for the timestamps in the Date column. Format: Continent/City, for example Europe/London (default UTC)
- fields: Filter by value field e.g. {"FactsheetVersion":"1"}


The following code shows an example of how to query the GX API:

 ```python
import pandas as pd

import generalindex as gx

# Instantiate Timeseries class
api = gx.GxApi()

# retrieve all available data from group according to code
# and save as query.csv in test/
api.index(code=['GX0000001'], _from='all', group='MyGroup')
.file(file_name='test/query.csv', output_type='csv')
# The retrieved data can be read as a pandas dataframe
df = pd.read_csv("test/query.csv")

# retrieve all available data from group according to code
# and stream to memory as BytesIO object
data = api.index(code=['GX0000001'], _from='all', group='MyGroup')
.csv()

# read as pandas dataframe
df = pd.read_csv(data)
```
### How to read data from GX API in JSON format?

To retrieve data in JSON format use json() method as follows. This

 ```python
import pandas as pd

import generalindex as gx

# Instantiate Timeseries class
api = gx.GxApi()

# retrieve data between from and to as json
# data will be retrieved between 2021-01-04 00:00:00 and 2021-02-05 23:59:59
# and stream to memory as BytesIO object
json_data = api.index(code=["GX0000001"],
                      group='My Group',
                      _from='2021-01-04',
                      to='2021-02-05'
                      ).json()

# retrieve all available data from group according to code
# and save as result.txt in test/
api.index(code=['GX0000001'], _from='all', group='MyGroup')
.file(file_name='test/resukt.txt', output_type='json')
```

### How to read data from GX API for specific dates?

To retrieve the data within specific time frame, user can specify the from and to params.

There are multiple options how the from and to params may look like (where * is a number): 
- from:
  - today
  - *d - specific amount of days
  - *m - specific amount of months
  - *y - specific amount of years
  - all- no specified starting point
  - {x}v- only x last values for each index
  - ISO date ex. 2022-11-21T00:00:00 
  - date ex. 2022-11-21

- to: 
  - today
  - *d - specific amount of days
  - *m - specific amount of months
  - *y - specific amount of years
  - ISO date ex. 2022-11-21T00:00:00
  - date ex. 2022-11-21


If date and time is specified then data will be retrieved exactly for the specified time frame.

Note that ISO format must be followed: YYYY-MM-DD**T**HH:mm:ss. Pay attention to the "T" letter between date and time.

 ```python
import generalindex as gx

# Instantiate Timeseries class
api = gx.GxApi()

# retrieve data between from and to
# data will be retrieved between 2021-01-04 00:00:00 and 2021-02-05 23:59:59
# saved as a csv file named test.csv
api.index(code=["GX0000001"],
          group='My Group',
          _from='2021-01-04',
          to='2021-02-05'
          ).file(file_name='test/test.csv')

# retrieve data for specific time frame
# from 2021-01-04 12:30:00
# to 2021-02-05 09:15:00
api.index(code=["GX0000001"],
          group='My Group',
          _from='2021-01-04T12:30:00',
          to='2021-02-05T09:15:00'
          ).file(file_name='test/test.csv')

# retrieve data for general time frame
# from previous 12 months
# to now
api.index(code=["GX0000001"],
          group='My Group',
          _from='12m'
          ).file(file_name='test/test.csv')

# retrieve data
# from first existing
# to 2021-02-05T09:15:00 
api.index(code=["GX0000001"],
          group='My Group',
          _from='all',
          to='2021-02-05T09:15:00'
          ).file(file_name='test/test.csv')

# retrieve data for only last 2 values
api.index(code=["GX0000001"],
          group='My Group',
          _from='2v'
          ).file(file_name='test/test.csv')
```

### How to modify the Time Zone of the data ?

The timestamps in the queried time series are set by default to UTC.
It is described in the Date column header between brackets (for example *Date(UTC)*)

To modify the timezone in the retrieved dataset, the timezone can be passed as a follow parameter.
It must respect the Continent/City format.

```python
import generalindex as gx
import pandas as pd

# Instantiate Api class
api = gx.GxApi()

# retrieve all data from group available from 2 days with Data in selected timezone
# and stream to memory as BytesIO object
data = api.index(group='My Group', _from='2d',
                 timezone='Europe/London').csv()

# read as pandas dataframe
df = pd.read_csv(data)
```

### How to get the metadata along with the data ?

It is possible to get extra columns in the retrieved data, along with the keys & column values, containing the metadata
of the symbols.
It is done by setting the argument *metadata='true'* in the retrieval function.

By default, no metadata is included in the queried data.

It is possible to get only columns containing the metadata of the symbols.
It is done by setting the argument *metadata='only'* in the retrieval function.

```python
import generalindex as gx

# Instantiate Api class
api = gx.GxApi()

# retrieve all data from group available from 2 days with metadata
# and stream to memory as BytesIO object
data = api.index(group='My Group', _from='2d',
                 metadata='true').csv()

# retrieve only metadata from group available from 2 days 
# and stream to memory as BytesIO object
metadata = api.index(group='My Group', _from='2d',
                     metadata='only').csv()

```
### How to get index codes belonging to specified module ?

The gx index codes are organized into modules.
Those can be queried using module param.

```python
import generalindex as gx

# Instantiate Timeseries class
api = gx.GxApi()

# retrieve all available data from module 'GlobalOilSelect' according to 2 codes and for 2 months 
#  get as json and stream to memory as BytesIO object
data = api.index(code=["GX000001", "GX000002"], _from="2m", module=['GlobalOilSelect']).json()
```

### How to filter the data by selected column ?

The gx index data can be queried using multiple params also by values in the columns:

By providing the dictionary of column name and column values or metadata column and value we can filter out 
data that is not needed.

```python
import generalindex as gx

# Instantiate Timeseries class
api = gx.GxApi()

# retrieve all available data from group according to 2 codes and 2 months
# get only those having FactsheetVersion equals to '1'
#  get as json and stream to memory as BytesIO object
filter_fields = {"FactsheetVersion": "1"}
data = api.index(code=["GX000001", "GX000002"], _from="2m", fields=filter_fields).json()

# retrieve all available data from group according to 2 codes and 2 months
# get only those having metadata field Currency(MD-S) equals to 'USD'
#  get as json and stream to memory as BytesIO object
metadata_fields = {"metadata.Currency": "USD"}
data = api.index(code=["GX000001", "GX000002"], _from="2m", metadata='true', metadata_fields=metadata_fields).json()
```
--- -
## Catalogue endpoint

### How to get the list of existing gx indexes?

```python
import generalindex as gx

# Instantiate GxApi class
gx_api = gx.GxApi()

# Get all GX indexes assigned to modules and save as a csv file
gx_api.catalogue().file("indexes.csv")

# Get all GX indexes and save as a csv file
gx_api.catalogue(no_module=True).file("indexes.csv")

# Get all GX indexes assigned to modules with Currency equals 'USD' as csv BytesIo
filter_fields = {'field.Currency': 'USD'}
gx_api.catalogue(fields=filter_fields).csv()

# Get only Code and Currency columns for all GX indexes assigned to modules as json BytesIo
limit_fields = ['Code', 'Currency']
gx_api.catalogue(limit_fields=limit_fields).json()
```

--- - 
## Datalake Handler

### How to download or read a file from data lake by its name ?

The DatalakeHandler class can be used as follows within a script to download or upload a file:

```python
import generalindex as gx
import pandas as pd

# Instantiate the Datalake Handler
dh = gx.DatalakeHandler()

# download file from data lake with name and group name
# it will be saved locally with name local_name.csv
dh.download_by_name(file_name='my_file.csv',
                    group_name='My Group',
                    file_type='SOURCE',
                    dest_file_name='folder/local_name.csv',
                    save=True,
                    unzip=False)

# OR read file from data lake with name and group name
# it returns a BytesIO object (kept in the RAM, not saved in the disk)
fileIO = dh.download_by_name(file_name='my_file.csv',
                             group_name='My Group',
                             file_type='SOURCE',
                             dest_file_name=None,
                             save=False,
                             unzip=False)

# read the object as pandas DataFrame
df = pd.read_csv(fileIO)

```

The download methods allows to either:

- download and save locally the wanted file, if *save=True*
- read the file directly from the datalake and get a BytesIO object (kept in memory only, that can for example be read
  by pandas as a dataframe directly)

Note that by default:

- the file is NOT saved locally, but returned as a BytesIO object (streamed from the datalake).
- the argument *dest_file_name=None*, which will save the downloaded file to the root folder with its original name.

### How to download or read a file from data lake by its ID ?

In the case that the file ID is known, it can be directly downloaded/read as follows:

```python
import generalindex as gx
import pandas as pd

# Instantiate the Datalake Handler
dh = gx.DatalakeHandler()

# download file from data lake by its ID
# it will be saved locally with name local_name.csv
dh.download_by_id(file_id='XXXX-XXXX',
                  dest_file_name='folder/local_name.csv',
                  save=True,
                  unzip=False)

# read file from data lake by its ID
# it returns a BytesIO object
fileIO = dh.download_by_id(file_id='XXXX-XXXX',
                           dest_file_name=None,
                           save=False,
                           unzip=False)

# read the object as pandas DataFrame
df = pd.read_csv(fileIO)

```

The download methods allows to either:

- download and save locally the wanted file, if *save=True*
- read the file directly from the datalake and get a BytesIO object (kept in memory only, that can for example be read
  by pandas as a dataframe directly)

Note that by default:

- the file is NOT saved locally, but returned as a BytesIO object (streamed from the datalake).
- the argument *dest_file_name=None*, which will save the downloaded file to the root folder with its original name.

### How to upload a file to the data lake?

The uploading method will upload to the given group the file at the specified path, and returns its ID on the lake:

```python
import generalindex as gx

# Instantiate the Datalake Handler
dh = gx.DatalakeHandler()

# upload file to data lake


file_id = dh.upload_file(file='path/local_name.csv', group_name='My Group', file_upload_name='name_in_the_datalake.csv',
                         file_type='SOURCE', partial_update=False,
                         avoid_duplicates=False)
```

It is possible as well to stream a python object's content directly to the datalake from memory, without having to save
the file on the disk.

The prerequisite is to pass to the uploading method a BytesIO object as file parameter (not other objects such as pandas
Dataframe).

```python
import generalindex as gx
import io

# Instantiate the Datalake Handler
dh = gx.DatalakeHandler()

# Turn the pandas DataFrame (df) to BytesIO for streaming
fileIO = io.BytesIO(df.to_csv().encode())

# upload file to data lake
file_id = dh.upload_file(file=fileIO, group_name='My Group', file_upload_name='name_in_the_datalake.csv',
                         file_type='SOURCE', partial_update=False,
                         avoid_duplicates=False)
```

--- -

## Timeseries Queries

##### Deprecated since 1.2.13! Please use GxApi() instead !!!

### How to get the list of existing symbols for a given group ?

Data saved in the time series database is structured by group, keys and timestamp.
Each set of keys has unique dates entries in the database, with corresponding columns values.

To explore what are the available symbols for a given group, the following method can be used:

```python
import generalindex as gx

# Instantiate Timeseries class
ts = gx.Timeseries()

# Get the list of symbols for given group
group = 'My Group'
group_symbols = ts.get_symbols(group_name=group)
```

The default size of the returned list is 1 000 items.

Note that the return object from the get_symbols() method is a JSON (python dict) where the keys and columns are
accessible in the *items* key of the JSON.

### How to query by metadata or descriptions?

In order to find the symbols querying by the metadata, column or symbol names, search_for parameter may be used.
It will look for passed string in the whole time series database and return the JSON with keys and columns where
searched string appears.

```python
import generalindex as gx

# Instantiate Timeseries class
ts = gx.Timeseries()

# Get the list of symbols for given group
search = 'Data description'
searched_symbols = ts.get_symbols(search_for=search)
```

Passing both group_name and search_for parameters of the get_symbols() method allows to narrow down the results from
selected group.
The user must provide either group_name or search_for to the method in order to obtain the symbols.

If trying to get the list of symbols from a group that contains more than 1 000 items, the results will be paginated (by
default into chunks of 1 000 items).
To navigate in the large results the *get_symbols()* method takes as extra arguments the size of the returned list and
the from page:

```python
import generalindex as gx

# Instantiate Timeseries class
ts = gx.Timeseries()

# Get the list of symbols for given group
group = 'My Group'

# Get the results into chunks of 200 items for page 5
# meaning the results from the 1000th till the 1200th 
group_symbols = ts.get_symbols(group_name=group, _size=200, _from=5)
```

By default, these parameters are _size=2000 (the maximum limit for the items lengths) and _from=0.

### How to read data from Timeseries database?

It is possible to use the SDK to directly query the TimeSeries database for data, given the symbol's keys, columns and
the datalake group it is stored on.

On the application, it is similar of creating a Dataprep instance, that selects a set of symbols from groups into a
basket.

The retrieved data can be:

- streamed directly to memory, retrieved as a BytesIO object, by setting *file_name* as None (default value),
- saved as a csv file locally with the provided path and name as *file_name*.

The symbols are the keys the data was saved with in the database. For a given symbol, all the keys must be passed, as a
dictionary object with the key name and value.
It is possible to use a wildcard for the symbols values, to have all the values for that key, using *.

The wanted columns are then passed as a list that can contain one or more items.
If an empty list [ ] is passed to the function, it returns all the available columns.

To read all available data for specific symbols and columns with no time frame, no start or end date are passed to the
method.

Extra settings are as well available to query data:

- Metadata: to either return it in the query of not
- Format: either get a Normalized CSV (NCSV) or a dataframe format
- Timezone: get the timestamps in the timezone of the user's account or get the data in a specific timezone
- Corrections: how to handle corrections to the TimeSeries database (corrections set to 'yes', 'no', 'history' or '
  only')
- Delta: whether to show by datatimestamp file (delta=False) or insert time (delta=True)

The following code shows an example of how to query the TimseSeries database: :

 ```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2"}
columns = ['Open', 'Close']

# retrieve all available data from group acccording to keys & columns 
# and save as query.csv in test/
ts.retrieve_data_as_csv(file_name='test/query.csv',
                        symbols=symbols,
                        columns=columns,
                        group_name='My Group'
                        )

# The retrieved data can be read as a pandas dataframe
df = pd.read_csv("test/query.csv")

# retrieve all available data from group acccording to keys & columns 
# and stream to memory as BytesIO object
fileIO = ts.retrieve_data_as_csv(file_name=None,
                                 symbols=symbols,
                                 columns=columns,
                                 group_name='My Group'
                                 )

# read as pandas dataframe
df = pd.read_csv(fileIO)
```

### How to read data from Timeseries for specific dates?

To retrieve data the data within specific time frame, user can specify the start and end date.

There are two options how the start and end date may look like:

- only date (e.g., 2021-01-04)

- date and time (e.g., 2021-02-01T12:00:00; ISO format must be followed)

For example, if user specified start_date=2021-02-01 and end_date=2021-02-06, then data will be retrieved like this:
from 2021-02-01 00:00:00 till 2021-02-06 23:59:59.

If date and time is specified then data will be retrieved exactly for the specified time frame.

Note that ISO format must be followed: YYYY-MM-DD**T**HH:mm:ss. Pay attention to the "T" letter between date and time.

 ```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2"}
columns = 'Open'

# retrieve data between start_date and end_date
# data will be retrieved between 2021-01-04 00:00:00 and 2021-02-05 23:59:59
# saved as a csv file named test.csv
ts.retrieve_data_as_csv(file_name='test/test.csv',
                        symbols=symbols,
                        columns=columns,
                        group_name='My Group',
                        start_date='2021-01-04',
                        end_date='2021-02-05'
                        )

# retrieve data for specific time frame
# from 2021-01-04 12:30:00
# to 2021-02-05 09:15:00
ts.retrieve_data_as_csv(file_name='test/test.csv',
                        symbols=symbols,
                        columns=columns,
                        group_name='My Group',
                        start_date='2021-01-04T12:30:00',
                        end_date='2021-02-05T09:15:00'
                        )

# For given keys, columns, group and dates range
# Streaming instead of saving
fileIO = ts.retrieve_data_as_csv(file_name=None,
                                 symbols=symbols,
                                 columns=columns,
                                 group_name='My Group',
                                 start_date='2021-01-04',
                                 end_date='2021-02-05'
                                 )

# read as pandas dataframe
df = pd.read_csv(fileIO)
```

### How to use a wildcard for a key's values ?

To get all the value for one a several keys for the query, the character * can be used as a wildcard.
The argument *allow_wildcard* should be set to True in the retrieval function to enable the use of wildcard.

Please note that by default, the use of wildcards is **DISABLED**.

```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2", "Key3": "*"}
columns = ['Open', 'Close']

# retrieve all history for the symbols with keys and columns
# all values for Key3 will be returned
# the data will be streamed to memory
fileIO = ts.retrieve_data_as_csv(file_name=None,
                                 symbols=symbols,
                                 columns=columns,
                                 group_name='My Group',
                                 allow_wildcard=True
                                 )

# read as pandas dataframe
df = pd.read_csv(fileIO)
```

### How to get all the columns for a given set of keys ?

To get all the columns values for a given set of keys in the database, the query can take an empty list as the queried
columns, as follow:

```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2", "Key3": "Val3"}
columns = []

# retrieve all history for the symbols with keys and columns
# all columns for the set of keys will be returned
# the data will be streamed to memory
fileIO = ts.retrieve_data_as_csv(file_name=None,
                                 symbols=symbols,
                                 columns=columns,
                                 group_name='My Group'
                                 )

# read as pandas dataframe
df = pd.read_csv(fileIO)
```

Note that this configuration can be used with keys wildcards (with *allow_wildacrd=True*) and any other setting.

### How to modify the Time Zone of the data ?

The timestamps in the queried time series are set by default in the timezone of the user's account, who created the
script or the pipeline.
It is described in the Date column header between brackets (for example *Date(UTC)*)

To modify the time zone in the retrieved dataset, the timezone can be passed directly to the retrieval function as
follows.
It must respect the Continent/City format.

```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2"}
columns = ['Open', 'Close']

# retrieve all available data from group according to keys & columns 
# and stream to memory as BytesIO object
fileIO = ts.retrieve_data_as_csv(file_name=None,
                                 symbols=symbols,
                                 columns=columns,
                                 group_name='My Group',
                                 timezone='Europe/London'
                                 )

# read as pandas dataframe
df = pd.read_csv(fileIO)
```

### How to get the metadata along with the data ?

It is possible to get extra columns in the retrieved data, along with the keys & columns values, containing the metadata
of the symbols.
It is done by setting the argument *metadata=True* in the retrieval function.

By default, no metadata is included in the queried data.

```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2"}
columns = ['Open', 'Close']

# retrieve all available data from group according to keys & columns 
# and stream to memory as BytesIO object
fileIO = ts.retrieve_data_as_csv(file_name=None,
                                 symbols=symbols,
                                 columns=columns,
                                 group_name='My Group',
                                 metadata=True
                                 )

# read as pandas dataframe
df = pd.read_csv(fileIO)
```

### How to modify the format of the received data ?

The queried data comes by default as Normalized CSV format (NCSV), with in this order:

* the keys columns,
* the date column, with timestamps in either the default timezone or the specified one (*timezone* argument in the
  function),
* the values columns,
* the metadata columns, if wanted (*metadata=True*)

By setting *NCSV=False* in the retrieval method, the data will be returned as Dataframe format (PANDAS in API docs), as
a JSON.
The JSON (python dict) has timestamps as keys and a dictionary containing pairs of symbols_columns and their value.

```python
import generalindex as gx
import pandas as pd

# Instantiate Timeseries class
ts = gx.Timeseries()

# Symbols to query from database
symbols = {'Key1': "Val1", "Key2": "Val2"}
columns = ['Open', 'Close']

# retrieve all available data from group according to keys & columns 
# and stream to memory as BytesIO object
file_json = ts.retrieve_data_as_csv(file_name=None,
                                    symbols=symbols,
                                    columns=columns,
                                    group_name='My Group',
                                    metadata=True,
                                    NCSV=False)

# read as pandas dataframe
# Transpose to have datetime as rows index
df = pd.DataFrame(file_json).T
```

Note that the dataframe, created from the JSON containing the data, is then transposed to have timestamps as
DatetimeIndex (along rows axis).
--- -

### Who do I talk to? ###

* Admin: General Index info@general-index.com