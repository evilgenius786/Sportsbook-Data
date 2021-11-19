import json
import os
import re
import traceback

mapteam = {}


def createMap():
    teams = []
    for directory in os.listdir():
        if os.path.isdir(directory) and not directory.startswith('.'):
            for file in os.listdir(directory):
                with open(f"./{directory}/{file}") as infile:
                    js = json.load(infile)
                    try:
                        for league in js[[k for k in js.keys()][0]]:
                            try:
                                for team in league.keys():
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
    # print(teams)
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
    # for team in teams:
    #     if team not in temp.keys():
    #         temp[team] = team.title()
    print(json.dumps(temp, indent=4))
    with open("teams.json", 'w') as tfile:
        json.dump(temp, tfile, indent=4)
    for team in teams:
        for k in temp.keys():
            try:
                if team.split(" ")[0] == temp[k].split(" ")[0] or team.lower() in temp[k].lower():
                    mapteam[team] = temp[k]
                    break
            except:
                pass
    for team in teams:
        for k in temp.keys():
            try:
                found = 0
                for word in team.split(" "):
                    if word in temp[k].split(" "):
                        found += 1
                if found > 1:
                    mapteam[team] = temp[k]
                    break
            except:
                pass
    # for team in teams:
    #     for k in temp.keys():
    #         try:
    #             found = 0
    #             for word in team.split(" "):
    #                 if word in temp[k].split(" "):
    #                     found += 1
    #             if found > 0:
    #                 mapteam[team] = temp[k]
    #                 break
    #         except:
    #             pass
    print(json.dumps(mapteam, indent=4))
    with open("map.json", 'w') as mfile:
        json.dump(mapteam, mfile, indent=4)
    for team in teams:
        if team not in mapteam.keys():
            print(team)
    print("Map", len([k for k in mapteam.keys()]))
    print("Temp", len([k for k in temp.keys()]))
    print("teams", len(teams))
    print("Teams left", len(teams) - len([k for k in mapteam.keys()]))


def main():
    createMap()
    convertOdds()


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
                                    mapteam[lkeys[0]]: {
                                        "Spread": getres(team1["Spread"]),
                                        "Money": getres(team1["Money"]),
                                        "Total": getres(team1["Total"])
                                    },
                                    mapteam[lkeys[1]]: {
                                        "Spread": getres(team2["Spread"]),
                                        "Money": getres(team2["Money"]),
                                        "Total": getres(team2["Total"])
                                    },
                                }
                                newjs.append(newleague)
                            except:
                                print("Error", team1)
                                print("Error", team2)
                                traceback.print_exc()
                                # input("Press any key")
                            # break
                    print(json.dumps(newjs, indent=4))
                    with open(f"./{directory}/-{file}", 'w') as jfile:
                        json.dump(newjs, jfile, indent=4)
            # break


def getres(res=""):
    r = [float(x) for x in re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", res)]
    if len(r) > 0:
        odd = r[-1]
        if odd > 10:
            odd = 1 + (odd / 100)
        elif odd < -10:
            odd = 1 - (odd / 100)
        if len(r) == 1:
            res = f"{odd}"
        elif len(r) == 2:
            res = f"{r[0]} {odd}"
    return res


if __name__ == '__main__':
    main()
