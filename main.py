import pandas as pd


def get_data() -> pd.DataFrame:
    """
    Function that takes data from the player per game dataset and removes rows/columns
    from the dataset of players 
    """
    b = pd.read_csv('nba data set/Player Totals.csv')
    b = b.drop(b[b['lg'] != 'NBA'].index, inplace=False)
    b = b.drop(b[b['tm'] == 'TOT'].index, inplace=False)
    cats = ['seas_id','season','birth_year','pos','experience','lg','g','gs','mp','fg','fga','fg_percent','x3p','x3pa','x3p_percent','x2p','x2pa','x2p_percent','e_fg_percent','ft','fta','ft_percent','orb','drb','trb','ast','stl','blk','tov','pf','pts']
    for x in cats:
        b = b.drop(x, axis=1)
    b = b.sort_values(['player', 'age'])
    return b

def find_same_team(team1,team2,df) -> set:
    """
    Function that finds players that have played on the two teams inputed
    Inputs must be abbreviations e.g. POR, BRK, MIL
    """
    teamplayers=df.loc[df['tm'] == team1]
    teamplayers=teamplayers.drop_duplicates(subset=['player_id'])
    playerids=teamplayers['player_id'].tolist()
    twoTeamPlayers={}
    for id in playerids:
        playerhistory=df.loc[df['player_id'] == id]
        teamlist=playerhistory['tm'].tolist()
        teamset=set(teamlist)
        if len(teamset)>1:
            for team in teamlist:
                if playerhistory.iloc[0]['player'] not in twoTeamPlayers:
                    twoTeamPlayers[playerhistory.iloc[0]['player']]=[team]
                else:
                    if team in twoTeamPlayers[playerhistory.iloc[0]['player']]:
                        continue
                    else:
                        twoTeamPlayers[playerhistory.iloc[0]['player']]+=[team]
    finalplayers=set()
    for x in twoTeamPlayers:
        if team2 in twoTeamPlayers[x]:
            finalplayers.add(x)
    return finalplayers

def get_season_data() -> pd.DataFrame:
    """
    Function that takes data from the player per game dataset and removes rows/columns
    from the dataset of players 
    """
    b = pd.read_csv('nba data set/Player Per Game.csv')
    b = b.drop(b[b['lg'] != 'NBA'].index, inplace=False)
    b = b.sort_values(['player', 'age'])
    return b

def find_team_and_stat(team1: str, stat: str, number: int, greater: bool, df) -> set:
    """
    Function that finds players that have played on one team with a specific statline
    Inputs must be abbreviations e.g. POR, BRK, MIL, trb, stl, blk 
    -look for player id's, remove if not tot or on that team
    """
    teamplayers=df.loc[df['tm'] == team1]
    teamplayers=teamplayers.drop_duplicates(subset=['player_id'])
    playerids=teamplayers['player_id'].tolist()
    playerlist=[]
    for id in playerids:
        bf=df.loc[df['player_id'] == id]
        bf = bf[(bf['tm'] == team1) | (bf['tm'] == 'TOT')]
        statlist=bf.values.tolist()
        statlist2 = []
        for x in statlist:
            traded = False
            for y in statlist:
                if (x[1]==y[1]) and (x[0] != y[0]): # checking season equality
                    traded = True
            if traded and x[9] == 'TOT':
                statlist2.append(x)
            elif not traded and x[9] == team1:
                statlist2.append(x)
        cats = ['seas_id','season','player_id','player','birth_year','pos','age','experience','lg','tm','g','gs','mp','fg','fga','fg_percent','x3p','x3pa','x3p_percent','x2p','x2pa','x2p_percent','e_fg_percent','ft','fta','ft_percent','orb','drb','trb','ast','stl','blk','tov','pf','pts']
        statsdicts = []
        for line in statlist2:
            statsdicts += [{cats[i]: line[i] for i in range(len(cats))}]
        playerlist += statsdicts
    outputlist = []
    for x in playerlist:
        if greater:
            if x[stat] > number:
                outputlist += [x['player']]
        else:
            if playerlist[stat] < number:
                outputlist += [x['player']]
    outputset = set(outputlist)
    return outputset


if __name__ == "__main__":
   bf = get_season_data()
   df=get_data()
   for _ in range(100):
    compare = input('Enter stat or team for whether you want to solve a stat + team or a 2 team category: ')
    if compare.lower() == 'stat':
            team1=input('Enter Team 1(E.g. POR, TOR): ')
            stat=input('Enter Stat(E.g. G, Pts, Trb): ')
            number = int(input('Enter Number to Compare Stat to(E.g. 5,10,15): '))
            greater = bool(input('Enter 1 if you want the stat to be greater, or 0 if you want the stat to be lower: '))
            print(find_team_and_stat(team1.upper(),stat,number,greater,bf))
    else:
        team1=input('Enter Team 1(E.g. POR, TOR): ')
        team2=input('Enter Team 1(E.g. MIL, MIA): ')
        print(find_same_team(team1.upper(),team2.upper(),df))

    