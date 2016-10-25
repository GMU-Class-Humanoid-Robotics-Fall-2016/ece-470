#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2013, Daniel M. Lofaro
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */

import hubo_ach as ha
import ach
import sys
import time
from ctypes import *
import math
import numpy as np

def simSleep(T):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	tick = state.time
	while(True):
		[statuss, framesizes] = s.get(state, wait=True, last=False)
		if((state.time - tick) > T):
			break

def RotationMatrix_x(theta_x):
	Rx = np.identity(4)
	Rx[1,1] = np.cos(theta_x)
	Rx[1,2] = np.sin(theta_x) * -1
	Rx[2,1] = np.sin(theta_x)
	Rx[2,2] = np.cos(theta_x)
	return Rx

def RotationMatrix_y(theta_y):
	Ry = np.identity(4)
	Ry[0,0] = np.cos(theta_y)
	Ry[0,2] = np.sin(theta_y)
	Ry[2,0] = np.sin(theta_y) * -1
	Ry[2,2] = np.cos(theta_y)
	return Ry

def RotationMatrix_z(theta_z):
	Rz = np.identity(4)
	Rz[0,0] = np.cos(theta_z)
	Rz[0,1] = np.sin(theta_z) * -1
	Rz[1,0] = np.sin(theta_z)	
	Rz[1,1] = np.cos(theta_z)
	return Rz

def getFK(theta):
	T1 = np.identity(4)
	T1[0,3] = 94.5
	T2 = np.identity(4)
	T3 = np.identity(4)
	T4 = np.identity(4)
	T4[2,3] = -179.14
	T5 = np.identity(4)
	T5[2,3] = -181.59
	T6 = np.identity(4)

	Q1 = np.dot(RotationMatrix_y(theta[0,0]),T1)
	Q2 = np.dot(RotationMatrix_x(theta[1,0]),T2)
	Q3 = np.dot(RotationMatrix_z(theta[2,0]),T3)
	Q4 = np.dot(RotationMatrix_y(theta[3,0]),T4)
	Q5 = np.dot(RotationMatrix_z(theta[4,0]),T5)
	Q6 = np.dot(RotationMatrix_x(theta[5,0]),T6)

	Q = np.dot(np.dot(np.dot(np.dot(np.dot(Q1,Q2),Q3),Q4),Q5),Q6)

	position = np.array([[Q[0,3]],[Q[1,3]],[Q[2,3]]])

	return position

def getJ(theta, dtheta):
	jac = np.zeros((3,6))
	for i in range((np.shape(jac))[0]):
		for j in range((np.shape(jac))[1]):
			tempTheta = np.copy(theta)
			tempTheta[j] = theta[j] + dtheta
			fk = getFK(theta)
			jac[i,j] = (fk[i,0]) / dtheta
	return jac

def getMet(e, G):
	met = math.sqrt(math.pow((e[0] - G[0]),2) + math.pow((e[1] - G[1]),2) + math.pow((e[2] - G[2]),2))
	return met

def getNext(e, G, de):
	h = getMet(e, G)
	dx = (G[0] - e[0]) * de / h
	dy = (G[1] - e[1]) * de / h
	dz = (G[2] - e[2]) * de / h
	DE = np.array([dx,dy,dz])
	return DE

def getIK(arm, theta, G, ref, r):
	e = getFK(theta)
	met = getMet(e, G)
	tempTheta = np.copy(theta)
	dtheta = 0.01
	de = 20	
	while(met > G[0,0]):
		jac = getJ(tempTheta, dtheta)
		jacInv = np.linalg.pinv(jac)
		DE = getNext(e, G, de)
		Dtheta = np.dot(jacInv, DE)
		tempTheta = np.add(tempTheta, Dtheta)
		met = getMet(e, G)
		e = getFK(tempTheta)

		print 'MET=',met

		if(arm == 'LEFT'):
			ref.ref[ha.LSP] = tempTheta[0]
			ref.ref[ha.LSR] = tempTheta[1]
			ref.ref[ha.LSY] = tempTheta[2]
			ref.ref[ha.LEB] = tempTheta[3]
			ref.ref[ha.LWY] = tempTheta[4]
			ref.ref[ha.LWR] = tempTheta[5]
		elif(arm == 'RIGHT'):
			ref.ref[ha.RSP] = tempTheta[0]
			ref.ref[ha.RSR] = tempTheta[1]
			ref.ref[ha.RSY] = tempTheta[2]
			ref.ref[ha.REB] = tempTheta[3]
			ref.ref[ha.RWY] = tempTheta[4]
			ref.ref[ha.RWR] = tempTheta[5]


		r.put(ref)

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=True)

theta = np.zeros((6,1))
LEFT = 'LEFT'
RIGHT = 'RIGHT'
GOAL = np.array([[350],[30],[60]])
getIK(LEFT, theta, GOAL, ref, r)
simSleep(0.2)

print 'goal2'
GOAL2 = np.array([[350],[-30],[60]])
getIK(LEFT, theta, GOAL2, ref, r)

simSleep(0.2)



# Close the connection to the channels
r.close()
s.close()
