# import modules
import pandas as pd
import calendar


# read csv
data = input('\n''Enter absolute path to CSV: ').strip(' ')
df = pd.read_csv(data, header = 0)


# add DLOC columns and specified values
df['Month'] = ('')
df['Day'] = ('')
df['Related URL'] = ('https://idep.library.ucla.edu/search#!/document/')
df['Related URL (link)'] = df['Related URL'] + df['PID']
df.drop(['Related URL', 'PID'], axis = 1, inplace = True)
df['Related URL (Label)'] = ('Full item available here')
df['Identifier Type'] = ('local')
df['Genre Authority'] = ('lcgft')
df['Continent'] = ('North and Central America')
df['Province'] = ('La Habana')
df['Country'] = ('Cuba')
df['Funding source'] = ('Arcadia Fund')
df['Source Institution Code'] = ('iUCLA')
df['Rights Statement'] = ('This item was contributed to the Digital Library of the Caribbean (dLOC) by the source institution listed in the metadata. This item may or may not be protected by copyright in the country where it was produced. Users of this work have responsibility for determining copyright status prior to reusing, publishing or reproducing this item for purposes other than what is allowed by applicable law, including any applicable international copyright treaty or fair use or fair dealing statutes, which dLOC partners have explicitly supported and endorsed. Any reuse of this item in excess of applicable copyright exceptions may require permission. dLOC would encourage users to contact the source institution directly or dloc@fiu.edu to request more information about copyright status or to provide additional information about the item.')


# tidy up data
df = df.fillna("")
df['dc.date'] = df['dc.date'].str.split(',', n = 1).str[0]
df['mods_originInfo_place_placeTerm_ms'] = df['mods_originInfo_place_placeTerm_ms'].str.split(r'\\', n = 1).str[0]
df['mods_titleInfo_title_ms'] = df['mods_titleInfo_title_ms'].str.split(r'\\', n = 1).str[0]
df['mods_identifier_local_ms'] = df['mods_identifier_local_ms'].str.split(',', n = 1).str[-1]
df['mods_part_detail_volume_number_ms'] = df['mods_part_detail_volume_number_ms'].str.split('.', n = 1).str[-1]
df['mods_part_detail_issue_number_ms'] = df['mods_part_detail_issue_number_ms'].str.split('.', n = 1).str[-1]
df['mods_identifier_local_ms'] = df['mods_identifier_local_ms'].str.split(',', n = 1).str[-1]
df['mods_relatedItem_host_titleInfo_title_ms'] = df['mods_relatedItem_host_titleInfo_title_ms'].str.split(',', n = 3).str[-1]


# rename Solr columns
df.rename(columns = {'mods_identifier_local_ms':'Identifier', 'mods_titleInfo_title_ms':'Title', 
                     'dc.publisher':'Creator', 'mods_language_languageTerm_text_ms':'Language', 
                     'dc.date':'Publication or creation year', 'mods_part_detail_volume_number_ms':'Volume', 
                     'mods_part_detail_issue_number_ms':'Issue', 'dc.format':'Extent', 'mods_genre_ms':'Genre', 
                     'mods_subject_topic_ms':'Subject', 'mods_originInfo_place_placeTerm_ms':'City', 
                     'mods_relatedItem_host_titleInfo_title_ms':'Series Title', 'mods_location_physicalLocation_repository_s':'Holding location statement',}, 
                     inplace = True)


# adds strings to the Holding location statement
df['Holding location statement'] = 'Newspapers are held at the ' + df['Holding location statement'].astype(str)
df['Holding location statement'] = df['Holding location statement'].astype(str) + ' in Havana, Cuba'


# separate out the subjects into their own respective columns
df = df.join(df['Subject'].str.split(',', expand=True).add_prefix('Subject'))
df.drop(['Subject'], axis = 1, inplace = True)


# adds values to date columns
df['Month'] = df['Publication or creation year'].str.split('-', n = 2).str[1]
df['Day'] = df['Publication or creation year'].str.split('-', n = 3).str[2]
df['Month'] = df['Month'].astype(int)
df['Month'] = df['Month'].apply(lambda x: calendar.month_name[x])
df['Volume'] = 'Volumen ' + df['Volume'].astype(str)
df['Issue'] = 'Numero ' + df['Issue'].astype(str)
df['Publication or creation year'] = df['Publication or creation year'].str.split('-', n = -3).str[3]


# export to csv
df.to_csv('idep_dloc_ColName.csv', index = False, encoding = 'utf-8')
print('\n''''
 /$$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$$ /$$
| $$__  $$ /$$__  $$| $$$ | $$| $$_____/| $$
| $$  \ $$| $$  \ $$| $$$$| $$| $$      | $$
| $$  | $$| $$  | $$| $$ $$ $$| $$$$$   | $$
| $$  | $$| $$  | $$| $$  $$$$| $$__/   |__/
| $$  | $$| $$  | $$| $$\  $$$| $$          
| $$$$$$$/|  $$$$$$/| $$ \  $$| $$$$$$$$ /$$
|_______/  \______/ |__/  \__/|________/|__/
                                                                                                                              
''')
