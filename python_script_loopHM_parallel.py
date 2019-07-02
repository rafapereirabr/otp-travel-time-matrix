# INPUT ###################################################################################################
###################################################################################################

# max number of threads to use in parallel
max_threads = 8

# Trips
fromm = 10             # set first departure time
until = 14             # set last time
every = 30             # set frequency (every 30 minutes)
time_threshold = 3600  # set a limit to maximum travel time (seconds)

# set date of trips
year= 2015
month = 9
day = 15
mydate = 20150915



###################################################################################################

import gc
gc.collect()

import random

# Start timing the code
import time
start_time = time.time()

# THREADED VERSION OF OTP SCRIPT
import threading
from time import sleep


#!/usr/bin/jython
from org.opentripplanner.scripting.api import OtpsEntryPoint


# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs(['--graphs', '.',
                               '--router', 'portland'])


# Get the default router
router = otp.getRouter('portland')


# Read Points of Destination - The file points.csv contains the columns GEOID, X and Y.
points = otp.loadCSVPopulation('points.csv', 'Y', 'X')
dests = otp.loadCSVPopulation('points.csv', 'Y', 'X')


### make a list of jobs to do
# times should be randomly selected to avoid periodicity effects
jobs = []
for h in range(fromm, until):
  for m in range(0 ,60, every):
    jobs.append((h, int(round(m + random.uniform(0, every)))))
    
# define a function describing a complete job
# I just copy-pasted what you had in the loop into here
def do_the_stuff(h,m):

  # Read Points of Destination - The file points.csv contains the columns GEOID, X and Y [inside]
  points = otp.loadCSVPopulation('points.csv', 'Y', 'X')
  dests = otp.loadCSVPopulation('points.csv', 'Y', 'X')

	# Create a default request for a given time
  req = otp.createRequest()
  req.setDateTime(year, month, day, h, m, 00)
  req.setMaxTimeSec(time_threshold) # 1h = 3600 seconds , 2h = 7200 seconds
  req.setModes('WALK,TRANSIT,BUS,RAIL,SUBWAY,TRAM') # define transport mode : ("WALK,CAR, TRANSIT, TRAM,RAIL,SUBWAY,FUNICULAR,GONDOLA,CABLE_CAR,BUS")
  req.setClampInitialWait(0)                        # clamp the initial wait time to zero
  # for more routing options, check: http://dev.opentripplanner.org/javadoc/0.19.0/org/opentripplanner/scripting/api/OtpsRoutingRequest.html

	# Create a CSV output
  matrixCsv = otp.createCSVOutput()
  matrixCsv.setHeader([ 'year','depart_time', 'origin', 'destination', 'walk_distance', 'travel_time' ])
  
  # Start Loop
  for origin in points:
    print "Processing origin: ", str(h)+"-"+str(m)," ", origin.getStringData('GEOID'), 'on ', threading.current_thread()
    req.setOrigin(origin)
    spt = router.plan(req)
    if spt is None: continue

  	# Evaluate the SPT for all points
    result = spt.eval(dests)

  	# Add a new row of result in the CSV output
    for r in result:
      matrixCsv.addRow([ mydate, str(h) + ":" + str(m) + ":00", origin.getStringData('GEOID'), r.getIndividual().getStringData('GEOID'), r.getWalkDistance() , r.getTime()])

	# Save the result
  matrixCsv.save('traveltime_matrix_'+ str(h)+"-"+str(m) + '.csv')

#
# ^ that ^ function has to be defined before it's called
# the threading bit is down here vvv
#

# how many threads do you want?
#max_threads = int(raw_input('max threads (int) ? --> '))
# start looping over jobs
while len(jobs) > 0:
  if threading.active_count() < max_threads + 1:
    h,m = jobs.pop()
    thread = threading.Thread(target=do_the_stuff, args=(h,m))
#   thread.daemon = True
    thread.start()
  else:
    sleep(0.1)
# now wait for all daemon threads to end before letting
# the main thread die. Otherwise stuff will get cut off
# before it's finished
while threading.active_count() > 1:
  sleep(0.1)
print 'ALL JOBS COMPLETED!'

print("Elapsed time was %g seconds" % (time.time() - start_time))


