import json
import os
import traceback

import requests
from bs4 import BeautifulSoup

sports = {
    "American-Football/NFL-Lines/1018": "NFL",
    "American-Football/NCAAF-Lines/1016": "NCAAF",
    "Baseball/MLB-Playoffs/1073": "MLB",
    "Basketball/NBA-Lines/1070": "NBA",
    "Basketball/German-BBL/1468": "GBBL",
    "Basketball/Euroleague/736": "EL",
    "Ice-Hockey/NHL-Lines/1064": "NHL",
    "Tennis/ATP-US-Open/1167": "ATP",
    "Tennis/WTA-US-Open/2034": "WTA",
    "Boxing-UFC/Boxing/1629": "BX"

}
lines = {
    "Spread": "Spread",
    "Total": "Total",
    "Money Line": "Money"
}

def scrape(sport):
    print("Working on", sport)
    url = f"https://sports.intertops.eu/en/Bets/{sport}"
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')
    try:
        trws = soup.find_all('div', {"class": "trw"})
        teams = {f"intertops-{sports[sport]}": []}
        for trw in trws[1:]:
            try:
                team1 = trw.find('div', {'class': "ustop"}).text.strip().title()
                team2 = trw.find('div', {'class': "usbot"}).text.strip().title()
                btns = trw.find_all('div', {'class': "tablebutton"})
                i = 0
                data = {team1: {}, team2: {}}
                for heading in trws[0].find_all('div', {"class": "res2 th"}):
                    data[team1][lines[heading.text.strip()]] = btns[i].text.strip().replace("\u00a0", " ").replace("\n", " ")
                    data[team2][lines[heading.text.strip()]] = btns[i + 1].text.strip().replace("\u00a0", " ").replace("\n",
                                                                                                                " ")
                    i += 2
                teams[f'intertops-{sports[sport]}'].append(data.copy())
                # break
            except:
                pass
        print(json.dumps(teams, indent=4))
        if not os.path.isdir(sports[sport]):
            os.mkdir(sports[sport])
        if len(teams[f'intertops-{sports[sport]}']) > 0:
            with open(f'./{sports[sport]}/intertops.json', 'w') as tfile:
                json.dump(teams, tfile, indent=4)
        else:
            print(f"No data for {sport}")
    except:
        print("Error", sport)
        traceback.print_exc()


def main():
    logo()
    for sport in sports.keys():
        scrape(sport)


def logo():
    os.system('color 0a')
    print("""
    .___        __                 __                       
    |   | _____/  |_  ____________/  |_  ____ ______  ______
    |   |/    \   __\/ __ \_  __ \   __\/  _ \\\\____ \/  ___/
    |   |   |  \  | \  ___/|  | \/|  | (  <_> )  |_> >___ \ 
    |___|___|  /__|  \___  >__|   |__|  \____/|   __/____  >
             \/          \/                   |__|       \/ 
==================================================================
       intertops.eu scraper by github.com/evilgenius786
==================================================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
__________________________________________________________________
""")


if __name__ == '__main__':
    main()
