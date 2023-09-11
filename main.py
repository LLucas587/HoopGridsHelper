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
    print(finalplayers)
    

if __name__ == "__main__":
   df=get_data()
   team1=input('Enter Team 1(E.g. POR, TOR): ')
   team2=input('Enter Team 1(E.g. MIL, MIA): ')
   find_same_team(team1,team2,df)

    