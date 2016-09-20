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

# Walking of HUBO
print "Bend"
positionBend = [0.1, 0.2, 0.3]
for x in positionBend:
	ref.ref[ha.LSR] = x
	ref.ref[ha.RSR] = -x
	ref.ref[ha.RHP] = -x
	ref.ref[ha.RKN] = 2*x
	ref.ref[ha.RAP] = -x
	ref.ref[ha.LHP] = -x
	ref.ref[ha.LKN] = 2*x
	ref.ref[ha.LAP] = -x

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

simSleep(0.2)

for i in range(3):
	print "tilt"	
	positionTilt = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.09, 0.1]
	for x in positionTilt:
		ref.ref[ha.RHR] = x
		ref.ref[ha.RAR] = -x
		ref.ref[ha.LHR] = x
		ref.ref[ha.LAR] = -x

		# Write to the feed-forward channel
		r.put(ref)
		simSleep(0.2)

	simSleep(0.2)

	print "lift foot"
	positionLiftFoot = .3
	ref.ref[ha.LHP] = -positionLiftFoot
	ref.ref[ha.LKN] = 2*positionLiftFoot
	ref.ref[ha.LAP] = -positionLiftFoot

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

	print "extend foot"
	positionExtendFoot = .2
	ref.ref[ha.LKN] = 2*positionExtendFoot
	ref.ref[ha.LAP] = -(positionExtendFoot - positionExtendFoot/2)

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

	print "tilt"
	positionTilt = [0.1, 0.09, 0.07, 0.05, 0.04, 0.03, 0.02, 0.01, 0]
	for x in positionTilt:
		ref.ref[ha.RHR] = x
		ref.ref[ha.RAR] = -x
		ref.ref[ha.LHR] = x
		ref.ref[ha.LAR] = -x

		# Write to the feed-forward channel
		r.put(ref)
		simSleep(0.2)

	simSleep(0.2)

	print "center"
	positionOriginal = 0.4
	ref.ref[ha.LHP] = -positionOriginal
	ref.ref[ha.LKN] = 2*positionOriginal
	ref.ref[ha.LAP] = -positionOriginal

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)
	
	print "tilt"
	positionTilt = [0, 0.01, 0.02, 0.03]
	for x in positionTilt:
		ref.ref[ha.RHR] = x
		ref.ref[ha.RAR] = -x
		ref.ref[ha.LHR] = x
		ref.ref[ha.LAR] = -x

		# Write to the feed-forward channel
		r.put(ref)
		simSleep(0.2)

	simSleep(0.2)

	print "lift foot"
	positionLiftFoot = .5
	ref.ref[ha.RHP] = -positionLiftFoot
	ref.ref[ha.RKN] = 2*positionLiftFoot
	ref.ref[ha.RAP] = -positionLiftFoot

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

	print "extend foot"
	positionExtendFoot = .4
	ref.ref[ha.RKN] = 2*positionExtendFoot
	ref.ref[ha.RAP] = -(positionExtendFoot - positionExtendFoot/2)

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

	print "tilt"
	positionTilt = [0.03, 0.02, 0.01, 0]
	for x in positionTilt:
		ref.ref[ha.RHR] = x
		ref.ref[ha.RAR] = -x
		ref.ref[ha.LHR] = x
		ref.ref[ha.LAR] = -x

		# Write to the feed-forward channel
		r.put(ref)
		simSleep(0.2)

	simSleep(0.2)

	print "center"
	positionOriginal = 0.4
	ref.ref[ha.RHP] = -positionOriginal
	ref.ref[ha.RKN] = 2*positionOriginal
	ref.ref[ha.RAP] = -positionOriginal

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

print "stand"
positionBend = [0.3, 0.2, 0.1, 0]
for x in positionBend:
	ref.ref[ha.LSR] = x
	ref.ref[ha.RSR] = -x
	ref.ref[ha.RHP] = -x
	ref.ref[ha.RKN] = 2*x
	ref.ref[ha.RAP] = -x
	ref.ref[ha.LHP] = -x
	ref.ref[ha.LKN] = 2*x
	ref.ref[ha.LAP] = -x

	# Write to the feed-forward channel
	r.put(ref)
	simSleep(0.2)

# Close the connection to the channels
r.close()
s.close()

