import json
import os
import traceback
from datetime import datetime, timedelta

import requests

headers = {
    'authority': 'widget-api.livelines.com',
    'iframe-referer': 'https://livelines.com/',
    'content-type': 'application/json;charset=UTF-8'
}
test = False
sports = {
    "NFL": "NFL",
    "CFL": "CFL",
    "MLB": "MLB",
    "NBA": "NBA",
    "WNBA": "WNBA",
    "NHL": "NHL",
    "SC": "SC",
    "UFC": "UFC",
    "Boxing": "BX",
}


def scrape(auth, cat):
    print(cat['Id'], cat['Name'], cat['Abbreviation'])
    response = requests.post('https://widget-api.livelines.com/api/v1/statsrole/oddsmodule/odds',
                             headers={'authorization': f'Bearer {auth["details"]["AccessToken"]}'},
                             params={"categoriesID": cat['Id']})
    try:
        js = json.loads(response.text)
        betdsi = {f"betdsi-{cat['Abbreviation']}": []}
        if js['details']['ListEvents'] is not None:
            for event in js['details']['ListEvents']:
                eventjs = {}
                for participant in event['ListParticipants']:
                    key = f"{participant['RotationNumber']} {participant['Name']}".title()
                    data = {key: {"Date": str(datetime.strptime(event["Date"], '%Y-%m-%dT%H:%M:%S')+timedelta(hours=3))}}
                    for lines in participant['ListLines']:
                        if lines['Sportsbook'] == "DSI":
                            if lines['LinesType'] != "Money":
                                data[key][lines['LinesType']] = f"{lines['Value']} {lines['Price']}"
                            else:
                                data[key][lines['LinesType']] = f"{lines['Price']}"
                    eventjs[key] = data[key].copy()
                if test:
                    print(json.dumps(eventjs, indent=4))
                betdsi[f'betdsi-{cat["Abbreviation"]}'].append(eventjs)
            print(json.dumps(betdsi, indent=4))
            if not os.path.isdir(sports[cat["Abbreviation"]]):
                os.mkdir(sports[cat["Abbreviation"]])
            if len(betdsi[f'betdsi-{cat["Abbreviation"]}']) > 0:
                with open(f'./{sports[cat["Abbreviation"]]}/betdsi.json', 'w') as out:
                    json.dump(betdsi, out, indent=4)
            else:
                print(f"No data for {cat['Abbreviation']}")
        else:
            print("No sports available",cat['Abbreviation'])
    except:
        print("Error", cat['Abbreviation'], response.text)
        traceback.print_exc()


def main():
    logo()
    response = requests.post('https://widget-api.livelines.com/api/v1/generalrole/authmodule/auth', headers=headers,
                                 data='{"Key":"Y9w497S9y3CXewKG"}')
    auth = json.loads(response.text)
    print("Categories", auth['details']['Categories'])
    for cat in auth['details']['Categories']:
        if cat['Abbreviation'] in sports.keys():
            scrape(auth, cat)


def logo():
    os.system('color 0a')
    print("""
        ____       __  ____  _____ ____
       / __ )___  / /_/ __ \/ ___//  _/
      / __  / _ \/ __/ / / /\__ \ / /  
     / /_/ /  __/ /_/ /_/ /___/ // /   
    /_____/\___/\__/_____//____/___/   
===========================================
        BetDSI.eu bets scraper by:
      https://github.com/evilgenius786
===========================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
___________________________________________
""")


if __name__ == '__main__':
    main()
