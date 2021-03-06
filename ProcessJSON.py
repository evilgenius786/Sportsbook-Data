import datetime
import json
import os
import re
import shutil
import threading
import time
import traceback

import betdsi
import betnow
import betus
import gtbets
import intertops
import jazzsports
# import mybookie
import xbet
import youwager

mapteam = {}


def createHtml():
    html = f"""<html>
    <head>
     <meta http-equiv="refresh" content="10" />
        <title>Sportsbook Data - BetDSI, BetNow, BetUS, GTbets, InterTops, JazzSports, MyBookie, xBet, YouWager  </title>
        <link rel="icon" type="image/x-icon" href="/sports.png">
        <b>Last updated: {datetime.datetime.now()}</b>
        <style>
            td {{text-align: center;}}
            table, th, td {{border: 1px solid black}}
            th, td {{padding: 2px}}
        </style>
    </head>
    <body>
    <table>
        <tr>
            <th>Teams</th>
            <th>Over</th>
            <th>Under</th>
        </tr>"""
    with open('result.json') as rfile:
        for result in json.load(rfile):
            print("result", result)
            html += f"""<tr>
            <td>{result['Over']} - O</td>
            <td>{result['OverInfo']['Value']}</td>
            <td>{result['UnderInfo']['Value']}</td>
        </tr>
        <tr>
            <td>{result['Under']} - U</td>
            <td><img width="100px" src="./.img/{result['OverInfo']['Service']}.png"></td>
            <td><img width="100px" src="./.img/{result['UnderInfo']['Service']}.png"></td>
        </tr>
        <tr>
            <td colspan="3">Sport: <b>{result['OverInfo']['Sport']}</b>\tLine: <b>{result['Line']}</b>\tArb: <b>{result['Arb']}</b>\tInv: <b>{result['Investment']}</b>\tProf: <b>{result['Profit']}</b></td>
        </tr>
       
<tr><td  colspan="3">Date: {result['OverInfo']["Date"]}</td></tr>
 <tr style="height: 20px"></tr>"""
        html += """</table>
</body>
</html>"""
    with open("index.html", 'w') as rfile:
        rfile.write(html)


def main():
    getFreshData()
    print(datetime.datetime.now(), "Processing files..")
    createMap()
    convertOdds()
    processFiles()
    processOdds()
    print(datetime.datetime.now(), "Processing files finished!")
    createHtml()


def getFreshData():
    for directory in os.listdir('./'):
        if os.path.isdir(directory) and not directory.startswith('.') and not directory.startswith('_'):
            shutil.rmtree(directory)
    print(datetime.datetime.now(), "Fetching live data...")
    threads = [threading.Thread(target=betus.main), threading.Thread(target=betdsi.main),
               threading.Thread(target=betnow.main), threading.Thread(target=gtbets.main),
               threading.Thread(target=intertops.main), threading.Thread(target=jazzsports.main),
               threading.Thread(target=youwager.main), threading.Thread(target=xbet.main),
               # threading.Thread(target=mybookie.main)
               ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(datetime.datetime.now(), "Fetching live data finished!")


def processOdds():
    result = []
    with open("highest.json") as hfile:
        highest = json.load(hfile)
    with open("mapteam.json") as mfile:
        mapteam = json.load(mfile)
    for team in mapteam.keys():
        for smt in highest.keys():
            try:
                odd1 = float(highest[smt][team]['Value'].split()[-1])
                odd2 = float(highest[smt][mapteam[team]]['Value'].split()[-1])
                if odd1 != 0 and odd2 != 0:
                    arb = (100 / odd1) + (100 / odd2)
                    data = {
                        "Over": team,
                        "Under": mapteam[team],
                        "Line": smt,
                        "OverInfo": highest[smt][team],
                        "UnderInfo": highest[smt][mapteam[team]],
                        "Arb": round(arb, 2),
                        "Investment": 100,
                        "Profit": round((100 / arb) - 100, 2)
                    }
                    print(json.dumps(data, indent=4))
                    if data['Arb'] < 100:
                        result.append(data)
            except KeyError:
                # traceback.print_exc()
                # input()
                pass
    with open("result.json", "w") as rfile:
        json.dump(result, rfile, indent=4)


def processFiles():
    data = {}
    for directory in os.listdir('./'):
        if os.path.isdir(directory) and not directory.startswith('.'):
            teams = {}
            games = {}
            for file in os.listdir(directory):
                if file.startswith("-"):
                    with open(f'./{directory}/{file}') as jfile:
                        js = json.load(jfile)
                        f = file[1:-5]
                        games[f] = {}
                        for league in js:
                            team1 = league["Team1"]['Name']
                            team2 = league["Team2"]['Name']
                            if team1 not in teams.keys():
                                teams[team1] = team2
                            del league['Team1']['Name']
                            del league['Team2']['Name']
                            league['Team1']['Sport'] = directory
                            league['Team2']['Sport'] = directory
                            games[f][team1] = league['Team1']
                            games[f][team2] = league['Team2']
            # print("============================================")
            # print("Teams", json.dumps(teams, indent=4))
            # print("============================================")
            # print("Games", json.dumps(games, indent=4))

            for smt in ["Spread", "Money", "Total"]:
                if smt not in data.keys():
                    data[smt] = {}
                for team in teams.keys():
                    # if team not in data[smt].keys():
                    data[smt][team] = {"Value": "0", "Service": "None", "Sport": ""}
                    # break
                    # if teams[team] not in data[smt].keys():
                    data[smt][teams[team]] = {"Value": "0", "Service": "None", "Sport": ""}
                    # break
            # print("=============================================")
            # print("Data: ", json.dumps(data, indent=4))

            for service in [k for k in games.keys()][:-1]:
                for team in teams.keys():
                    for smt in ["Spread", "Money", "Total"]:
                        if team in games[service].keys():
                            # print(data[smt][team]['Value'])
                            # print(team, games[service][team][smt])
                            if data[smt][teams[team]]['Service'] != service and float(
                                    data[smt][team]['Value'].split()[-1]) < float(
                                games[service][team][smt].split()[-1]):
                                data[smt][team] = {"Value": games[service][team][smt], "Service": service,
                                                   "Sport": games[service][team]['Sport'],
                                                   "Date": games[service][team]["Date"]}
                        if teams[team] in games[service].keys():
                            if data[smt][team]['Service'] != service and float(
                                    data[smt][teams[team]]['Value'].split()[-1]) < float(
                                games[service][teams[team]][smt].split()[-1]):
                                try:
                                    data[smt][teams[team]] = {"Value": games[service][teams[team]][smt],
                                                              "Service": service,
                                                              "Sport": games[service][teams[team]]['Sport'],
                                                              "Date": games[service][teams[team]]["Date"]}
                                except:
                                    traceback.print_exc()
                                    print("Error " + str(games[service]))
                                    # print("Error...")
                                    # print(service, team)
                                    # input(json.dumps(games, indent=4))
            # print("=============================================")
    # print(json.dumps(data, indent=4))
    with open("highest.json", 'w') as hfile:
        json.dump(data, hfile, indent=4)


def createMap():
    teams = []
    teammap = {}
    for directory in os.listdir():
        if os.path.isdir(directory) and not directory.startswith('.') and not directory.startswith('_'):
            for file in os.listdir(directory):
                if not file.startswith("-"):
                    with open(f"./{directory}/{file}", encoding='utf8') as infile:
                        try:
                            js = json.load(infile)
                        except:
                            print(directory, file)
                            traceback.print_exc()
                        try:
                            leagues = js[[k for k in js.keys()][0]]
                            for league in leagues:
                                try:
                                    for team in league.keys():
                                        lks = [k for k in league.keys()]
                                        try:
                                            teammap[lks[0]] = lks[1]
                                            if team not in teams:
                                                teams.append(team)
                                        except:
                                            # traceback.print_exc()
                                            print("Error", lks)
                                except:
                                    traceback.print_exc()
                                    pass
                        except:
                            pass
                            traceback.print_exc()
    teams.sort()
    temp = {}
    with open("mapteam.json", 'w') as hfile:
        json.dump(teammap, hfile, indent=4)
    for team in teams:
        rotnum = team.split()[0]
        if rotnum.isdigit() and "(" not in team and len(team.split()) > 2:
            if rotnum not in temp.keys() or len(temp[rotnum]) < len(team):
                temp[rotnum] = team.title()
    for team in teams:
        rotnum = team.split()[0]
        if rotnum.isdigit():
            if rotnum not in temp.keys() or len(temp[rotnum]) < len(team):
                temp[rotnum] = team.title()
    # print(json.dumps(temp, indent=4))

    for team in teams:
        for k in temp.keys():
            try:
                if team not in mapteam.keys() and team.split(" ")[0] == temp[k].split(" ")[0] or team.lower() in temp[
                    k].lower():
                    mapteam[team] = temp[k]
                    break
            except:
                traceback.print_exc()
    for team in teams:
        for k in temp.keys():
            try:
                found = 0
                for word in team.split(" "):
                    if word in temp[k].split(" "):
                        found += 1
                if found > 1:
                    if team not in mapteam.keys():
                        mapteam[team] = temp[k]
                        break
            except:
                traceback.print_exc()
    for team in teams:
        if team not in mapteam.keys():
            mapteam[team] = team
    # print(json.dumps(mapteam, indent=4))
    with open("map.json", 'w') as mfile:
        json.dump(mapteam, mfile, indent=4)
    # for team in teams:
    #     if team not in mapteam.keys():
    #         print(team)
    # print("Map", len([k for k in mapteam.keys()]))
    # print("Temp", len([k for k in temp.keys()]))
    # print("teams", len(teams))
    # print("Teams left", len(teams) - len([k for k in mapteam.keys()]))


def convertOdds():
    for directory in os.listdir('./'):
        if os.path.isdir(directory) and not directory.startswith('.') and not directory.startswith('_'):
            for file in os.listdir(directory):
                if not file.startswith("-"):
                    newjs = []
                    with open(f'./{directory}/{file}', encoding='utf8') as jfile:
                        js = json.load(jfile)
                        # input(json.dumps(js, indent=4))
                        key = [k for k in js.keys()][0]
                        for league in js[key]:
                            lkeys = [k for k in league.keys()]
                            if len(lkeys) > 1:
                                team1 = league[lkeys[0]]
                                try:
                                    team2 = league[lkeys[1]]
                                except:
                                    traceback.print_exc()
                                    print("Error | ", lkeys)
                                    # input("Press any key")
                                    continue
                                try:
                                    newleague = {
                                        "Team1": {
                                            "Name": mapteam[lkeys[0]],
                                            "Spread": getres(
                                                "0 0" if "Spread" not in team1.keys() or team1["Spread"] == "" else (
                                                    team1['Spread'] if "ev" not in team1[
                                                        'Spread'].lower() else f"{team1['Spread'].split(' ')[0]} {team2['Spread'].split(' ')[1].replace('u', 'o')}")),
                                            "Money": getres(team1["Money"] if "Money" in team1.keys() else "0"),
                                            "Total": getres(
                                                "0 0" if "Total" not in team1.keys() or team1["Total"] == "" else (
                                                    team1['Total'] if "ev" not in team1[
                                                        'Total'].lower() else f"{team1['Total'].split(' ')[0]} {team2['Total'].split(' ')[1].replace('u', 'o')}")),
                                            "Date": team1["Date"]
                                        },
                                        "Team2": {
                                            "Name": mapteam[lkeys[1]],
                                            "Spread": getres(
                                                "0 0" if "Spread" not in team2.keys() or team2["Spread"] == "" else (
                                                    team2['Spread'] if "ev" not in team2[
                                                        'Spread'].lower() else f"{team2['Spread'].split(' ')[0]} {team1['Spread'].split(' ')[1].replace('u', 'o')}")),
                                            "Money": getres(team2["Money"] if "Money" in team2.keys() else "0"),
                                            "Total": getres(
                                                "0 0" if "Total" not in team2.keys() or team2["Total"] == "" else (
                                                    team2['Total'] if "ev" not in team2[
                                                        'Total'].lower() else f"{team2['Total'].split(' ')[0]} {team1['Total'].split(' ')[1].replace('u', 'o')}")),
                                            "Date": team2["Date"]
                                        },

                                    }

                                    newjs.append(newleague)
                                except:
                                    print("Error", team1)
                                    print("Error", team2)
                                    traceback.print_exc()
                                    # input("Press any key")
                                # break
                    # print(json.dumps(newjs, indent=4))
                    with open(f"./{directory}/-{file}", 'w') as jfile:
                        json.dump(newjs, jfile, indent=4)


def getres(res=""):
    r = [float(x) for x in re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res)]
    if len(r) > 0:
        odd = r[-1]
        if odd > 10:
            odd = 1 + (odd / 100)
        elif odd < -10:
            odd = 1 - (100 / odd)
        if len(r) == 1:
            res = f"{round(odd, 2)}"
        elif len(r) == 2:
            res = f"{r[0]} {round(odd, 2)}"
    else:
        res = "0"
    return res


if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        time.sleep(1)
