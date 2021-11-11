import json
import os

import requests

test = False
api = "https://betslipapi.isppro.net/api/Guest"
sports = {
    724: 'NFL',
    385: 'CFL',
    32: 'NCAAF',
    3: 'NBA',
    113: 'NCAAB',
    7: 'NHL',
    5: 'MLB',
    731: 'EL',
    2121: 'CR',
    342: 'ATP',
    165: 'WTA',
    10: 'BX',
    58: 'UFC'
}


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
            visitor = f"{game['Vnum']} {game['Vtm']}"
            home = f"{game['Hnum']} {game['Htm']}"
            data = {
                visitor: {
                    "spread": f"{game['Lines'][0]['Vsprdt']} {game['Lines'][0]['Vsprdoddst']}",
                    "total": f"{game['Lines'][0]['Ovt']} {game['Lines'][0]['Ovoddst']}",
                    "money": f"{game['Lines'][0]['Voddst']}"
                },
                home: {
                    "spread": f"{game['Lines'][0]['Hsprdt']} {game['Lines'][0]['Hsprdoddst']}",
                    "total": f"{game['Lines'][0]['Unt']} {game['Lines'][0]['Unoddst']}",
                    "money": f"{game['Lines'][0]['Hoddst']}"
                }
            }
            teams.append(data)
        print(json.dumps(teams, indent=4))
        if not os.path.isdir(sports[sport]):
            os.mkdir(sports[sport])
        with open(f"./{sports[sport]}/jazzsports.json", 'w') as out:
            json.dump({f"jazzsports-{sports[sport]}": teams}, out, indent=4)


def main():
    logo()
    for sport in sports.keys():
        scrape(sport)
        # break


def logo():
    os.system('color 0a')
    print("""
   $$$$$\                                      $$$$$$\                                 $$\               
   \__$$ |                                    $$  __$$\                                $$ |              
      $$ | $$$$$$\  $$$$$$$$\ $$$$$$$$\       $$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\ $$$$$$\    $$$$$$$\ 
      $$ | \____$$\ \____$$  |\____$$  |      \$$$$$$\  $$  __$$\ $$  __$$\ $$  __$$\\\\_$$  _|  $$  _____|
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


def loadLeagues():
    with open('leagues.json') as lfile:
        res = json.load(lfile)
    res = json.loads(requests.post(f'{api}/GetActiveLeagues', json={"Player": "1JAZZMAST"}).text)
    print(json.dumps(res, indent=4))
    with open('leagues.json', 'w') as lfile:
        json.dump(res, lfile)
    # leagues = []
    # for sport in res:
    #     # print(json.dumps(s, indent=4))
    #     for league in sport['Leagues']:
    #         leagues.append(league)
    # print(json.dumps(leagues, indent=4))
    # with open('out.json', 'w') as ofile:
    #     json.dump(leagues, ofile)


if __name__ == '__main__':
    main()
