import json
import os
import traceback

import requests
from bs4 import BeautifulSoup

sports = {
    "nfl": "NFL",
    "nhl": "NHL",
    "europa-league": "EL",
    "nba": "NBA",
    "college-football": "NCAAF",
    "cfl": "CFL",
    "mlb": "MLB",
    "college-baseball": "NCAAB",
    "wnba": "WNBA",
    "germany-bbl": "GBBL",
    "college-hockey": "NCAAH",
    "atp": "ATP",
    "wta": "WTA",
    "boxing": "BX",
    "ufc": "UFC"
}


def scrape(sport):
    print("Working on", sport)
    try:
        url = f"https://mybookie.ag/sportsbook/{sport}"
        content = requests.get(url).content
        # with open('mybookie.html', encoding='utf8') as tfile:
        #     content = tfile.read()
        soup = BeautifulSoup(content, 'lxml')
        teams = {f"mybookie-{sports[sport]}": []}
        rows = soup.find_all('div', {"class": "row pt-3"})
        # print(rows)
        for row in rows:
            try:
                btn1 = row.find('div', {'class': 'game-line__visitor-line d-flex justify-content-around'}).find_all(
                    'button')
                btn2 = row.find('div', {'class': 'game-line__home-line d-flex justify-content-around'}).find_all(
                    'button')
                data = {
                    row.find('div', {'class': 'game-line__visitor-team'}).text.strip().title(): {
                        "Spread": btn1[0].text.strip().replace('&frac12', '.5'),
                        "Total": btn1[2].text.strip().replace('&frac12', '.5'),
                        "Money": btn1[1].text.strip().replace('&frac12', '.5'),
                    },
                    row.find('div', {'class': 'game-line__home-team'}).text.strip().title(): {
                        "Spread": btn2[0].text.strip().replace('&frac12', '.5'),
                        "Total": btn2[2].text.strip().replace('&frac12', '.5'),
                        "Money": btn2[1].text.strip().replace('&frac12', '.5'),
                    },
                }
                teams[f"mybookie-{sports[sport]}"].append(data.copy())
            # break
            except:
                pass
        print(json.dumps(teams, indent=4))
        if not os.path.isdir(sports[sport]):
            os.mkdir(sports[sport])
        if len(teams[f"mybookie-{sports[sport]}"])>0:
            with open(f'./{sports[sport]}/mybookie.json', 'w') as bfile:
                json.dump(teams, bfile, indent=4)
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
           *                                         
         (  `           (                )           
         )\))(   (    ( )\            ( /( (     (   
        ((_)()\  )\ ) )((_)  (    (   )\()))\   ))\  
        (_()((_)(()/(((_)_   )\   )\ ((_)\((_) /((_) 
        |  \/  | )(_))| _ ) ((_) ((_)| |(_)(_)(_))   
        | |\/| || || || _ \/ _ \/ _ \| / / | |/ -_)  
        |_|  |_| \_, ||___/\___/\___/|_\_\ |_|\___|  
                 |__/                                
==============================================================
       MyBookie.ag scraper by github.com/evilgenius786
==============================================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
______________________________________________________________
""")


if __name__ == '__main__':
    main()
