import json
import os
import traceback
from datetime import datetime, timedelta

import requests

test = False
api = "https://betslipapi.isppro.net/api/Guest"

fetchSports = False
sjson = "jazzsports.json"
try:
    with open(sjson) as bfile:
        sports = json.load(bfile)
except:
    fetchSports = True
    traceback.print_exc()
    sports = {}


def getSports():
    global sports
    res = json.loads(requests.post(f'{api}/GetActiveLeagues', json={"Player": "1JAZZMAST"}).text)
    print(json.dumps(res, indent=4))
    all_sports = {}
    data = sports.copy()
    for sport in res:
        # print(json.dumps(s, indent=4))
        for league in sport['Leagues']:
            key = f"{sport['Sport']}-{league['IdSport']}-{getInitial(league['LeagueDescription'])}".replace(" ","")
            all_sports[league['IdLeague']] = key
            if league['IdLeague'] not in sport.keys():
                data[league['IdLeague']] = key
    print(json.dumps(all_sports, indent=4))
    print(json.dumps(data, indent=4))
    with open(sjson, 'w') as bfile:
        json.dump(data, bfile, indent=4)
    with open(sjson) as bfile:
        sports = json.load(bfile)


def getInitial(msg):
    return ''.join([x[0] for x in msg.split()])


def scrape(sport):
    headers = {
        "Player": "1JAZZMAST",
        "LeagueList": [sport]
    }
    js = requests.post(f'{api}/GetNewLines', json=headers).text
    res = json.loads(js)
    # print(json.dumps(res, indent=4))
    for league in res:
        print("Working on", league['Description'])
        teams = []
        for game in league['Games']:
            visitor = f"{game['Vnum']} {game['Vtm']}".title()
            home = f"{game['Hnum']} {game['Htm']}".title()
            date = str(datetime.strptime(f"{game['Gmdt']} {game['Gmtm']}", "%Y%m%d %H:%M:%S") + timedelta(hours=3))
            data = {
                visitor: {
                    "Spread": f"{game['Lines'][0]['Vsprdt']} {game['Lines'][0]['Vsprdoddst']}",
                    "Total": f"{game['Lines'][0]['Ovt']} {game['Lines'][0]['Ovoddst']}",
                    "Money": f"{game['Lines'][0]['Voddst']}",
                    "Date": date
                },
                home: {
                    "Spread": f"{game['Lines'][0]['Hsprdt']} {game['Lines'][0]['Hsprdoddst']}",
                    "Total": f"{game['Lines'][0]['Unt']} {game['Lines'][0]['Unoddst']}",
                    "Money": f"{game['Lines'][0]['Hoddst']}",
                    "Date": date
                }
            }
            teams.append(data)
        print(json.dumps(teams, indent=4))
        if not os.path.isdir(sports[sport]):
            os.mkdir(sports[sport])
        if len(teams) > 0:
            with open(f"./{sports[sport]}/jazzsports.json", 'w') as out:
                json.dump({f"jazzsports-{sports[sport]}": teams}, out, indent=4)
        else:
            print(f"No data for {sport}")


def main():
    logo()
    if fetchSports:
        getSports()
        input("Done")
    for sport in sports.keys():
        scrape(sport)
        # break


def logo():
    os.system('color 0a')
    print(r"""
   $$$$$\                                      $$$$$$\                                 $$\               
   \__$$ |                                    $$  __$$\                                $$ |              
      $$ | $$$$$$\  $$$$$$$$\ $$$$$$$$\       $$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\ $$$$$$\    $$$$$$$\ 
      $$ | \____$$\ \____$$  |\____$$  |      \$$$$$$\  $$  __$$\ $$  __$$\ $$  __$$\\_$$  _|  $$  _____|
$$\   $$ | $$$$$$$ |  $$$$ _/   $$$$ _/        \____$$\ $$ /  $$ |$$ /  $$ |$$ |  \__| $$ |    \$$$$$$\  
$$ |  $$ |$$  __$$ | $$  _/    $$  _/         $$\   $$ |$$ |  $$ |$$ |  $$ |$$ |       $$ |$$\  \____$$\ 
\$$$$$$  |\$$$$$$$ |$$$$$$$$\ $$$$$$$$\       \$$$$$$  |$$$$$$$  |\$$$$$$  |$$ |       \$$$$  |$$$$$$$  |
 \______/  \_______|\________|\________|       \______/ $$  ____/  \______/ \__|        \____/ \_______/ 
                                                        $$ |                                             
                                                        $$ |                                             
                                                        \__|                                             
============================================================================================================
                        jazzsports.ag scraper by github.com/evilgenius786
============================================================================================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
____________________________________________________________________________________________________________
""")


if __name__ == '__main__':
    main()
