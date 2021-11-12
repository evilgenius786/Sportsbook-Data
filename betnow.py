import json
import os
import traceback

import requests
from bs4 import BeautifulSoup

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
    for div in divs:
        try:
            t = div.find_all('div', {'class': 'odd-info-teams'})
            team1 = t[0].find_all('div')
            if team1[1].text.strip() != "-":
                team2 = t[1].find_all('div')
                data = {
                    team1[0].text.strip(): {
                        "Spread": team1[1].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Total": team1[2].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Money": team1[3].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                    },
                    team2[0].text.strip(): {
                        "Spread": team2[1].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Total": team2[2].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                        "Money": team2[3].text.strip().replace('½', '.5').replace('\n( ', ' ').replace(' )', ''),
                    },
                }
                teams[f"betnow-{sports[sp]}"].append(data.copy())
                print(json.dumps(teams, indent=4))
                if not os.path.isdir(sports[sp]):
                    os.mkdir(sports[sp])
                with open(f'./{sports[sp]}/betnow.json', 'w') as bfile:
                    json.dump(teams, bfile, indent=4)
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
    print("""
         _______    _______  ___________  _____  ___      ______    __   __  ___ 
        |   _  "\  /"     "|("     _   ")(\\"   \|"  \    /    " \  |"  |/  \|  "|
        (. |_)  :)(: ______) )__/  \\__/ |.\\\\   \    |  // ____  \ |'  /    \:  |
        |:     \/  \/    |      \\\\_ /    |: \.   \\\\  | /  /    ) :)|: /'        |
        (|  _  \\\\  // ___)_     |.  |    |.  \    \. |(: (____/ //  \//  /\\'    |
        |: |_)  :)(:      "|    \:  |    |    \    \ | \        /   /   /  \\\\   |
        (_______/  \_______)     \__|     \___|\____\)  \\"_____/   |___/    \___|
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
