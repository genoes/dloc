# idep-dloc-metadata-mapping
### Mapping a IDEP metadata spreadsheet to DLOC


### Requirements
* Python 3.x
* Pandas

------------

### Steps
1. Open Terminal and run the following ```curl``` command for the IDEP solr metadata export CSV (change ```COLL_NAMING_CONVENTION``` to the desired collection. e.g. *ihc_comunista*):

```curl -o solr-output.csv 'https://dl.library.ucla.edu/solr/select?q=fgs_label_s:COLL_NAMING_CONVENTION*&fl=mods_identifier_local_ms,PID,mods_titleInfo_title_ms,dc.publisher,mods_part_detail_volume_number_ms,mods_part_detail_issue_number_ms,dc.format,mods_language_languageTerm_text_ms,dc.date,mods_location_physicalLocation_repository_s,mods_relatedItem_host_titleInfo_title_ms,mods_relatedItem_host_titleInfo_title_ms,mods_genre_ms,mods_originInfo_place_placeTerm_ms,mods_subject_topic_ms&wt=csv&rows=20000'```

2. Run python script and input path to ```solr-output.csv```

3. A new CSV will be exported as ```idep_dloc_ColName.csv```

------------
### Troubleshooting

1. ```ValueError: cannot convert float NaN to integer```
* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure dates are in ISO-8601 format (YYYY-MM-DD). The normalized dates must be the first value in the cell. Errors will occur if human readable dates are listed first in the cell. (e.g. primero de mayo de 1952, 1952-05-01 ==> 1952-05-01, primero de mayo de 1952)

2. ```ValueError: invalid literal for int() with base 10:```
* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure the normalized dates (YYYY-MM-DD) do not contain extra characters like an extra ```-```. (e.g. 1984--01-01 ==> 1984-01-01)

3.```AttributeError: Can only use .str accessor with string values!```
* This error occurs when there are no columns present for volume/issue. **Work in progress!**
