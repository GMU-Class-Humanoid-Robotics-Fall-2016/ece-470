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

def simSleep(T):
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	tick = state.time
	while(True):
		[statuss, framesizes] = s.get(state, wait=True, last=False)
		if((state.time - tick) > T):
			break

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
[statuss, framesizes] = s.get(state, wait=False, last=False)

# Tilt right
pos = [0, .1, .15]
for x in pos:
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	
	r.put(ref)
	simSleep(.25)
simSleep(.5)

# Pull up left foot
pos = [0, .3, .6, .9, 1.2]
for x in pos:
	ref.ref[ha.LHP] = -x
	ref.ref[ha.LKN] = 2*x
	ref.ref[ha.LAP] = -x

	r.put(ref)
	simSleep(.25)
simSleep(.5)	

for i in range(2):
	# Squat 0.2m
	pos = [0, .1, .2, .3, .4, .5, .6, .7, .8]
	for p in pos:
		ref.ref[ha.RHP] = -p
		ref.ref[ha.RKN] = 2*p
		ref.ref[ha.RAP] = -p

		r.put(ref)
		simSleep(0.25)

	# Stand up
	pos = [.8, .7, .6, .5, .4, .3, .2, .1, 0]
	for p in pos:
		ref.ref[ha.RHP] = -p
		ref.ref[ha.RKN] = 2*p
		ref.ref[ha.RAP] = -p

		r.put(ref)
		simSleep(0.25)
	simSleep(0.5)

# Put down left foot
pos = [1.2, .9, .6, .3, 0]
for x in pos:
	ref.ref[ha.LHP] = -x
	ref.ref[ha.LKN] = 2*x
	ref.ref[ha.LAP] = -x

	r.put(ref)
	simSleep(.25)
simSleep(.5)	

# Tilt left
pos = [.15, .1, 0, -.1, -.15]
for x in pos:
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	
	r.put(ref)
	simSleep(.25)
simSleep(.5)

# Pull up right foot
pos = [0, .3, .6, .9, 1.2]
for x in pos:
	ref.ref[ha.RHP] = -x
	ref.ref[ha.RKN] = 2*x
	ref.ref[ha.RAP] = -x

	r.put(ref)
	simSleep(.25)
simSleep(.5)	

for i in range(2):
	# Squat 0.1m
	pos = [0, .1, .2, .3, .4, .5]
	for p in pos:
		ref.ref[ha.LHP] = -p
		ref.ref[ha.LKN] = 2*p
		ref.ref[ha.LAP] = -p

		r.put(ref)
		simSleep(0.25)

	# Stand up
	pos = [.5, .4, .3, .2, .1, 0]
	for p in pos:
		ref.ref[ha.LHP] = -p
		ref.ref[ha.LKN] = 2*p
		ref.ref[ha.LAP] = -p

		r.put(ref)
		simSleep(0.25)
	simSleep(0.5)

# Put down right foot
pos = [.9, .6, .3, 0]
for x in pos:
	ref.ref[ha.RHP] = -x
	ref.ref[ha.RKN] = 2*x
	ref.ref[ha.RAP] = -x

	r.put(ref)
	simSleep(.25)
simSleep(.5)	

# Tilt center
pos = [-.15, -.1, 0]
for x in pos:
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	
	r.put(ref)
	simSleep(.25)
simSleep(.5)

# Close the connection to the channels
r.close()
s.close()
