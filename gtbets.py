import json
import os
import traceback

import requests

test = False
sports = {
    "NFL": "NFL",
    "CF": "NCAAF",
    "MLB": "MLB",
    "NBA": "NBA",
    "IBK": "EL",
    "NHL": "NHL",
    "BOX": "BX",
}

lines = {
    "spread": "Spread",
    "moneyline": "Money",
    "total": "Total"
}


def scrape(sport):
    print("Working on", sport)
    headers = {'Referer': f'https://www.gtbets.ag/wagering1.asp?mode=lines&league={sport}'}
    params = (('action', 'wagevents'), ('l', sport))
    response = requests.get('https://www.gtbets.ag/postback.asp', headers=headers, params=params).text
    # with open('gtbets.json') as infile:
    #     response = infile.read()
    try:
        res = json.loads(response)
        data = {}
        keys = []
        for event in res['events_games']:
            if "-" not in event['vtnm']:
                key = f"{event['vrot']} {event['vtnm'].title()}".title()
                if key not in data.keys():
                    data[key] = {}
                if event['lt'] != "moneyline":
                    data[key][lines[event['lt']]] = f"{event['vps']} {event['vml']}"
                    data[key]['Total'] = f"{event['opts']} {event['oml']}"
                else:
                    data[key][lines[event['lt']]] = f"{event['vml']}"
                keys.append((key, f"{event['hrot']} {event['htnm'].title()}"))
                key = f"{event['hrot']} {event['htnm'].title()}".title()
                if key not in data.keys():
                    data[key] = {}
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
    logo()
    for sport in sports.keys():
        scrape(sport)


def logo():
    os.system('color 0a')
    print("""
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
