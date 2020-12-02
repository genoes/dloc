# idep-dloc-metadata-mapping
### Mapping a IDEP metadata spreadsheet to DLOC

**readme work in progress**

------------
### Requirements
* Python 3.x
* Pandas

------------

### Steps
1. Open Terminal and run ```curl``` command for solr metadata export csv (change ```COLL_NAMING_CONVENTION``` to the desired collection):

```curl -o solr-output.csv 'https://dl.library.ucla.edu/solr/select?q=fgs_label_s:COLL_NAMING_CONVENTION*&fl=mods_identifier_local_ms,PID,mods_titleInfo_title_ms,dc.publisher,mods_part_detail_volume_number_ms,mods_part_detail_issue_number_ms,dc.format,mods_language_languageTerm_text_ms,dc.date,mods_location_physicalLocation_repository_s,mods_relatedItem_host_titleInfo_title_ms,mods_relatedItem_host_titleInfo_title_ms,mods_genre_ms,mods_originInfo_place_placeTerm_ms,mods_subject_topic_ms&wt=csv&rows=20000'```

2. Run python script and input path to ```solr-output.csv```

3. A new csv will be exported as ```idep_dloc_ColName.csv```

------------
### Troubleshooting

```ValueError: cannot convert float NaN to integer```
* Review the ```dc.date``` column in the ```solr-output.csv```. Make sure dates are in ISO-8601 format (YYYY-MM-DD). The normalized dates must be the first value in the cell. Errors will occur if human readable dates are listed first in the cell.
