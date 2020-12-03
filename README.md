# idep-dloc-metadata-mapping
### Mapping a IDEP metadata spreadsheet to DLOC


### Requirements
* Python 3.x
* Pandas

------------

### Steps
1. Open the ```solr-query.txt``` file and replace ```COLL_NAMING_CONVENTION``` with the desired collection file name prefix. e.g. *ihc_comunista*):

2. Open Terminal and run the ```curl``` command: ```bash solr-query.txt```

* A CSV file will be exported as ```solr-output.csv``` to your working directory

3. Run python script and input path to ```solr-output.csv``` when prompted

4. A new CSV file will be exported as ```idep_dloc_ColName.csv```to your working directory

### Manual edits
1. Edit the ```Holding location statement``` values IF the collection genre is anything other than "Newspapers". (See Line 51)

------------
### Troubleshooting

1. ```ValueError: cannot convert float NaN to integer```
* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure dates are in ISO-8601 format (YYYY-MM-DD). The normalized dates must be the first value in the cell. Errors will occur if human readable dates are listed first in the cell. (e.g. primero de mayo de 1952, 1952-05-01 ==> 1952-05-01, primero de mayo de 1952)

2. ```ValueError: invalid literal for int() with base 10:```
* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure the normalized dates (YYYY-MM-DD) do not contain extra characters like an extra ```-```. (e.g. 1984--01-01 ==> 1984-01-01)

3. ```ValueError: cannot convert float NaN to integer```
* Inspect the ```solr-output.csv``` and remove any rows that do not belong in the collection.
