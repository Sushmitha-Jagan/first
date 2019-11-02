def get_duta_id(duta_event_id):
    data={
        'duta_event_id': duta_event_id
         }
    query = "select categories, title, event_time from ods_master_events where duta_event_id=:duta_event_id;"
    result = DBSession('duta').execute(query,data).fetchone()
    match_details['title'] = result[1].encode('utf-8')
    match_details['start_time_utc'] = result[2].strftime("%s")
    return match_details
def main():
        duta_event_id='77254'
        data=get_duta_id(duta_event_id)
        print (data)
if __name__ == ' __main__ ':
        main()
