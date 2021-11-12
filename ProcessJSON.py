import json
import os
import re


def main():
    for file in os.listdir("./NFL"):
        # f = f'./NFL/{file}'
        f = f'./NFL/intertops.json'
        with open(f) as jfile:
            js = json.load(jfile)
            # print(json.dumps(js, indent=4))
            for league in (js[[k for k in js.keys()][0]]):
                for team in league:
                    for line in league[team]:
                        print(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", league[team][line]))
                # teams = [k for k in team.keys()]
                # team1 = team[teams[0]]
                # team2 = team[teams[1]]
                # print(team1, team2)
                break
        break
    return
    # for directory in os.listdir('./'):
    #     if os.path.isdir(directory) and not directory.startswith('.'):
    #         for file in os.listdir(directory):
    #             f = f'./{directory}/{file}'
    #             with open(f) as jfile:
    #                 js = json.load(jfile)
    #                 print(json.dumps(js, indent=4))


if __name__ == '__main__':
    main()
