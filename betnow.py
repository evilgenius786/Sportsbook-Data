import json
import os
import traceback

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse

url = "https://www.betnow.eu/sportsbook-info/"
sports = {
    'football/nfl/': "NFL",
    'football/cfl/': "CFL",
    'football/ncaa-fb/': "NCAAF",
    'baseball/mlb/': "MLB",
    'basketball/wnba/': "WNBA",
    'basketball/nba/': "NBA",
    'basketball/germany-bbl/': "GBBL",
    'fighting/ufc/': "UFC",
    'fighting/boxing/': "BX",
    'hockey/nhl/': "NHL",
    'tennis/atp-european-open-matchups/': "ATP",
    'tennis/wta-tenerife-ladies-open-matchups': "WTA"
}


def scrape(sp):
    print("Working on", sports[sp])
    content = requests.get(url + sp).content
    soup = BeautifulSoup(content, 'lxml')
    teams = {f"betnow-{sports[sp]}": []}
    divs = soup.find_all('div', {"class": "searchContent"})
    date = ""
    for div in divs:
        try:
            date = div.find("div", {"class": "col-md-4 col-xs-12"}).text.strip()
        except:
            pass
        try:
            t = div.find_all('div', {'class': 'odd-info-teams'})
            team1 = t[0].find_all('div')
            if team1[1].text.strip() != "-":
                dt = str(parse(f'{date} {div.find("div", {"class": "odd-time col-md-12"}).text.split("@")[0].strip()}'.strip()))
                team2 = t[1].find_all('div')
                data = {
                    team1[0].text.strip().title(): {
                        "Spread": team1[1].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Total": team1[2].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Money": team1[3].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Date": dt
                    },
                    team2[0].text.strip().title(): {
                        "Spread": team2[1].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Total": team2[2].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Money": team2[3].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Date": dt
                    },
                }
                teams[f"betnow-{sports[sp]}"].append(data.copy())
                print(json.dumps(teams, indent=4))
                if not os.path.isdir(sports[sp]):
                    os.mkdir(sports[sp])
                if len(teams[f"betnow-{sports[sp]}"]) > 0:
                    with open(f'./{sports[sp]}/betnow.json', 'w') as bfile:
                        json.dump(teams, bfile, indent=4)
                else:
                    print(f"No data for {sp}")
            # break
        except:
            print("Error", sports[sp], sp)
            traceback.print_exc()


def main():
    logo()
    for sp in sports.keys():
        scrape(sp)


def logo():
    os.system('color 0a')
    print(r"""
                __________        __     _______                 
                \______   \ _____/  |_   \      \   ______  _  __
                 |    |  _// __ \   __\  /   |   \ /  _ \ \/ \/ /
                 |    |   \  ___/|  |   /    |    (  <_> )     / 
                 |______  /\___  >__|   \____|__  /\____/ \/\_/  
                        \/     \/               \/               
==============================================================================================
                    BetNow scraper by : github.com/evilgenius786
==============================================================================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
______________________________________________________________________________________________
""")


if __name__ == '__main__':
    main()
