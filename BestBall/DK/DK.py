# -*- coding: utf-8 -*-
"""BBM3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ARuNtzzLE9B4y-a8ZgV0BFL-30O8SmBv

#### Library imports and dataset creation
"""

!pip install vega

import pandas as pd
import seaborn as sns
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.core.pylabtools import figsize
from IPython.display import display
alt.renderers.enable('default')
sns.set_context(font_scale=2)

# to bypass warnings in various dataframe assignments
pd.options.mode.chained_assignment = None

#Read in CSV to dataframe
url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/DK/DK5.csv'
df = pd.read_csv(url, index_col='Team')
df = df.dropna(how='all')

df

"""#### Initial data manipulation"""

df1 = df.groupby('Team')['POS'].apply(lambda x: ', '.join(x.astype(str))).reset_index()

df1['RB'] = df1['POS'].str.count('RB')
df1['WR'] = df1['POS'].str.count('WR')
df1['QB'] = df1['POS'].str.count('QB')
df1['TE'] = df1['POS'].str.count('TE')

df1['build'] = df1['QB'].astype(str) + "/" + df1['RB'].astype(str) + "/" + df1['WR'].astype(str) + "/" + df1['TE'].astype(str)
df1 = df1.drop(columns=['POS', 'RB', 'WR', 'QB', 'TE'])
df1

df2 = pd.merge(df, df1, how='left', on = 'Team')
df3 = df2.groupby('Team')['Name'].apply(lambda x: ', '.join(x.astype(str))).reset_index()
df2 = pd.merge(df2, df3, how='left', on='Team')

final_df = df2.drop(columns=['POS', 'Name_x', 'TEAM', 'Round', 'Pick', 'ADP', 'Value'])
final_df = final_df.drop_duplicates()
final_df ['Players'] = final_df['Name_y']
final_df = final_df.drop(columns=['Name_y'])
final_df

split_df = pd.concat([final_df['Team'], final_df['Players'].str.split(', ', expand=True)], axis=1)
split_df.rename({0 : 1, 1 : 2, 2 : 3, 3 : 4, 4 : 5, 5 : 6, 6 : 7, 7 : 8, 8 : 9, 9 : 10, 10 : 11, 11 : 12, 12 : 13, 13 : 14, 14 : 15, 15 : 16, 16 : 17, 17 : 18, 18 : 19, 19 : 20}, axis='columns', inplace=True)

df1 = pd.merge(df1, df2, how='left', on = 'Team')
df1 = df1.drop(columns=['POS', 'Name_x', 'TEAM', 'Round', 'Pick', 'ADP', 'Value', 'Name_y'])
df1

"""#### Player/Build viz and stats"""

df2

#Exposure calc
exp_df = df2['Name_x'].value_counts()
exp_df = exp_df.reset_index()
exp_df['Count'] = exp_df['Name_x']
exp_df['%'] = round((exp_df['Count'] / df2['Team'].max()) * 100, 1)
exp_df = exp_df.drop(columns=['Name_x'])
exp_df.rename({'index' : 'Player'}, axis='columns', inplace=True)
pos_df = df2.drop_duplicates(subset='Name_x')
pos_df = pos_df.drop(columns=['Team', 'TEAM', 'Round', 'Pick', 'ADP', 'Value', 'Draft Start', 'Cumulative Val', 'Strategy', 'Elite Onesie', 'build', 'Name_y'])
pos_df.rename({'Name_x' : 'Player'}, axis='columns', inplace=True)
exp_df = exp_df.merge(pos_df, on='Player', how='left')
exp_df

pos_count = exp_df['POS'].value_counts()
pos_count = pos_count.reset_index()
pos_count = pos_count.rename({'index' : 'Position'}, axis='columns', inplace=True)
pos_count

#Player Exposure
alt.Chart(exp_df).mark_circle(size=60).encode(
    x='Count',
     y=alt.Y("Player", sort='-x'),
    color='Count',
    tooltip=['Player', 'Count', '%']
).interactive()

#Better exp viz
#my_range=range(1,len(exp_df.index)+1)

#plt.stem(exp_df['Count'])
#plt.xticks(my_range, exp_df['Player'])

#Team Build by draft date, with cumulative ADP value

alt.Chart(df1).mark_circle(size=40).encode(
    x='Draft Start',
    y='Cumulative Val',
    color='build_x',
    tooltip=['Draft Start','Team', 'Strategy', 'Elite Onesie', 'build_x', 'Cumulative Val']
).interactive()

#Team Build by draft date, with cumulative ADP value

alt.Chart(df1).mark_circle(size=40).encode(
    x='Draft Start',
    y='Cumulative Val',
    color='Strategy',
    tooltip=['Draft Start','Team', 'Strategy', 'Elite Onesie', 'build_x', 'Cumulative Val']
).interactive()

#Elite QB/TE with CLV/Date
alt.Chart(df1).mark_circle(size=40).encode(
    x='Draft Start',
    y='Cumulative Val',
    color='Elite Onesie',
    tooltip=['Draft Start','Team', 'Strategy', 'Elite Onesie', 'build_x', 'Cumulative Val']
).interactive

#Breakdown of all builds
build_count = final_df['build'].value_counts()
build_count = build_count.reset_index()
build_count['Count'] = build_count['build']
build_count['%'] = round((build_count['Count'] / df2['Team'].max()) * 100, 1)
build_count = build_count.drop(columns=['build'])
build_count.rename({'index' : 'Build'}, axis='columns', inplace=True)
build_count

#Breakdown of structural strategies
strat_count = final_df['Strategy'].value_counts()
strat_count = strat_count.reset_index()
strat_count['Count'] = strat_count['Strategy']
strat_count['%'] = round((strat_count['Count'] / df2['Team'].max()) * 100, 1)
strat_count = strat_count.drop(columns=['Strategy'])
strat_count.rename({'index' : 'Strategy'}, axis='columns', inplace=True)
strat_count

#Breakdown of Elite QB/TE teams
onesie_count = final_df['Elite Onesie'].value_counts()
onesie_count = onesie_count.reset_index()
onesie_count['Count'] = onesie_count['Elite Onesie']
onesie_count['%'] = round((onesie_count['Count'] / df2['Team'].max()) * 100, 1)
onesie_count = onesie_count.drop(columns=['Elite Onesie'])
onesie_count.rename({'index' : 'Elite Onesie'}, axis='columns', inplace=True)
onesie_count

"""#### Player team by round search"""

#Function that returns all teams with player passed, along with the builds used with the player
def player_team_search(players):
      base = r'^{}'
      expr = '(?=.*{})'
      base = base.format(''.join(expr.format(p) for p in players))
      #Change for number of rounds
      rounds = 20
      i = 1

      with_player = final_df.loc[final_df['Players'].str.contains(base)]
      with_player = with_player.drop_duplicates(subset=['Team'])

      #Building out round by round breakdown for teams with given player
      split_df = pd.concat([final_df['Team'], final_df['Players'].str.split(', ', expand=True)], axis=1)
      split_df.rename({0 : 1, 1 : 2, 2 : 3, 3 : 4, 4 : 5, 5 : 6, 6 : 7, 7 : 8, 8 : 9, 9 : 10, 10 : 11, 11 : 12, 12 : 13, 13 : 14, 14 : 15, 15 : 16, 16 : 17, 17 : 18, 18 : 19, 19: 20}, axis='columns', inplace=True)
      split_df = split_df.merge(with_player, on=['Team', 'Team'], how='right')
      split_df = split_df.drop_duplicates(subset=['Team'])
      print("Round by Round selections with " + ', '.join(players) + " on the team \n")
      while i <= rounds:
        round_count = split_df[i].value_counts().rename_axis('Player').reset_index(name='Times Selected')
        round_count = round_count.sort_index()
        print("===============================================================")
        print("                                    Round " + str(i) + " \n")
        chart = bars = alt.Chart(round_count).mark_bar().encode(
            x=alt.X('Times Selected', axis=alt.Axis(labels=True), title=""),
            y=alt.Y('Player', axis=alt.Axis(labels=True), sort='-x', title=""),
            tooltip=['Player', 'Times Selected'],
            color=alt.Color('Player', legend=None, scale=alt.Scale(scheme=alt.SchemeParams(name='darkblue')))
        ).interactive()
        chart.display(renderer='svg')
        i=i+1

      #List of teams with given player on roster
      #print("===========================================================")
      #print("Full Teams with " + ', '.join(players) + " on the roster \n")
      #print(with_player['Players'].value_counts())

"""#### Build Count with Given Players"""

#Build Count with given players function
def builds_with_players(players):
      base = r'^{}'
      expr = '(?=.*{})'
      base = base.format(''.join(expr.format(p) for p in players))
      #Change for number of rounds
      rounds = 20
      i = 1

      with_player = final_df.loc[final_df['Players'].str.contains(base)]
      with_player = with_player.drop_duplicates(subset=['Team'])    
      print("Structural builds with " + ', '.join(players) + " on the roster")
      print(with_player['build'].value_counts())
      chart = (alt.Chart(with_player).mark_circle(size=30).encode(
      x='Draft Start',
      y='Cumulative Val',
      color='build',
      tooltip=['Draft Start','Team', 'build', 'Cumulative Val']
      ).interactive())
      chart.display(renderer='svg')
      print("\n")

"""#### Strategy and Elite Onesie count functions"""

#Strat Count with given players function
def strats_with_players(players):
      base = r'^{}'
      expr = '(?=.*{})'
      base = base.format(''.join(expr.format(p) for p in players))
      #Change for number of rounds
      rounds = 20
      i = 1

      with_player = final_df.loc[final_df['Players'].str.contains(base)]
      with_player = with_player.drop_duplicates(subset=['Team'])    
      print("Strategies with " + ', '.join(players) + " on the roster")
      print(with_player['Strategy'].value_counts())
      chart = (alt.Chart(with_player).mark_circle(size=30).encode(
      x='Draft Start',
      y='Cumulative Val',
      color='Strategy',
      tooltip=['Draft Start','Team', 'Strategy', 'build', 'Cumulative Val']
      ).interactive())
      chart.display(renderer='svg')
      print("\n")

#Elite Onesie Count with given players function
def onesie_with_players(players):
      base = r'^{}'
      expr = '(?=.*{})'
      base = base.format(''.join(expr.format(p) for p in players))
      #Change for number of rounds
      rounds = 20
      i = 1

      with_player = final_df.loc[final_df['Players'].str.contains(base)]
      with_player = with_player.drop_duplicates(subset=['Team'])    
      print("Elite Onesie teams with " + ', '.join(players) + " on the roster")
      print(with_player['Elite Onesie'].value_counts())
      chart = (alt.Chart(with_player).mark_circle(size=30).encode(
      x='Draft Start',
      y='Cumulative Val',
      color='Elite Onesie',
      tooltip=['Draft Start','Team', 'Strategy', 'Elite Onesie', 'build', 'Cumulative Val']
      ).interactive())
      chart.display(renderer='svg')
      print("\n")

"""#### To use while drafting"""

#Use of build and player search functions
players_to_search = ['Jonathan Taylor']
builds_with_players(players_to_search)
strats_with_players(players_to_search)
onesie_with_players(players_to_search)

#Round by Round searching
player_team_search(players_to_search)

"""#### Round by round ADP reaches (work in progress)"""

#General ADP Guidelines. This function when given a pick will give the user the likely players availible to them in each round, given current ADP.

#WORK IN PROGRESS



def adp_dist(pick):
  adp_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/Underdog/adps.csv'
  adp = pd.read_csv(adp_url, index_col='Player ID')
  adp = adp.dropna(how='all')
  adp = adp.drop_duplicates(subset=['Player Name'])
  picks_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/PicksByRound.csv'
  possible_picks = ['Round','1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th' ]
  picks = pd.read_csv(picks_url, index_col='Round', names=possible_picks, encoding="utf-8-sig")
  picks = picks.dropna(how='all')
  picks = picks.iloc[1: , :]
  picks   
  round = 0
  rounds = 19
  team_temp = pd.DataFrame(columns=['Team', 'Diff'])
  while round <= rounds:
    pos = picks.iloc[round].loc[pick]
    plus = int(pos) + 5
    minus = int(pos) - 5
    temp = adp[adp['ADP'].between(minus, plus)]
    temp['diff'] = int(pos) - temp['ADP']
    error_bars = alt.Chart(temp).mark_errorbar(extent='stdev').encode(
    x=alt.X('diff', scale=alt.Scale(zero=False)),
    y=alt.Y('Player Name')
    )

    points = alt.Chart(temp).mark_point(filled=True, color='black').encode(
    x=alt.X('diff', aggregate='mean'),
    y=alt.Y('Player Name'),
    tooltip=['Player Name','diff', 'ADP', 'Team']
    ).interactive()

    ye = error_bars + points
    ye.display() 
    round = round + 1

"""#### Most likely Team Stacks by pick position accoridng to ADP. (work in progress)"""

#This function will tell you the most likely team stacks given a draft position for players with an ADP lower than 180.
#The closer to zero a team's value is, the more likely that team stack from that draft position has happened.
#General ADP Guidelines. This function when given a pick will give the user the likely players availible to them in each round, given current ADP.
def Likely_team_stacks(pick):
  adp_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/Underdog/adps.csv'
  adp = pd.read_csv(adp_url, index_col='Player ID')
  adp = adp.dropna(how='all')
  adp = adp.drop_duplicates(subset=['Player Name'])
  picks_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/PicksByRound.csv'
  possible_picks = ['Round','1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th' ]
  picks = pd.read_csv(picks_url, index_col='Round', names=possible_picks, encoding="utf-8-sig")
  picks = picks.dropna(how='all')
  picks = picks.iloc[1: , :]
  picks   
  round = 0
  rounds = 19
  team_temp = pd.DataFrame(columns=['Team', 'Diff'])
  temp1 = adp[adp['ADP'] <= 190]
  while round <= rounds:
    pos = picks.iloc[round].loc[pick]
    plus = int(pos) + 5
    minus = int(pos) - 5
    temp = temp1[temp1['ADP'].between(minus, plus)]
    temp['diff'] = int(pos) - temp['ADP']
    for index, row in temp.iterrows():
      team_temp = team_temp.append({'Team': row['Team'], 'Diff' : row['diff']}, ignore_index=True)
    
    round = round + 1
  Avg_team_diff = team_temp.groupby(['Team'])
  Avg_team_diff = team_temp.groupby(['Team'])['Diff'].agg(lambda x: x.unique().mean())
  Avg_team_diff = Avg_team_diff.sort_values(ascending=False)
  print(Avg_team_diff)
  #print(temp1.shape)

"""#### Correlation between pick position and team stack by ADP (work in progress)"""

#This function will tell you the most likely team stacks given a draft position for players with an ADP lower than 180.
#The closer to zero a team's value is, the more likely that team stack from that draft position has happened.
#General ADP Guidelines. This function when given a pick will give the user the likely players availible to them in each round, given current UD ADP.
def pick_to_stack_corr():
  adp_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/adps.csv'
  adp = pd.read_csv(adp_url, index_col='Player ID')
  adp = adp.dropna(how='all')
  adp = adp.drop_duplicates(subset=['Player Name'])
  picks_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/PicksByRound.csv'
  possible_picks = ['Round','1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
  picks = pd.read_csv(picks_url, index_col='Round', names=possible_picks, encoding="utf-8-sig")
  picks = picks.dropna(how='all')
  picks = picks.iloc[1: , :]
  picks   
  round = 0
  rounds = 19
  avg_team_df = pd.DataFrame(columns=['Team', 'Avg'])
  for i in possible_picks:
    team_temp = pd.DataFrame(columns=['Team', 'Diff'])
    temp1 = adp[adp['ADP'] <= 190]
    while round <= rounds:
      pos = picks.iloc[round].loc[i]
      plus = int(pos) + 5
      minus = int(pos) - 5
      temp = temp1[temp1['ADP'].between(minus, plus)]
      temp['diff'] = int(pos) - temp['ADP']
      for index, row in temp.iterrows():
        team_temp = team_temp.append({'Team': row['Team'], 'Diff' : row['diff']}, ignore_index=True)
      round = round + 1
    Avg_team_diff = team_temp.groupby(['Team'])
    Avg_team_diff = team_temp.groupby(['Team'])['Diff'].agg(lambda x: x.unique().mean())
    Avg_team_diff = Avg_team_diff.sort_values(ascending=False)
    for index, row in Avg_team_diff.iterrows():
      avg_team_df = avg_team_df.append({'Team' : row['Team'], 'Avg' : row['Diff']}. ignore_index=True)

    print(Avg_team_diff)
    #print(temp1.shape)

"""#### Functions to call ADP insights (work in progress)"""

#Insert pick you have to see round by round breakdown of the players availible to you.
#pick = '6th'
#adp_dist(pick)
#Likely_team_stacks(pick)

picks_url = 'https://raw.githubusercontent.com/AndrewRucker/Fantasy-Football-and-Betting/main/BestBall/PicksByRound.csv'
  possible_picks = ['Round','1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th' ]
  picks = pd.read_csv(picks_url, index_col='Round', names=possible_picks, encoding="utf-8-sig")
  picks = picks.dropna(how='all')
  picks = picks.iloc[1: , :]
  picks