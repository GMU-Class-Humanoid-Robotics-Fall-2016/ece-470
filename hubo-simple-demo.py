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

def getFK(theta):
	Rx = np.identity(4)
	Rx[0,0] = np.cos(theta[0,0])
	Rx[0,1] = np.sin(theta[0,0]) * -1
	Rx[1,0] = np.sin(theta[0,0])
	Rx[1,1] = np.cos(theta[0,0])
	
	Ry = np.identity(4)
	Ry[0,0] = np.cos(theta[1,0])
	Ry[0,1] = np.sin(theta[1,0])
	Ry[1,0] = np.sin(theta[1,0]) * -1
	Ry[1,1] = np.cos(theta[1,0])

	T1 = np.identity(4)
	T1[1,3] = 179.14
	Q1 = np.dot(Rx,T1)
	T2 = np.identity(4)
	T2[2,3] = 181.59
	Q2 = np.dot(Ry,T2)

	Q = np.dot(Q1, Q2)

	position = np.array([[Q[0,2]],[Q[1,2]]])

	#x = 179.14 * math.cos(theta[0]) + 181.59 * math.cos(theta[0] + theta[1]) 
	#y = 179.14 * math.sin(theta[0]) + 181.59 * math.sin(theta[0] + theta[1]) 
	return position

def getJ(theta, dtheta):
	jac = np.zeros((2,2))
	for i in range((np.shape(jac))[0]):
		for j in range((np.shape(jac))[1]):
			tempTheta = np.copy(theta)
			tempTheta[j] = theta[j] + dtheta
			fk = getFK(tempTheta)
			jac[i,j] = (fk[i,0]) / dtheta
	return jac

def getMet(e, G):
	m = math.sqrt(math.pow((e[0] - G[0]),2) + math.pow((e[1] - G[1]),2))
	return m

def getNext(e, G, de, h):
	dx = (G[0] - e[0]) * de / h
	dy = (G[1] - e[1]) * de / h
	DE = np.array([[round(dx,2)],[round(dy,2)]])
	return DE

def getIK(theta, G, dtheta, de, des_err, ref, r):
	e = getFK(theta)
	met = getMet(e, G)
	tempMet = met
	while(met > des_err):
		jac = getJ(theta, dtheta)
		jacInv = np.linalg.pinv(jac)
		DE = getNext(e, G, de, tempMet)
		Dtheta = np.dot(jacInv,DE)
		met = getMet(e, G)
		e = getFK(theta)
	return theta

def setArms(theta, ref, r):
	ref.ref[ha.RSP] = theta[0]
	ref.ref[ha.RSR] = theta[1]

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

theta = np.zeros((2,1))
GOAL = np.array([[361.73-10.09298],[34.5]])
print "get Arm angle"
armTheta = getIK(theta, GOAL, 0.01, 4, 5, ref, r)
print "Arm Angle =", armTheta
setArms(armTheta, ref, r)
print "After set"
simSleep(0.2)



# Close the connection to the channels
r.close()
s.close()
