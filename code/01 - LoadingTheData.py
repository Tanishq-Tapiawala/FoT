#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:10:29 2021

@author: tanishqtapiawala
"""

import json

with open('../Statsbomb/data/competitions.json') as f:
    competitions = json.load(f)
    
# Competition ID => 72 => Women's World Cup 2019
competition_id = 72

# Loading all the match lists for this competition
# 30 => Season ID
with open('../Statsbomb/data/matches/'+str(competition_id)+'/30.json') as f:
    matches = json.load(f)
    
matches[0]

matches[0]['home_team']

matches[0]['home_team']['home_team_name']

# Print all the match result
for match in matches:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    home_score = match['home_score']
    away_score = match['away_score']
    print('The match between ' + home_team_name + ' and ' + away_team_name + 
          ' finished ' + str(home_score) +  ' : ' + str(away_score))
    
# For a particular match
home_team_required = "England Women's"
away_team_required = "Sweden Women's"

# To find the ID of that match
for match in matches:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    if (home_team_name == home_team_required) and (away_team_name == away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id: ' + str(match_id_required))

#Exercise: 
#1, Edit the code above to print out the result list for the Mens World cup 
#2, Edit the code above to find the ID for England vs Sweden
#3, Write new code to write out a list of just Sweden's results in the tournament


# 1
# Competition ID => 43  && Season ID => 3

with open('../Statsbomb/data/matches/43/3.json') as f:
    matches = json.load(f)

for match in matches:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    home_score = match['home_score']
    away_score = match['away_score']
    print('The match between ' + home_team_name + ' and ' + away_team_name + 
          ' finished ' + str(home_score) +  ' : ' + str(away_score))



# 2

home_team_required = "England"
away_team_required = "Sweden"

for match in matches:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    if (home_team_name == home_team_required) and (away_team_name == away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id: ' + str(match_id_required))


# 3

for match in matches:
    if(match['home_team']['home_team_name'] == "Sweden" or match['away_team']['away_team_name'] == "Sweden"):
        print('The match between ' + match['home_team']['home_team_name'] + ' and ' + match['away_team']['away_team_name'] + 
              ' finished ' + str(match['home_score']) +  ' : ' + str(match['away_score']))


























