#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 01:53:22 2021

@author: tanishqtapiawala
"""

"""
Pitch Control (at a given location) => Player/Team will gain control of the ball if it moves directly to that location
Provides the answer to - What options are available to player with the ball?

For a given location in a pitch:
    1. How long would it take for the ball to arrive
    2. How long would it take for the player to arrive
    3. Probability that a team will gain possession after it has arrived
    
Key Assumptions:
    1. Ball Arrival: Ball travels at a constant speed => 15 m/s
    2. Player Arrival:
        i. Players have a max speed => 5 m/s
       ii. Players have a max acceleration => 7 m/s/s
      iii. Players take the fastest possible path

Simple Approximation for Arrival Time:
    1. Initial 'Reaction Time of a Player' is 0.7s. During this time, each player continues along their current trajectory
    2. After 0.7s the player runs towards the target location at their max speed of 5m/s

Time taken by the player to control a ball is suggested as 1/4.3 => 0.25s         
"""

import Metrica_IO as mio
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import Metrica_PitchControl as mpc

import numpy as np

