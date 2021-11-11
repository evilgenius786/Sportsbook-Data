import json
import os

import requests

test = False

api = 'https://a.ffsvrs.lv:8018/api/lines'
sports = {
    "Football/NFL": "NFL",
    "Baseball/MLB": "MLB",
    "Football/College": "NCAAF",
    "Basketball/Germany": "GBBL",
    "Basketball/NBA": "NBA",
    "Hockey/NHL": "NHL",
    "MMA/UFC": "UFC",
    "Tennis/Mens%20Tennis": "ATP",
    "Tennis/Womens%20Tennis": "WTA"
}


def scrape(sport):
    print("Working on", sport)
    res = requests.get(f'{api}/{sport}').text
    lines = json.loads(res)
    teams = []
    for line in lines:
        away = f"{line['away']['rotationNumber']} {line['away']['name']}"
        home = f"{line['home']['rotationNumber']} {line['home']['name']}"
        team = {
            away: {
                "spread": f"{line['lines'][0]['spread']['points']} {line['lines'][0]['spread']['away']}",
                "total": f"{line['lines'][0]['total']['points']} {line['lines'][0]['total']['away']}",
                "moneyLine": f"{line['lines'][0]['moneyLine']['away']}",
            },
            home: {
                "spread": f"{line['lines'][0]['spread']['points']} {line['lines'][0]['spread']['home']}",
                "total": f"{line['lines'][0]['total']['points']} {line['lines'][0]['total']['home']}",
                "moneyLine": f"{line['lines'][0]['moneyLine']['home']}",
            }
        }
        teams.append(team)
    data = {f"youwager-{sports[sport]}": teams}
    print(json.dumps(data, indent=4))
    if not os.path.isdir(sports[sport]):
        os.mkdir(sports[sport])
    with open(f'./{sports[sport]}/youwager.json', 'w') as outfile:
        json.dump(data, outfile)


def main():
    logo()
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
