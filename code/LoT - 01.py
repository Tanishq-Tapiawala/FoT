#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 18:15:43 2021

@author: tanishqtapiawala
"""

"""
1. Plotting events: passes and shots
2. Reading and parsing the tracking data
3. Plotting individual player trajectory
4. Plotting Starting line-up
5. Looking at goals with tracking and event data
"""

import Metrica_IO as mio
import Metrica_Viz as mviz

# Setting up the initial path
datadir = '../Metrica/sample-data-master/data'
game_id = 2

# Loading the data
events = mio.read_event_data(datadir, game_id)

print(events['Type'].value_counts())

# The position coordinates used by Metrica are between 0 & 1
# Change it to metres and re arrange the coordinate system with centre of the pitch as (0, 0)
events = mio.to_metric_coordinates(events)

# Divide the events into Home and Away data
home_events = events[events['Team'] == 'Home']
away_events = events[events['Team'] == 'Away']

# Frequency of each events
print(home_events['Type'].value_counts())
print(away_events['Type'].value_counts())

# Looking at the Shots 
shots = events[events['Type'] == 'SHOT']

home_shots = home_events[home_events.Type == 'SHOT']
away_shots = away_events[away_events.Type == 'SHOT']

# Subtype gives more information about the shot
# OUT => Out of Play
print(home_shots['Subtype'].value_counts())
print(away_shots['Subtype'].value_counts())

# Calculating the shot taken by different players
print(home_shots['From'].value_counts())
print(away_shots['From'].value_counts())

# Getting the shots that were a goal
goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()

home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

print(home_goals)
print(away_goals)

# Add a column event 'Minute' to the data frame
home_goals['Minute'] = home_goals['Start Time [s]']/60.
away_goals['Minute'] = away_goals['Start Time [s]']/60.

# Plotting the Goals
fig,ax = mviz.plot_pitch()

# 198 is the index of 1st home goal
ax.plot(events.loc[198]['Start X'], events.loc[198]['Start Y'], 'ro')

# Creating the path of ball travel
ax.annotate("", xy=events.loc[198][['End X','End Y']], xytext=events.loc[198][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))

# Visualizing the whole play that led to the Goal
# We see that at index 189 => Ball is recovered
# Index 190 the play starts and 198 is the goal

# plot_events => goes through every index mentioned and keeps adding it in the ax
# annotate => marks the player number 
mviz.plot_events(events.loc[190:198], indicators = ['Marker','Arrow'], annotate=True)

###### TRACKING DATA #####

# To look for every player position (even the players not included in the play)

tracking_home = mio.tracking_data(datadir, game_id, 'Home')
tracking_away = mio.tracking_data(datadir, game_id, 'Away')

tracking_home.columns

# Convert the pitch coordinates
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)

# Plotting some player tracking data over the first minute
# Will plot the trajectory of that player
# 1500 => 60s * 25 fps
fig, ax = mviz.plot_pitch()
ax.plot(tracking_home['Home_11_x'].iloc[:1500], tracking_home['Home_11_y'].iloc[:1500], 'r.', MarkerSize=1)
ax.plot(tracking_home['Home_1_x'].iloc[:1500], tracking_home['Home_1_y'].iloc[:1500], 'b.', MarkerSize=1)
ax.plot(tracking_home['Home_2_x'].iloc[:1500], tracking_home['Home_2_y'].iloc[:1500], 'g.', MarkerSize=1)
ax.plot(tracking_home['Home_3_x'].iloc[:1500], tracking_home['Home_3_y'].iloc[:1500], 'k.', MarkerSize=1)
ax.plot(tracking_home['Home_4_x'].iloc[:1500], tracking_home['Home_4_y'].iloc[:1500], 'c.', MarkerSize=1)

# Plotting the player position during Kickoff
# plot_frame => plots the position of every player and the ball in a particular frame
kickoff_frame = events.loc[0]['Start Frame']
fig, ax = mviz.plot_frame(tracking_home.loc[kickoff_frame], tracking_away.loc[kickoff_frame])

# Plotting th player position during the 1st goal (index => 198)
# the Shot figure
fig, ax = mviz.plot_events(events.loc[198:198], indicators = ['Marker','Arrow'], annotate=True)
goal1_frame = events.loc[198]['Start Frame']
fig, ax = mviz.plot_frame(tracking_home.loc[goal1_frame], tracking_away.loc[goal1_frame], figax=(fig,ax))



# HOMEWORK
# 1) Plot all the passes and the shot for goals 2 & 3
# 2) Plot all shots by Player9. Use a different symbol and transparency for goals
# 3) Plot the position of all the players at Player9 goal
# 4) Calculate how far each player ran


# 1

# Overall 2nd Goal was by the Away team 
# Goal 1(Away) => 823
# Pass started at frame 818
mviz.plot_events(events.loc[818:823], indicators = ['Marker','Arrow'], annotate=True, color='b')

# Goal 2(Home) => 1118
# Pass starts at frame 1109
mviz.plot_events(events.loc[1109:1118], indicators = ['Marker','Arrow'], annotate=True)
# But as there are some challenges mid-play, the graph is blurred 
# So we only consider the shot and pass 
goal2 = events[events['Type'].isin(['SHOT', 'PASS'])]
mviz.plot_events(goal2.loc[1109:1118], indicators = ['Marker','Arrow'], annotate=True)

# Goal 3(Home) => 1723
# Pass start at 1718
# Frame 1721 is an Away frame, thats why we need to split
fig, ax = mviz.plot_events(events.loc[1723:1723], indicators = ['Marker','Arrow'], annotate=True)
mviz.plot_events(events.loc[1718:1720], indicators = ['Marker','Arrow'], annotate=True, figax=(fig,ax))
mviz.plot_events(events.loc[1722:1723], indicators = ['Marker','Arrow'], annotate=True, figax=(fig,ax))


# 2

player9_shot_index = home_shots[home_shots['From'] == 'Player9'].index
fig,ax = mviz.plot_pitch()

for index1 in player9_shot_index:
    if index1 in list(home_goals.index.values):
        ax.plot(events.loc[index1]['Start X'], events.loc[index1]['Start Y'], 'b^', alpha=0.8, ms=9)
    else:
        ax.plot(events.loc[index1]['Start X'], events.loc[index1]['Start Y'], 'ro', alpha=0.4, ms=7)
        
        
# 3

# Player9 goal => 1118
fig, ax = mviz.plot_events(events.loc[1118:1118], indicators = ['Marker','Arrow'], annotate=True)
goal2_frame = events.loc[1118]['Start Frame']
fig, ax = mviz.plot_frame(tracking_home.loc[goal2_frame], tracking_away.loc[goal2_frame], figax=(fig,ax))


# 4
# Solution in LoT - 02
