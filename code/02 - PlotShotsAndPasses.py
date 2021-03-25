#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:23:37 2021

@author: tanishqtapiawala
"""

import matplotlib.pyplot as plt
import numpy as np
import json

# Size of a football pitch is given in yards in Statsbomb
pitchLengthX = 120
pitchWidthY = 80

# Analyzing the Women's => England vs Sweden 
match_id_required = 69301
home_team_required ="England Women's"
away_team_required ="Sweden Women's"

file_name = str(match_id_required) + '.json'

# Loading the Match Events
with open('../Statsbomb/data/events/' + file_name) as data_file:
    data = json.load(data_file)
    
# Get the nested structure into a dataframe 
# Store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

# A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

# Draw the pitch
from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

# Plot the shots
for i,shot in shots.iterrows():
    x = shot['location'][0]
    y = shot['location'][1]
    
    goal = shot['shot_outcome_name']=='Goal'
    team_name = shot['team_name']
    
    # Setting the size of the shot circle
    circleSize = 2
    
    # Setting the size of the shot in proportional to the xG
    circleSize = np.sqrt(shot['shot_statsbomb_xg'])*12

    if (team_name == home_team_required):
        if goal:
            shotCircle = plt.Circle((x,pitchWidthY-y),circleSize,color="red")
            plt.text((x+1),pitchWidthY-y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
    elif (team_name == away_team_required):
        if goal:
            shotCircle = plt.Circle((pitchLengthX-x,y),circleSize,color="blue") 
            plt.text((pitchLengthX-x+1),y+1,shot['player_name']) 
        else:
            shotCircle = plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
            shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)
    
    
plt.text(5,75,away_team_required + ' shots') 
plt.text(80,75,home_team_required + ' shots') 
     
plt.show()


#Exercise: 
#1, Create a dataframe of passes which contains all the passes in the match
#2, Plot the start point of every Sweden pass. Attacking left to right.
#3, Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database)
#4, Plot arrows to show where the passes we


# 1
# Dataframe for passes
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

# 2
# Draw the pitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
team_required = "Sweden Women's"

for i,passs in passes.iterrows():
    
    if(team_name == team_required):
        x = passs['location'][0]
        y = passs['location'][1]
        
        passCircle = plt.Circle((x, pitchWidthY-y+1), 0.5, color="red")
        passCircle.set_alpha(0.2)
    ax.add_patch(passCircle)
plt.show()
# 3 & 4
# Draw the pitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
player_required = 'Sara Caroline Seger'
for i,passs in passes.iterrows():
   
    if(passs['player_name'] == player_required):
        x = passs['location'][0]
        y = passs['location'][1]
        xl = passs['pass_end_location'][0] - x
        yl = passs['pass_end_location'][1] - y
        
        passCircle = plt.Circle((x, pitchWidthY-y), 2)
        passCircle.set_alpha(0.2)
        ax.add_patch(passCircle)
        
        passArrow = plt.Arrow(x, pitchWidthY-y, xl, yl, width=4)
        ax.add_patch(passArrow)
plt.show()




























