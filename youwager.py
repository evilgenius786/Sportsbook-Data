import json
import os
import traceback
from datetime import datetime, timedelta

import requests

test = False

api = 'https://a.ffsvrs.lv:8018/api/lines'

fetchSports = False
sjson = "youwager.json"
try:
    with open(sjson) as bfile:
        sports = json.load(bfile)
except:
    fetchSports = True
    traceback.print_exc()
    sports = {}


def getSports():
    global sports
    res = json.loads(requests.get('https://a.ffsvrs.lv:8018/api/sports/active').content)
    print(json.dumps(res, indent=4))
    all_sports = {}
    data = sports.copy()
    for sport in res:
        for league in sport['leagues']:
            key = f"{sport['name']}/{league}"
            all_sports[key] = getInitial(key.replace("/", " "))
            if key not in data.keys():
                data[key] = getInitial(key.replace("/", " "))
    print(json.dumps(all_sports, indent=4))
    print(json.dumps(data, indent=4))
    with open(sjson, 'w') as bfile:
        json.dump(data, bfile, indent=4)
    with open(sjson) as bfile:
        sports = json.load(bfile)


def getInitial(msg):
    return ''.join([x[0] for x in msg.split()])


def scrape(sport):
    print("Working on", sport)
    res = requests.get(f'{api}/{sport}').text
    lines = json.loads(res)
    teams = []
    for line in lines:
        date = str(datetime.strptime(f"{line['dateTime'].split('.')[0]}", "%Y-%m-%dT%H:%M:%S"))
        away = f"{line['away']['rotationNumber']} {line['away']['name']}".title()
        home = f"{line['home']['rotationNumber']} {line['home']['name']}".title()
        team = {
            away: {
                "Spread": f"{line['lines'][0]['spread']['points']} {line['lines'][0]['spread']['away']}",
                "Total": f"{line['lines'][0]['total']['points']} {line['lines'][0]['total']['away']}",
                "Money": f"{line['lines'][0]['moneyLine']['away']}",
                "Date": date
            },
            home: {
                "Spread": f"{line['lines'][0]['spread']['points']} {line['lines'][0]['spread']['home']}",
                "Total": f"{line['lines'][0]['total']['points']} {line['lines'][0]['total']['home']}",
                "Money": f"{line['lines'][0]['moneyLine']['home']}",
                "Date": date
            }
        }
        teams.append(team)
    data = {f"youwager-{sports[sport]}": teams}
    print(json.dumps(data, indent=4))
    if not os.path.isdir(sports[sport]):
        os.mkdir(sports[sport])
    if len(data[f"youwager-{sports[sport]}"]) > 0:
        with open(f'./{sports[sport]}/youwager.json', 'w') as outfile:
            json.dump(data, outfile)
    else:
        print(f"No data for {sport}")


def main():
    logo()
    if fetchSports:
        getSports()
        # input("Done")
    for sport in sports.keys():
        scrape(sport)


def logo():
    os.system('color 0a')
    print(r"""
    _____.___.             __      __                              
    \__  |   | ____  __ __/  \    /  \_____     ____   ___________ 
     /   |   |/  _ \|  |  \   \/\/   /\__  \   / ___\_/ __ \_  __ \\
     \____   (  <_> )  |  /\        /  / __ \_/ /_/  >  ___/|  | \/
     / ______|\____/|____/  \__/\  /  (____  /\___  / \___  >__|   
     \/                          \/        \//_____/      \/       
==========================================================================
            YouWager.lv scraper by github.com/evilgenius786
==========================================================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
__________________________________________________________________________
""")


if __name__ == '__main__':
    main()
