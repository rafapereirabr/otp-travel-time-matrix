#!/usr/bin/jython
from org.opentripplanner.scripting.api import OtpsEntryPoint

# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs(['--graphs', '.',
                               '--router', 'portland'])

# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter('portland')

# Create a default request for a given time
req = otp.createRequest()
req.setDateTime(2015, 9, 15, 10, 00, 00)
req.setMaxTimeSec(7200)
req.setModes('WALK,BUS,RAIL') 

<<<<<<< HEAD

# Read Points of Origin
points = otp.loadCSVPopulation('points.csv', 'Y', 'X')

# Read Points of Destination
=======
# The file points.csv contains the columns GEOID, X and Y.
points = otp.loadCSVPopulation('points.csv', 'Y', 'X')
>>>>>>> fd09da156550299f2c1b3776a6fdc703871e575b
dests = otp.loadCSVPopulation('points.csv', 'Y', 'X')

# Create a CSV output
matrixCsv = otp.createCSVOutput()
matrixCsv.setHeader([ 'Origin', 'Destination', 'Walk_distance', 'Travel_time' ])

# Start Loop
for origin in points:
  print "Processing origin: ", origin
  req.setOrigin(origin)
  spt = router.plan(req)
  if spt is None: continue

  # Evaluate the SPT for all points
  result = spt.eval(dests)
  
  # Add a new row of result in the CSV output
  for r in result:
    matrixCsv.addRow([ origin.getStringData('GEOID'), r.getIndividual().getStringData('GEOID'), r.getWalkDistance() , r.getTime()])

# Save the result
matrixCsv.save('traveltime_matrix.csv')

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
