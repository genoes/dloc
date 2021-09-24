# import modules
import pandas as pd
import re


# read csv
data = input('\n'"Enter absolute path to solr output CSV: "'\n').strip()
df = pd.read_csv(data, header = 0)
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


# add DLOC columns and specified values
df['Month'] = ('')
df['Day'] = ('')
df['Extent'] = ('')
df['Measurements'] = ('')


# data cleaning
df['mods_location_physicalLocation_folderNumber_s'] = df['mods_location_physicalLocation_folderNumber_s'].fillna(0)
df = df.fillna("")
df['mods_location_physicalLocation_folderNumber_s'] = df['mods_location_physicalLocation_folderNumber_s'].astype(int)
df['mods_location_physicalLocation_folderNumber_s'] = df['mods_location_physicalLocation_folderNumber_s'].replace(0, "")
#df['dc.date'] = df['dc.date'].str.split(',', n = 1).str[0]
df['dc.date'] = df['dc.date'].str.replace('\\', '')
df['mods_titleInfo_title_ms'] = df['mods_titleInfo_title_ms'].str.replace('\\', '')
df['dc.format'] = df['dc.format'].str.replace('\\', '')
df['dc.contributor'] = df['dc.contributor'].str.replace('\\', '')
df['mods_identifier_local_ms'] = df['mods_identifier_local_ms'].str.split(',', n = 1).str[-1]
df['mods_part_detail_volume_number_ms'] = df['mods_part_detail_volume_number_ms'].str.replace('\\', '')
df['dc.description'] = df['dc.description'].str.replace('\\', '')
df['mods_part_detail_issue_number_ms'] = df['mods_part_detail_issue_number_ms'].str.replace('\\', '')
df['mods_originInfo_publisher_ms'] = df['mods_originInfo_publisher_ms'].str.replace('\\', '')
df['mods_subject_topic_ms'] = df['mods_subject_topic_ms'].str.replace('\\', '')
df['mods_subject_cartographics_coordinates_s'] = df['mods_subject_cartographics_coordinates_s'].str.replace('ﾡ', '°')
df['mods_subject_cartographics_coordinates_s'] = df['mods_subject_cartographics_coordinates_s'].str.replace('�', '°')



# rename Solr columns
df.rename(columns = {'mods_identifier_local_ms':'For Digital Support Services reference', 'mods_titleInfo_title_ms':'Title','dc.contributor':'Creator', 'mods_language_languageTerm_text_ms':'Language',
                    'dc.date':'Publication or Creation Year', 'mods_location_physicalLocation_boxNumber_s': 'Box #', 'mods_location_physicalLocation_folderNumber_s': 'Folder #',
                     'mods_part_detail_volume_number_ms':'Volume','mods_part_detail_issue_number_ms':'Issue', 'dc.description':'Abstract', 'mods_genre_ms':'Genre', 'mods_relatedItem_series_titleInfo_title_ms':'Series', 'mods_originInfo_publisher_ms': 'Publisher','mods_subject_temporal_ms':'Temporal Coverage','mods_subject_topic_ms':'Subject', 'mods_originInfo_place_placeTerm_ms':'City','mods_relatedItem_host_titleInfo_title_ms':'Series Title','mods_location_physicalLocation_repository_s':'Donor','mods_location_physicalLocation_collection_s':'Collection Name','mods_typeOfResource_s':'Material Type',
                     'dc.format':'Materials','mods_subject_geographic_ms':'Geographic Area','mods_accessCondition_copyright_services_contact_ms':'Rights Statement'},
                     inplace = True)



# separate out the creators into their own respective columns
df['Creator'] =  df['Creator'].apply(lambda x: re.sub(r'(,[^,]*),', r'\1|', str(x)))
df = df.join(df['Creator'].str.split('|', expand = True).add_prefix('Creator'))
df.drop(['Creator'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# separate out the publishers into their own respective columns
df['Publisher'] =  df['Publisher'].apply(lambda x: re.sub(r'(,[^,]*),', r'\1|', str(x)))
df = df.join(df['Publisher'].str.split('|', expand = True).add_prefix('Publisher'))
df.drop(['Publisher'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# separate out the subjects into their own respective columns
df = df.join(df['Subject'].str.split(',', expand = True).add_prefix('Subject'))
df.drop(['Subject'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# separate out the genres into their own respective columns
df = df.join(df['Genre'].str.split(',', expand = True).add_prefix('Genre'))
df.drop(['Genre'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')



# separate out the Geographic Area into their own respective columns
df = df.join(df['Geographic Area'].str.split(',', expand = True).add_prefix('Geographic Area'))
df.drop(['Geographic Area'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# Split out the coordinates and give them their own column.
# comment this block out if there are no coordinates present (it will break script)
df['mods_subject_cartographics_coordinates_s'].dropna(inplace = True)
new = df["mods_subject_cartographics_coordinates_s"].str.split(",", n = 1, expand = True)
df["Latitude"]= new[0]
df["Longitude"]= new[1]
df.drop(columns =["mods_subject_cartographics_coordinates_s"], inplace = True)


# Split out the extent/dimensions and give them their own column.
# comment this block out if there are no extent metadata present (it will break script)
#df['mods_physicalDescription_extent_s'].dropna(inplace = True)
#new = df["mods_physicalDescription_extent_s"].str.split(",", n = 1, expand = True)
#df["Extent"]= new[0]
#df["Dimensions"]= new[1]
df.drop(columns =["mods_physicalDescription_extent_s"], inplace = True)





# export to csv
df.to_csv('meap_dloc_ColName.csv', index = False, encoding = 'utf-8')
print('\n''''
 /#######   /######  /##   /## /######## /##
| ##__  ## /##__  ##| ### | ##| ##_____/| ##
| ##  \ ##| ##  \ ##| ####| ##| ##      | ##
| ##  | ##| ##  | ##| ## ## ##| #####   | ##
| ##  | ##| ##  | ##| ##  ####| ##__/   |__/
| ##  | ##| ##  | ##| ##\  ###| ##
| #######/|  ######/| ## \  ##| ######## /##
|_______/  \______/ |__/  \__/|________/|__/

''')
