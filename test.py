#!/usr/bin/jython
from org.opentripplanner.scripting.api import *

# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs(['--graphs', 'C:/Users/rafa/Desktop/jython_portland',
                               '--router', 'portland'])

# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter('portland')

# Create a default request for a given time
req = otp.createRequest()
req.setDateTime(2015, 9, 15, 10, 00, 00)
req.setMaxTimeSec(1800)

req.setModes('WALK,BUS,RAIL') 


# Read Points of Origin
points = otp.loadCSVPopulation('points.csv', 'Y', 'X')

# Read Points of Destination
dests = otp.loadCSVPopulation('points.csv', 'Y', 'X')


# Create a CSV output
matrixCsv = otp.createCSVOutput()
matrixCsv.setHeader([ 'Origin', 'Destination', 'min_time', 'walK_distance', 'outro_temp' ])

# Start Loop
for origin in points:
  print "Processing: ", origin
  req.setOrigin(origin)
  spt = router.plan(req)
  if spt is None:	continue

  # Evaluate the SPT for all points
  result = spt.eval(dests)
  
  # Find the time to other points
  if len(result) == 0:	minTime = -1
  else:			minTime = min([ r.getTime() for r in result ])
  
  # Add a new row of result in the CSV output
  matrixCsv.addRow([ origin.getStringData('GEOID'), r.getIndividual().getStringData('GEOID'), minTime, r.getWalkDistance() , r.getTime()])


# Save the result
matrixCsv.save('traveltime_matrix.csv')

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
