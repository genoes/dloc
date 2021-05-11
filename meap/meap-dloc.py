# import modules
import pandas as pd
import calendar
import re


# read csv
data = input('\n'"Enter absolute path to solr output CSV: "'\n').strip()
genre = input('\n'"Enter the genre for this collection (e.g. newspapers, posters, etc...): "'\n').strip()
continent = input('\n'"Enter the continent associated with this collection: "'\n').strip()
province = input('\n'"Enter the province associated with this collection: "'\n').strip()
country = input('\n'"Enter the country associated with this collection: "'\n').strip()
df = pd.read_csv(data, header = 0)
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# add DLOC columns and specified values
df['Month'] = ('')
df['Day'] = ('')
df['Related URL'] = ('https://meap.library.ucla.edu/search#!/document/')
df['Related URL (Note)'] = df['Related URL'] + df['PID']
df.drop(['Related URL', 'PID'], axis = 1, inplace = True)
df['Related URL (Label)'] = ('Full item available here')
df['Identifier Type'] = ('local')
df['Genre Authority'] = ('lcgft')
df['Continent'] = (continent).title()
df['Province'] = (province).title()
df['Country'] = (country).title()
df['Funding source'] = ('Arcadia Fund')
df['Source Institution Code'] = ('iUCLA')
df['Rights Statement'] = ('This item was contributed to the Digital Library of the Caribbean (dLOC) by the source institution listed in the metadata. This item may or may not be protected by copyright in the country where it was produced. Users of this work have responsibility for determining copyright status prior to reusing, publishing or reproducing this item for purposes other than what is allowed by applicable law, including any applicable international copyright treaty or fair use or fair dealing statutes, which dLOC partners have explicitly supported and endorsed. Any reuse of this item in excess of applicable copyright exceptions may require permission. dLOC would encourage users to contact the source institution directly or dloc@fiu.edu to request more information about copyright status or to provide additional information about the item.')


# data cleaning
df = df.fillna("")
df['dc.date'] = df['dc.date'].str.split(',', n = 1).str[0]
df['mods_originInfo_place_placeTerm_ms'] = df['mods_originInfo_place_placeTerm_ms'].str.split(r'\\', n = 1).str[0]
df['mods_titleInfo_title_ms'] = df['mods_titleInfo_title_ms'].str.replace('\\', '')
df['dc.format'] = df['dc.format'].str.replace('\\', '')
df['dc.contributor'] = df['dc.contributor'].str.replace('\\', '')
df['mods_identifier_local_ms'] = df['mods_identifier_local_ms'].str.split(',', n = 1).str[-1]
df['mods_identifier_local_ms'] = df['mods_identifier_local_ms'].str.replace('.pdf', '')
df['mods_part_detail_volume_number_ms'] = df['mods_part_detail_volume_number_ms'].str.replace('vol.', 'Volumen')
df['mods_part_detail_volume_number_ms'] = df['mods_part_detail_volume_number_ms'].str.replace('\\', '')
df['mods_part_detail_issue_number_ms'] = df['mods_part_detail_issue_number_ms'].str.replace('no.', 'Numero')
df['mods_part_detail_issue_number_ms'] = df['mods_part_detail_issue_number_ms'].str.replace('\\', '')
df['dc.date'] = df['dc.date'].str.replace('\\', '')
df['mods_subject_topic_ms'] = df['mods_subject_topic_ms'].str.replace('\\', '')
df['mods_identifier_local_ms'] = df['mods_identifier_local_ms'].str.split(',', n = 1).str[-1]
df['mods_relatedItem_host_titleInfo_title_ms'] = df['mods_relatedItem_host_titleInfo_title_ms'].str.split(',', n = 3).str[-1]
df['mods_genre_ms'] = df['mods_genre_ms'].str.split(',', n = 1).str[-1]


# rename Solr columns
df.rename(columns = {'mods_identifier_local_ms':'Identifier', 'mods_titleInfo_title_ms':'Title',
                     'dc.contributor':'Creator', 'mods_language_languageTerm_text_ms':'Language',
                     'dc.date':'Publication or creation year', 'mods_part_detail_volume_number_ms':'Volume',
                     'mods_part_detail_issue_number_ms':'Issue', 'dc.format':'Extent', 'mods_genre_ms':'Genre',
                     'mods_subject_topic_ms':'Subject', 'mods_originInfo_place_placeTerm_ms':'City',
                     'mods_relatedItem_host_titleInfo_title_ms':'Series Title', 'mods_location_physicalLocation_repository_s':'Holding location statement',},
                     inplace = True)


# adds string to the Holding location statement
df['Holding location statement'] = genre.title() + ' are held at the ' + df['Holding location statement'].astype(str) +  ' in Havana, Cuba.'

# separate out the creators into their own respective columns
df['Creator'] =  df['Creator'].apply(lambda x: re.sub(r'(,[^,]*),', r'\1|', str(x)))
df = df.join(df['Creator'].str.split('|', expand = True).add_prefix('Creator'))
df.drop(['Creator'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# separate out the subjects into their own respective columns
df = df.join(df['Subject'].str.split(',', expand = True).add_prefix('Subject'))
df.drop(['Subject'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# separate out the languages into their own respective columns
df = df.join(df['Language'].str.split(',', expand = True).add_prefix('Language'))
df.drop(['Language'], axis = 1, inplace = True)
df.columns = df.columns.str.replace('[0-9]', '')


# removes all leading and trialing whitespaces in dataframe
df.replace(r"^ +| +$", r"", regex = True, inplace = True)

# (need to standardize the dates first)

# splits out the dates
#df['Month'] = df['Publication or creation year'].str.split('-', n = 2).str[1]
#df['Day'] = df['Publication or creation year'].str.split('-', n = 3).str[2]
#df['Month'] = df['Month'].astype(int)
#df['Month'] = df['Month'].apply(lambda x: calendar.month_name[x])
#df['Publication or creation year'] = df['Publication or creation year'].str.split('-').str[0]


# translates months into the Spanish form
#df = df.replace({'Month': {'January':'enero', 'February' : 'febrero', 'March':'marzo', 'April':'abril', 'May':'mayo', 'June':'junio',
#'July':'julio', 'August':'agosto', 'September':'septiembre', 'October':'octubre', 'November':'noviembre', 'December':'diciembre'}})




# export to csv
df.to_csv('idep_dloc_ColName.csv', index = False, delimiter=',', encoding = 'utf-8')
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
