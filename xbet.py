import json
import os
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup

fetchSports = True
sjson = "xbet.json"
try:
    with open(sjson) as bfile:
        sports = json.load(bfile)
except:
    fetchSports = True
    traceback.print_exc()
    sports = {}


def getSports():
    global sports
    url = f"https://xbet.ag/sportsbook/"
    soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content, 'lxml')
    data = sports.copy()
    all_sports = {}
    for league in soup.find_all('a', {"class": 'nav-link sub-items-menu__body__item__link active request_league'}):
        key = league.text.strip().split(' ')[0] + getInitial(" ".join(league.text.strip().split(' ')[1:]))
        all_sports[league['href']] = key
        if key not in sports.keys():
            data[league['href']] = key
    print(json.dumps(all_sports, indent=4))
    print(json.dumps(data, indent=4))
    with open(sjson, 'w') as bfile:
        json.dump(data, bfile, indent=4)
    with open(sjson) as bfile:
        sports = json.load(bfile)


def getInitial(msg):
    return ''.join([x[0] for x in msg.split()])


def scrape(sport):
    url = f"https://xbet.ag/sportsbook/{sport}"
    print("Working on", sport, url)
    try:
        content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
    except:
        scrape(sport)
        return
    soup = BeautifulSoup(content, 'lxml')
    teams = {f"xbet-{sports[sport]}": []}
    rows = soup.find_all('div', {"class": "game-line py-3"})
    for row in rows:
        try:
            date = str(datetime.strptime(
                f"{row.find('span', {'class': 'game-line__time__date__hour dynamic_date change__timer sportsbook__line-date'})['data-time']}",
                "%Y-%m-%d %H:%M:%S"))
            btn1 = row.find('div', {'class': 'game-line__visitor-line d-flex justify-content-around'}).find_all(
                'button')
            btn2 = row.find('div', {'class': 'game-line__home-line d-flex justify-content-around'}).find_all('button')
            data = {
                row.find('div', {'class': 'game-line__visitor-team'}).text.strip().title(): {
                    "Spread": btn1[0].text.strip().replace('&frac12', '.5'),
                    "Total": btn1[2].text.strip().replace('&frac12', '.5'),
                    "Money": btn1[1].text.strip().replace('&frac12', '.5'),
                    "Date": date
                },
                row.find('div', {'class': 'game-line__home-team'}).text.strip().title(): {
                    "Spread": btn2[0].text.strip().replace('&frac12', '.5'),
                    "Total": btn2[2].text.strip().replace('&frac12', '.5'),
                    "Money": btn2[1].text.strip().replace('&frac12', '.5'),
                    "Date": date

                },
            }
            teams[f"xbet-{sports[sport]}"].append(data.copy())
        # break
        except:
            pass
    print(json.dumps(teams, indent=4))
    if not os.path.isdir(sports[sport]):
        os.mkdir(sports[sport])
    if len(teams[f"xbet-{sports[sport]}"]) > 0:
        with open(f'./{sports[sport]}/xbet.json', 'w') as bfile:
            json.dump(teams, bfile, indent=4)
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
        ____  ______.           __   
        \   \/  /\_ |__   _____/  |_ 
         \     /  | __ \_/ __ \   __\
         /     \  | \_\ \  ___/|  |  
        /___/\  \ |___  /\___  >__|  
              \_/     \/     \/      
==============================================
 Xbet.ag scraper by github.com/evilgenius786
==============================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
______________________________________
""")


if __name__ == '__main__':
    main()
