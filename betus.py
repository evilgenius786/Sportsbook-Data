import json
import os
import re
import traceback
from datetime import timedelta

from dateutil.parser import parse

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


def getText(soup, cname):
    x = soup.find('div', {'class': cname}).text.strip().replace('\u00bd', ".5").replace('\u00a0', '').replace(
        '\n', '').replace('\r', '').replace("-", " -").replace("+", " +").replace("Ev", " Ev").strip()
    return re.sub(' +', ' ', x)


def scrape(sport):
    print("Working on", sport)
    try:
        content = requests.get(f"https://www.betus.com.pa/sportsbook/{sport}").content
        soup = BeautifulSoup(content, 'lxml')
        teams = {f"betus-{sports[sport]}": []}
        for div in soup.find_all('div', {"class": "game-block"}):
            d = div.find('span', {"class": "date font-weight-normal"}).text.strip().replace("EST", "")
            for row in div.find_all('div', {"class": "game-tbl container-fluid mb-1"}):
                data = {
                    f"{getText(row, 'away-rotation g-ln col-3 p-1 col-lg-1 d-none d-lg-flex')} {row.find('span', {'id': 'awayName'}).text.strip()}".title(): {
                        "Spread": getText(row, "g-ln col-3 col-lg-2 p-0 border-left-0 line-container"),
                        "Total": getText(row, "g-ln col-3 col-lg-2 p-0 line-container"),
                        "Money": row.find_all('div', {'class': "g-ln col-3 col-lg-2 p-0 border-left-0 line-container"})[
                            1].text.strip(),
                        "Date": str(parse(f'{row.find("span", {"class": "time"}).text.strip()} {d}'))
                    },
                    f"{getText(row, 'home-rotation g-ln col-3 p-1 col-lg-1 d-none d-lg-flex border-bottom-0')} {row.find('span', {'id': 'homeName'}).text.strip()}".title(): {
                        "Spread": getText(row, "col-3 p-0 col-lg-2 line-container border-bottom-0"),
                        "Total": getText(row, "g-ln col-3 p-0 col-lg-2 border-top-0 line-container border-bottom-0"),
                        "Money": getText(row, "g-ln col-3 p-0 col-lg-2 line-container border-bottom-0"),
                        "Date": str(parse(f'{row.find("span", {"class": "time"}).text.strip()} {d}'))
                    }
                }
                teams[f"betus-{sports[sport]}"].append(data.copy())
            # break
        # print(json.dumps(teams, indent=4))
        # teams[f"betus-{sports[sport]}"] = process(teams[f"betus-{sports[sport]}"])
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

#
# def process(test):
#     newteams = []
#     # print(json.dumps(test, indent=4))
#     for match in test:
#         t1 = [k for k in match.keys()][0]
#         t2 = [k for k in match.keys()][1]
#         newleague = {
#             t1: {
#                 "Spread": "" if match[t1]['Spread'] == "" else (match[t1]['Spread'] if "Ev" not in match[t1][
#                     'Spread'] else f"{match[t1]['Spread'].split(' ')[0]} {match[t2]['Spread'].split(' ')[1].replace('u', 'o')}"),
#                 "Total": "" if match[t1]['Total'] == "" else (match[t1]['Total'] if "Ev" not in match[t1][
#                     'Total'] else f"{match[t1]['Total'].split(' ')[0]} {match[t2]['Total'].split(' ')[1].replace('u', 'o')}"),
#                 "Money": "" if match[t1]['Money'] == "" else (
#                     match[t1]['Money'] if "Ev" not in match[t1]['Money'] else match[t2]['Money'].replace('u', 'o'))
#             },
#             t2: {
#                 "Spread": "" if match[t2]['Spread'] == "" else (match[t2]['Spread'] if "Ev" not in match[t2][
#                     'Spread'] else f"{match[t2]['Spread'].split(' ')[0]} {match[t1]['Spread'].split(' ')[1].replace('o', 'u')}"),
#                 "Total": "" if match[t2]['Total'] == "" else (match[t2]['Total'] if "Ev" not in match[t2][
#                     'Total'] else f"{match[t2]['Total'].split(' ')[0]} {match[t1]['Total'].split(' ')[1].replace('o', 'u')}"),
#                 "Money": "" if match[t2]['Money'] == "" else (
#                     match[t2]['Money'] if "Ev" not in match[t2]['Money'] else match[t1]['Money'].replace('o', 'u'))
#             },
#         }
#
#         newteams.append(newleague)
#         # print(match[t1])
#         # print(match[t2])
#     print(json.dumps(newteams, indent=4))
#     return newteams
