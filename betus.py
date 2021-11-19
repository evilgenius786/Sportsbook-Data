import json
import os
import traceback

import requests
from bs4 import BeautifulSoup

sports = {
    'nfl/': "NFL",
    'ncaaf/': "NCAAF",
    'football/futures/afl-championship/': "AFL",
    'basketball/nba/': "NBA",
    'baseball/mlb/': "MLB",
    'basketball/euro-cup/': "EL",
    'ice-hockey/nhl/': "NHL",
    'boxing/boxing/': 'BX',
}


def scrape(sport):
    print("Working on", sport)
    try:
        content = requests.get(f"https://www.betus.com.pa/sportsbook/{sport}").content
        soup = BeautifulSoup(content, 'lxml')
        teams = {f"betus-{sports[sport]}": []}
        rows = soup.find_all('div', {"class": "game-tbl row"})
        for row in rows:
            data = {
                f"{row.find('div', {'class': 'away-rotation g-ln col-3 p-1 col-lg-1 d-none d-lg-flex'}).text.strip()} {row.find('span', {'id': 'awayName'}).text.strip()}".title(): {
                    "Spread": row.find('div', {
                        'class': "g-ln col-3 col-lg-2 p-0 border-left-0 line-container"}).text.strip().replace('\u00bd',
                                                                                                               ""),
                    "Total": row.find('div', {'class': "g-ln col-3 col-lg-2 p-0 line-container"}).text.strip().replace(
                        '\u00bd', " ").replace('\u00a0', ' ').replace(' ', '').replace('\n', ' ').replace('\r', ''),
                    "Money":
                        row.find_all('div', {'class': "g-ln col-3 col-lg-2 p-0 border-left-0 line-container"})[
                            1].text.strip(),
                },
                f"{row.find('div', {'class': 'home-rotation g-ln col-3 p-1 col-lg-1 d-none d-lg-flex border-bottom-0'}).text.strip()} {row.find('span', {'id': 'homeName'}).text.strip()}".title(): {
                    "Spread": row.find('div', {
                        'class': "col-3 p-0 col-lg-2 line-container border-bottom-0"}).text.strip().replace('\u00bd',
                                                                                                            ""),
                    "Total": row.find('div', {
                        'class': "g-ln col-3 p-0 col-lg-2 border-top-0 line-container border-bottom-0"}).text.strip().replace(
                        '\u00bd', " ").replace('\u00a0', ' ').replace(' ', '').replace('\n', ' ').replace('\r', ''),
                    "Money": row.find('div', {
                        'class': "g-ln col-3 p-0 col-lg-2 line-container border-bottom-0"}).text.strip(),
                }
            }
            teams[f"betus-{sports[sport]}"].append(data.copy())
            # break
        print(json.dumps(teams, indent=4))
        if not os.path.isdir(sports[sport]):
            os.mkdir(sports[sport])
        if len(teams[f"betus-{sports[sport]}"]) > 0:
            with open(f'./{sports[sport]}/betus.json', 'w') as bfile:
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
    ██████  ███████ ████████ ██    ██ ███████ 
    ██   ██ ██         ██    ██    ██ ██      
    ██████  █████      ██    ██    ██ ███████ 
    ██   ██ ██         ██    ██    ██      ██ 
    ██████  ███████    ██     ██████  ███████ 
===================================================
 BetUS.com.pa scraper by github.com/evilgenius786
===================================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
___________________________________________________
""")


if __name__ == '__main__':
    main()
