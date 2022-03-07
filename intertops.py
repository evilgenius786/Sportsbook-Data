import json
import os
import traceback
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

lines = {
    "Spread": "Spread",
    "Total": "Total",
    "Money Line": "Money"
}

fetchSports = False
sjson = "intertops.json"
try:
    with open(sjson) as bfile:
        sports = json.load(bfile)
except:
    fetchSports = True
    traceback.print_exc()
    sports = {}


def getSports():
    global sports
    soup = BeautifulSoup(requests.get('https://sports.everygame.eu').content, 'lxml')
    data = sports.copy()
    all_sports = {}
    for li in soup.find_all('li', {"class": "sl"}):
        key = li.find('a')['href']
        all_sports[key] = getInitial(li.text)
        if key not in data.keys():
            data[key] = getInitial(li.text)
    print(json.dumps(all_sports, indent=4))
    print(json.dumps(data, indent=4))
    with open(sjson, 'w') as bfile:
        json.dump(data, bfile, indent=4)
    with open(sjson) as bfile:
        sports = json.load(bfile)


def getInitial(msg):
    return ''.join([x[0] for x in msg.split()])


def scrape(sport):
    print("Working on", sport)
    url = f"https://sports.everygame.eu/{sport}"
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')
    try:
        if '<div class="tbody">' not in str(soup):
            return
        trws = soup.find('div', {"class": "tbody"}).find_all('div', {"class": "trw"})
        teams = {f"intertops-{sports[sport]}": []}
        for trw in trws:
            try:
                team1 = trw.find('div', {'class': "ustop"}).text.strip().title()
                team2 = trw.find('div', {'class': "usbot"}).text.strip().title()
                btns = trw.find_all('div', {'class': "tablebutton"})
                i = 0
                date = str(
                    datetime.strptime(trw.find('span', {"class": "eventdatetime"})['title'],
                                      '%m/%d/%Y<br/>%I:%M %p') - timedelta(hours=5))
                data = {
                    team1: {"Date": date},
                    team2: {"Date": date}
                }
                for heading in trws[0].find_all('div', {"class": "res2 th"}):
                    try:
                        data[team1][lines[heading.text.strip()]] = btns[i].text.strip().replace("\u00a0", " ").replace("\n",
                                                                                                                       " ")
                        data[team2][lines[heading.text.strip()]] = btns[i + 1].text.strip().replace("\u00a0", " ").replace(
                            "\n",
                            " ")
                    except:
                        pass
                    i += 2
                teams[f'intertops-{sports[sport]}'].append(data.copy())
                # break
            except:
                # print("Error", sport)
                # traceback.print_exc()
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
    if fetchSports:
        getSports()
        # input("Done")
    for sport in sports.keys():
        scrape(sport)


def logo():
    os.system('color 0a')
    print(r"""
    .___        __                 __                       
    |   | _____/  |_  ____________/  |_  ____ ______  ______
    |   |/    \   __\/ __ \_  __ \   __\/  _ \\____ \/  ___/
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
