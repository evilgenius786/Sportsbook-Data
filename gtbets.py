import json
import os
import traceback
from datetime import datetime, timedelta

import requests

test = False
lines = {
    "spread": "Spread",
    "moneyline": "Money",
    "total": "Total"
}


fetchSports = False
sjson = "gtbets.json"
try:
    with open(sjson) as bfile:
        sports = json.load(bfile)
except:
    fetchSports = True
    traceback.print_exc()
    sports = {}



def getSports():
    global sports
    headers = {'Referer': f'https://www.gtbets.ag/wagering1.asp'}
    params = {'action': 'waglines'}
    response = requests.get('https://www.gtbets.ag/postback.asp', headers=headers, params=params).text
    data = sports.copy()
    all_sports = {}
    for line in json.loads(response)['lines'][12:]:
        key = line['league']
        if line['use_full_league'] == 1:
            key += "|" + line['full_league_name']
        all_sports[key] = getInitial(key)
        if key not in data.keys():
            data[key] = getInitial(key)
    print(json.dumps(all_sports, indent=4))
    print(json.dumps(data, indent=4))
    with open(sjson, 'w') as bfile:
        json.dump(data, bfile, indent=4)
    with open(sjson) as bfile:
        sports = json.load(bfile)
        # break


def getInitial(msg):
    if "|" in msg:
        t = msg.split("|")[1].replace("-", " ")
        print(t)
        return msg.split("|")[0] + "-" + ''.join([x[0] for x in t.split()])
    return msg


def scrape(sport):
    print("Working on", sport)
    headers = {'Referer': f'https://www.gtbets.ag/wagering1.asp?mode=lines&league={sport}'}
    if "|" in sport:
        params = (('action', 'wagevents'), ('l', sport.split("|")[0]), ('se', sport.split("|")[1]))
    else:
        params = (('action', 'wagevents'), ('l', sport))
    response = requests.get('https://www.gtbets.ag/postback.asp', headers=headers, params=params).text
    # with open('gtbets.json') as infile:
    #     response = infile.read()
    try:
        res = json.loads(response)
        # print(json.dumps(res, indent=4))
        data = {}
        keys = []
        if "events_games" in res.keys():
            for event in res['events_games']:
                if "-" not in event['vtnm']:
                    key = f"{event['vrot']} {event['vtnm'].title()}".title()
                    if key not in data.keys():
                        data[key] = {
                            "Date": str(datetime.strptime(event['dt'], "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=5))}
                    if event['lt'] != "moneyline":
                        data[key][lines[event['lt']]] = f"{event['vps']} {event['vml']}"
                        data[key]['Total'] = f"{event['opts']} {event['oml']}"
                    else:
                        data[key][lines[event['lt']]] = f"{event['vml']}"
                    keys.append((key, f"{event['hrot']} {event['htnm'].title()}"))
                    key = f"{event['hrot']} {event['htnm'].title()}".title()
                    if key not in data.keys():
                        data[key] = {
                            "Date": str(datetime.strptime(event['dt'], "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=5))}
                    if event['lt'] != "moneyline":
                        data[key][lines[event['lt']]] = f"{event['hps']} {event['hml']}"
                        data[key]['Total'] = f"{event['opts']} {event['uml']}"
                    else:
                        data[key][lines[event['lt']]] = f"{event['hml']}"
                    # break

        teams = {f"gtbets-{sports[sport]}": []}
        for x in (sorted(set(keys))):
            teams[f"gtbets-{sports[sport]}"].append({
                x[0]: data[x[0]],
                x[1]: data[x[1]]
            })
        print(json.dumps(teams, indent=4))
        if not os.path.isdir(sports[sport]):
            os.mkdir(sports[sport])
        if len(teams[f"gtbets-{sports[sport]}"]) > 0:
            with open(f'./{sports[sport]}/gtbets.json', 'w') as out:
                json.dump(teams, out, indent=4)
        else:
            print(f"No data for {sport}")
    except:
        print("Error", sport, response)
        traceback.print_exc()


def main():
    # logo()
    if fetchSports:
        getSports()
    for sport in sports.keys():
        scrape(sport)


def logo():
    os.system('color 0a')
    print(r"""
      ___________  ___      __    
     / ___/_  __/ / _ )___ / /____
    / (_ / / /   / _  / -_) __(_-<
    \___/ /_/   /____/\__/\__/___/
========================================
         gtbets.ag scraper by:
       github.com/evilgenius786
========================================
[+] Without browser
[+] Multithreaded
[+] Efficient and fast
[+] Works with API
________________________________________
""")


if __name__ == '__main__':
    main()
