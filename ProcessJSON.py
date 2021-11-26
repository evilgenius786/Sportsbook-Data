import json
import os
import re
import traceback

try:
    with open('map.json') as mfile:
        mapteam = json.load(mfile)
except:
    mapteam = {}



def main():
    # createMap()
    # convertOdds()
    # processFiles()
    processOdds()


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
                # print("Odd1", odd1, "Odd2", odd2)
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
                            games[f][team1] = league['Team1']
                            games[f][team2] = league['Team2']
            # print("============================================")
            # print(json.dumps(teams, indent=4))
            # print("============================================")
            # print(json.dumps(games, indent=4))

            for smt in ["Spread", "Money", "Total"]:
                if smt not in data.keys():
                    data[smt] = {}
                for team in teams.keys():
                    # if team not in data[smt].keys():
                    data[smt][team] = {"Value": "0", "Service": "None"}
                    # break
                    # if teams[team] not in data[smt].keys():
                    data[smt][teams[team]] = {"Value": "0", "Service": "None"}
                    # break
            # print("=============================================")
            # print("Data: ", json.dumps(data, indent=4))

            for service in games.keys():
                for team in teams.keys():
                    for smt in ["Spread", "Money", "Total"]:
                        if team in games[service].keys():
                            # print(data[smt][team]['Value'])
                            # print(team, games[service][team][smt])
                            if data[smt][teams[team]]['Service'] != service and float(
                                    data[smt][team]['Value'].split()[-1]) < float(
                                    games[service][team][smt].split()[-1]):
                                data[smt][team] = {"Value": games[service][team][smt], "Service": service}
                        if teams[team] in games[service].keys():
                            if data[smt][team]['Service'] != service and float(
                                    data[smt][teams[team]]['Value'].split()[-1]) < float(
                                    games[service][teams[team]][smt].split()[-1]):
                                data[smt][teams[team]] = {"Value": games[service][teams[team]][smt], "Service": service}
            # print("=============================================")
    # print(json.dumps(data, indent=4))
    with open("highest.json", 'w') as hfile:
        json.dump(data, hfile, indent=4)


def createMap():
    teams = []
    teammap = {}
    for directory in os.listdir():
        if os.path.isdir(directory) and not directory.startswith('.'):
            for file in os.listdir(directory):
                if not file.startswith("-"):
                    with open(f"./{directory}/{file}") as infile:
                        js = json.load(infile)
                        try:
                            leagues = js[[k for k in js.keys()][0]]
                            for league in leagues:
                                try:
                                    for team in league.keys():
                                        lks = [k for k in league.keys()]
                                        teammap[lks[0]] = lks[1]
                                        if team not in teams:
                                            teams.append(team)
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
        if os.path.isdir(directory) and not directory.startswith('.'):
            for file in os.listdir(directory):
                if not file.startswith("-"):
                    newjs = []
                    with open(f'./{directory}/{file}') as jfile:
                        js = json.load(jfile)
                        # print(json.dumps(js, indent=4))
                        key = [k for k in js.keys()][0]
                        for league in js[key]:
                            lkeys = [k for k in league.keys()]
                            team1 = league[lkeys[0]]
                            team2 = league[lkeys[1]]
                            try:
                                newleague = {
                                    "Team1": {
                                        "Name": mapteam[lkeys[0]],
                                        "Spread": getres(team1["Spread"] if "Spread" in team1.keys() else "0 0"),
                                        "Money": getres(team1["Money"] if "Money" in team1.keys() else "0"),
                                        "Total": getres(team1["Total"] if "Total" in team1.keys() else "0 0")
                                    },
                                    "Team2": {
                                        "Name": mapteam[lkeys[1]],
                                        "Spread": getres(team2["Spread"] if "Spread" in team2.keys() else "0 0"),
                                        "Money": getres(team2["Money"] if "Money" in team2.keys() else "0"),
                                        "Total": getres(team2["Total"] if "Total" in team2.keys() else "0 0")
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
    main()
