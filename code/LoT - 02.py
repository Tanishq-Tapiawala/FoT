#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 00:29:53 2021

@author: tanishqtapiawala
"""

"""
1. Making movies
2. Measuring player speed
3. Generating physical performance reports
"""

import Metrica_IO as mio
import Metrica_Viz as mviz
import Metrica_Velocities as mvel

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Setting up the data path
datadir = '../Metrica/sample-data-master/data'
game_id = 2

# Loading the Event Data
events = mio.read_event_data(datadir, game_id)

# Loading the Tracking Data
tracking_home = mio.tracking_data(datadir, game_id, 'Home')
tracking_away = mio.tracking_data(datadir, game_id, 'Away')

# Converting the coordinate system of the pitch 
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# Reversing the coordinates for the second half so that a team always attacking in 1 direction 
# And it doesnt change the sides during the second half
tracking_home, tracking_away, events = mio.to_single_playing_direction(tracking_home, tracking_away, events)

# Making the Movie
# Using the function in mviz
# Its for the 2nd Goal
plotdir = '../movie'
#mviz.save_match_clip(tracking_home.iloc[73600:73600+500],tracking_away.iloc[73600:73600+500],plotdir,fname='home_goal_2',include_player_velocities=False)

# Calculating Player Velocities
# mvel => calc_player_velocities
# Loops through every player
# Calculates X and Y velocity components separately 
# Throws away outliers (when player position is incorrectly recorded, it gives absurd high value speed)
# So we make those NaN (when max speed > 12 ms (Usain Bolt max speed))
# We need to smooth the data to avoid jittering
# Its done by calculating moving averages
tracking_home = mvel.calc_player_velocities(tracking_home, smoothing=True, filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away, smoothing=True, filter_='moving_average')

# Plotting a frame to see player velocities
# The size of the arrow is proportional to the speed
mviz.plot_frame( tracking_home.loc[10000], tracking_away.loc[10000], include_player_velocities=True, annotate=True)
mviz.plot_frame( tracking_home.loc[500], tracking_away.loc[500], include_player_velocities=True, annotate=True)

# Create a Physical summary dataframe for home players
# Calculate minutes played, distance covered (sprint + run + jog + walk)
# Sprints made by a player and in which region of the field

# New dataframe that has player jersey number as the index
# Extracts the Jersey Number 
home_players = np.unique([c.split('_')[1] for c in tracking_home.columns if c[:4] == 'Home'])
home_summary = pd.DataFrame(index=home_players)

# Calculate minutes played for each player
minutes = []
for player in home_players:
    # search for first and last frames that we have a position observation for each player (when a player is not on the pitch positions are NaN)
    column = 'Home_' + player + '_x' # use player x-position coordinate
    player_minutes = ( tracking_home[column].last_valid_index() - tracking_home[column].first_valid_index() + 1 ) / 25 / 60. # convert to minutes
    minutes.append( player_minutes )
home_summary['Minutes Played'] = minutes
home_summary = home_summary.sort_values(['Minutes Played'], ascending=False)

# Calculate total distance covered for each player
distance = []
for player in home_summary.index:
    column = 'Home_' + player + '_speed'
    player_distance = tracking_home[column].sum()/25./1000 # this is the sum of the distance travelled from one observation to the next (1/25 = 40ms) in km.
    distance.append( player_distance )
home_summary['Distance [km]'] = distance

# Make a simple bar chart of distance covered for each player
plt.subplots()
ax = home_summary['Distance [km]'].plot.bar(rot=0)
ax.set_xlabel('Player')
ax.set_ylabel('Distance covered [km]')

# We see 5, 6, 7 cover the max distance and from the starting position we see they are the midfielders
# plot positions at KO (to find out what position each player is playing)
mviz.plot_frame( tracking_home.loc[51], tracking_away.loc[51], include_player_velocities=False, annotate=True)

# Calculate distance covered while: walking, joggings, running, sprinting
walking = []
jogging = []
running = []
sprinting = []
for player in home_summary.index:
    column = 'Home_' + player + '_speed'
    # Walking (less than 2 m/s)
    player_distance = tracking_home.loc[tracking_home[column] < 2, column].sum()/25./1000
    walking.append( player_distance )
    # Jogging (between 2 and 4 m/s)
    player_distance = tracking_home.loc[ (tracking_home[column] >= 2) & (tracking_home[column] < 4), column].sum()/25./1000
    jogging.append( player_distance )
    # Running (between 4 and 7 m/s)
    player_distance = tracking_home.loc[ (tracking_home[column] >= 4) & (tracking_home[column] < 7), column].sum()/25./1000
    running.append( player_distance )
    # Sprinting (greater than 7 m/s)
    player_distance = tracking_home.loc[ tracking_home[column] >= 7, column].sum()/25./1000
    sprinting.append( player_distance )
    
home_summary['Walking [km]'] = walking
home_summary['Jogging [km]'] = jogging
home_summary['Running [km]'] = running
home_summary['Sprinting [km]'] = sprinting

# Make a clustered bar chart of distance covered for each player at each speed
ax = home_summary[['Walking [km]','Jogging [km]','Running [km]','Sprinting [km]']].plot.bar(colormap='coolwarm')
ax.set_xlabel('Player')
ax.set_ylabel('Distance covered [m]')

# sustained sprints: how many sustained sprints per match did each player complete? Defined as maintaining a speed > 7 m/s for at least 1 second
nsprints = []
sprint_threshold = 7 # minimum speed to be defined as a sprint (m/s)
sprint_window = 1*25 # minimum duration sprint should be sustained (in this case, 1 second = 25 consecutive frames)
for player in home_summary.index:
    column = 'Home_' + player + '_speed'
    # trick here is to convolve speed with a window of size 'sprint_window', and find number of occassions that sprint was sustained for at least one window length
    # diff helps us to identify when the window starts
    player_sprints = np.diff( 1*( np.convolve( 1*(tracking_home[column]>=sprint_threshold), np.ones(sprint_window), mode='same' ) >= sprint_window ) )
    nsprints.append( np.sum( player_sprints == 1 ) )
home_summary['# sprints'] = nsprints
         
# Plot the trajectories for each of player 10's sprints
player = '10'
column = 'Home_' + player + '_speed' # spped
column_x = 'Home_' + player + '_x' # x position
column_y = 'Home_' + player + '_y' # y position

# same trick as before to find start and end indices of windows of size 'sprint_window' in which player speed was above the sprint_threshold
player_sprints = np.diff( 1*( np.convolve( 1*(tracking_home[column]>=sprint_threshold), np.ones(sprint_window), mode='same' ) >= sprint_window ) )
player_sprints_start = np.where( player_sprints == 1 )[0] - int(sprint_window/2) + 1 # adding sprint_window/2 because of the way that the convolution is centred
player_sprints_end = np.where( player_sprints == -1 )[0] + int(sprint_window/2) + 1
# now plot all the sprints
fig,ax = mviz.plot_pitch()
for s,e in zip(player_sprints_start,player_sprints_end):
    ax.plot(tracking_home[column_x].iloc[s],tracking_home[column_y].iloc[s],'ro')
    ax.plot(tracking_home[column_x].iloc[s:e+1],tracking_home[column_y].iloc[s:e+1],'r')


# HOMEWORK
# 1) Estimate top speed of each player
# 2) Measure player acceleration and estimate max acceleration rate for each player












