import requests
import argparse
from bs4 import BeautifulSoup
from dutalib.dbutil import DBSession, DBTransaction
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def code1(data):
    res=requests.get("https://en.wikipedia.org/wiki/List_of_FIFA_country_codes")
    s=BeautifulSoup(res.content,'html.parser')
    table=s.find('table')
    subtable=table.find_all("table")
    for subtables in subtable:
        trtag=subtables.find_all("tr")
        for trtags in trtag:
            tdtag=trtags.find_all("td")
            if not tdtag:
                continue
            country=tdtag[0].text
            code=tdtag[1].text
    #       print(country, code)
    #       con="Uganda"
            if data in country:
                return code
            else:
                return data.replace(data,"")    

def flag1(data):
    res=requests.get('https://emojipedia.org/flags/')
    s=BeautifulSoup(res.content,'html.parser')
    orderlist=s.find('ul', {'class': 'emoji-list'})
    litags=orderlist.find_all('li')
    for litag in litags:
        atag=litag.find('a')
        fin=atag.text.replace("Flag:", "")
        fin1=fin.lower()
        if data in fin1:
            return fin1.replace(data,"")
        else:
            return data                   
def value_new1(data):
    #print data
    c1=code1(data)
    f1=flag1(data)
    return ("{}{}".format(f1,c1))
def value_newww1(data1):
    data=data1
    #print data
    c1=code1(data)
    f1=flag1(data)
    return ("{}{}".format(c1,f1))

def duta_event(duta_event_id):
    data={
        'duta_event_id': duta_event_id
    }
    query = "select title from ods_master_events where duta_event_id=:duta_event_id;"
    result = DBSession('duta').execute(query,data).fetchone()
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--dat',required='True',nargs='+')
    argumets=parser.parse_args()
    dataa=argumets.dat
    for duta_event_id in dataa:
        datass1=duta_event(duta_event_id)
        team=None
        if datass1:
            [title]=datass1
            title=title.strip()
            title=title.lower()
            print u"Tittle {}".format(title)
            if  ' v ' in title:
                teams=title.split(' v ')
            else:
                teams=title.split(' vs ')
        team0=teams[0]
        team1=teams[1]
        #print team0
        #print team1
        if team0:
            data=team0
            value_new=value_new1(data)
        if team1:
            data1=team1
            value_neww1=value_newww1(data1)
        template="{}::-::{}".format(value_new,value_neww1)  
        print template
        
if __name__=='__main__':
    main()
