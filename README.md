# idep-dloc-metadata-mapping
### Mapping IDEP metadata fields to DLOC metadata fields


### Requirements
* Python 3.x
* Pandas

------------

### Steps
1. Open Terminal and change your working directory to the "idep-dloc-metadata-mapping-main" folder

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
	* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure dates are in ISO-8601 format (YYYY-MM-DD). The normalized dates must be the first value in the cell. Errors will occur if human readable dates are listed first in the cell. (e.g. primero de mayo de 1952, 1952-05-01 ==> 1952-05-01, primero de mayo de 1952)
	
* ```ValueError: invalid literal for int() with base 10:```
	* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure the normalized dates (YYYY-MM-DD) do not contain extra characters like an extra ```-```. (e.g. 1984--01-01 ==> 1984-01-01)
	
* ```ValueError: cannot convert float NaN to integer```
	* Inspect the ```solr-output.csv``` and remove any rows that do not belong in the collection.
