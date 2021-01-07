# idep-dloc-metadata-mapping
### Mapping IDEP metadata fields to DLOC metadata fields


### Requirements
* [Python 3.x](https://www.python.org/ "Python")
* [Pandas](https://pypi.org/project/pandas/ "Pandas")

------------

### Steps
1. Open Terminal, run ```git clone https://github.com/genoes/idep-dloc-metadata-mapping.git```, and change your current working directory to the "idep-dloc-metadata-mapping" folder.

2. Open the "solr-query.txt" file and replace ```CHANGE-ME``` with the desired collection file name prefix. e.g. *ihc_comunista*.

3. In Terminal type: ```bash solr-query.txt```

	* A CSV file named "solr-output.csv" will be exported to your current working directory

4. In Terminal type: ```python idep_dloc_mapping.py```

5. Input absolute path to the "solr-output.csv" when prompted

	* A new CSV file named "idep_dloc_ColName.csv" will be exported to your current working directory

### Manual edits
1. Edit the "Holding location statement" values IF the collection genre is anything other than "Newspapers". (See Line 51)

------------
### Troubleshooting

* ```ValueError: cannot convert float NaN to integer```
	* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure dates are in ISO-8601 format (YYYY-MM-DD). The normalized dates must be the first value in the cell. Errors will occur if human readable dates are listed first in the cell. (e.g. primero de mayo de 1952, 1952-05-01 ==> 1952-05-01, primero de mayo de 1952). This error will also occur if there are no dates present.
	* Check for any rows that only contain PIDs and delete them. (e.g. Cuba y America's solr query contains empty rows from a past test ingest.)
	
* ```ValueError: invalid literal for int() with base 10:```
	* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure the normalized dates (YYYY-MM-DD) do not contain extra characters like an extra ```-```. (e.g. 1984--01-01 ==> 1984-01-01)

* ```ValueErrorIndexError: list index out of range:```
	* Review the ```dc.date``` column in the ```solr-output.csv```. This error occurs when there are only year range dates present (e.g. 1911-1933). Solution for now is to comment out lines 62-66 and then run the script as normal.
