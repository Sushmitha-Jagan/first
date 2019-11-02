 # -*- coding: utf-8 -*-
  
 from dutalib.dbutil import DBSession
 28 from collections import defaultdict
 28 from sys import argv
 28 import json
 28 import argparse
 28 from datetime import datetime, timedelta
 28 import cachetools
 28 
 32 
 32 footer_message = u'${duta_group.channel_promo_auto(\'football\')}'
 32 
 32 flags = {
 32     'epl': '🏴',
 32     'bundesliga': '🇩🇪',
 32     'serie a': '🇮🇹',
 32     'laliga': '🇪🇸',
 32     'ligue 1': '🇫🇷',
 32         tournaments.add(r[0])
 32     return tournaments
 32 
 32 
 32 @cachetools.cached({})
 32 def tournament_name(normalized_tournament_name):
 32     db = DBSession('duta')
 32     query = """
 32         select tournament_name from ods_tournaments where normalized_name=:normalized
 32     """
 32     params = {
 32         'normalized': normalized_tournament_name
 32     }
 32     return db.execute(query, params).fetchone()[0]
 32 
 32 
 32 def get_match_details(duta_event_id, cut_off_time=None):
 32     db = DBSession('duta')
 32     query = """
 32         select categories, title, event_time from ods_master_events where duta_event_id =:duta_event_id
 32     """
 32     params = {
 32         'duta_event_id': duta_event_id
 32     }
 31     return match_details
 31 
 31 
 31 def article_section(tournament, matches):
 31     section_head = flags.get(tournament,'') + ' *{}*\n'.format(tournament_name(tournament).encode('utf-8'))
 31     template = '⚽ {team1} ::-:: {team2} 📹\n'
 31     message = section_head + ''
 31     for m in matches:
 31         teams = str.split(m, ' vs ')
 31         message = message + template.format(team1=teams[0], team2=teams[1])
 31     message = message + '\n\n'
 31     return message
 31 
 31 def highlights(match_details, time_of_day):
 31     if time_of_day not in ['early', 'late']:
 31         return
 31     file_name = '/tmp/football_highlights_{tod}_{dt}.txt'.format(tod=time_of_day, dt=datetime.today().strftime("%Y%m%d"))
 31     sections = []
 31     for detail in match_details:

🇫🇷 *Ligue 1*
 28 # -*- coding: utf-8 -*-
 28 
 28 from dutalib.dbutil import DBSession
 28 from collections import defaultdict
 28 from sys import argv
 28 import json
 28 import argparse
 28 from datetime import datetime, timedelta
 28 import cachetools
 28 
 32 
 32 footer_message = u'${duta_group.channel_promo_auto(\'football\')}'
 32 
 32 flags = {
 32     'serie a': '🇮🇹',
 32     'laliga': '🇪🇸',
 32     'ligue 1': '🇫🇷',
 32     'french coupe de france': '🇫🇷'
 32 }
 32 
 32 @cachetools.cached({})
 32 def get_normalized_tournament_names():
 32     db = DBSession('duta')
 32     tournaments = set()
 32     query_results = db.execute("select normalized_name from ods_tournaments where sport_name = 'football'").fetchall()
 32     for r in query_results:
 32     return tournaments
 32 
 32 
 32 @cachetools.cached({})
 32 def tournament_name(normalized_tournament_name):
 32     db = DBSession('duta')
 32     query = """
 32         select tournament_name from ods_tournaments where normalized_name=:normalized """
 32 
 32 
 32 def get_match_details(duta_event_id, cut_off_time=None):
 32     db = DBSession('duta')
 32     query = """
 32         select categories, title, event_time from ods_master_events where duta_event_id =:duta_event_id
 32     """
 32     params = {
 32         'duta_event_id': duta_event_id
 32     }
 32     result = db.execute(query, params).fetchone()
 31     match_details['title'] = result[1].encode('utf-8')
 31     match_details['start_time_utc'] = result[2].strftime("%s")
 31     return match_details	
 31 
 31 
 31 def article_section(tournament, matches):
 31     section_head = flags.get(tournament,'') + ' *{}*\n'.format(tournament_name(tournament).encode('utf-8'))
 31     template = '⚽ {team1} ::-:: {team2} 📹\n'
 31     for m in matches:
 31         teams = str.split(m, ' vs ')
 31         message = message + template.format(team1=teams[0], team2=teams[1])
 31     message = message + '\n\n'
 31     return message
 31 
 31 def highlights(match_details, time_of_day):
 31     if time_of_day not in ['early', 'late']:
 31         return
 31     file_name = '/tmp/football_highlights_{tod}_{dt}.txt'.format(tod=time_of_day, dt=datetime.today().strftime("%Y%m%d"))
 31     sections = []
 31     for detail in match_details:
 31         sections.append(article_section(detail, match_details[detail]))
 30     highlights_content = initial_message + ''.join(sections) + footer_message.encode('utf-8')
 29     with open(file_name, 'w') as f:
 28         f.writelines(highlights_content)
 27     return file_name
 26 
 25 
 24 def main():
 23     parser = argparse.ArgumentParser()
 22     parser.add_argument('-i', '--duta-event-ids', nargs='+', required=True, help='Duta event ids for which highlights are required')
      parser.add_argument('-x', '--cut-off-till', required=True, help='Highlights for matches starting upto this time will be early highligh    ts. This is in IST')
 20     early_highlights = defaultdict(list)
 19     late_highlights = defaultdict(list)
 18     arguments = parser.parse_args()
 17     today = datetime.today().strftime("%Y-%m-%d ")
 16     print "Today: %s" %today
 15     today = today + arguments.cut_off_till
 14     cutoff = datetime.strptime(today, '%Y-%m-%d %H:%M')
 13     cutoff_utc = cutoff - timedelta(hours=5, minutes=30)
 12     ts_cutoff_utc = cutoff_utc.strftime("%s")
 11     for event_id in arguments.duta_event_ids:
 10         details = get_match_details(event_id)
  9         ts_match_start = details['start_time_utc']
  8         if ts_match_start <= ts_cutoff_utc:
  7             early_highlights[details['normalized_tournament']].append(details['title'])
  6         else:
  5             late_highlights[details['normalized_tournament']].append(details['title'])
  4     print "Files: %s,%s"%(highlights(early_highlights, 'early'),highlights(late_highlights, 'late'))
  3 
  2 
  1 if __name__ == '__main__':
109     main()
create_highlight_
