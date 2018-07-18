import gc
gc.collect()

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


# Read Points of Destination - The file points.csv contains the columns GEOID, X and Y.
points = otp.loadCSVPopulation('points.csv', 'Y', 'X')
dests = otp.loadCSVPopulation('points.csv', 'Y', 'X')


for h in range(7, 13):      # Loop every hour between 7h and 13h
  for m in range(0,60,10):  # Loop every 10 minutes
  
    # Create a default request for a given time
    req = otp.createRequest()
    req.setDateTime(2015, 9, 15, h, m, 00)  # set departure time
    req.setMaxTimeSec(7200)                 # set a limit to maximum travel time (seconds)
    req.setModes('WALK,TRANSIT')            # define transport mode : ("WALK,CAR, TRANSIT, TRAM,RAIL,SUBWAY,FUNICULAR,GONDOLA,CABLE_CAR,BUS")
    # req.maxWalkDistance = 3000                # set the maximum distance (in meters) the user is willing to walk
    # req.walkSpeed = walkSpeed                 # set average walking speed ( meters ?)
    # req.bikeSpeed = bikeSpeed                 # set average cycling speed (miles per hour ?)
    # ? ERROR req.setSearchRadiusM(500)                # set max snapping distance to connect trip origin to street network

# for more routing options, check: http://dev.opentripplanner.org/javadoc/0.19.0/org/opentripplanner/scripting/api/OtpsRoutingRequest.html

    
    # Create a CSV output
    matrixCsv = otp.createCSVOutput()
    matrixCsv.setHeader([ 'year','depart_time', 'origin', 'destination', 'walk_distance', 'travel_time' ])
    
    # Start Loop
    for origin in points:
      print "Processing origin: ", str(h)+"-"+str(m)," ", origin.getStringData('GEOID')
      req.setOrigin(origin)
      spt = router.plan(req)
      if spt is None: continue
    
      # Evaluate the SPT for all points
      result = spt.eval(dests)
      
      # Add a new row of result in the CSV output
      for r in result:
        matrixCsv.addRow([ 2015, str(h) + ":" + str(m) + ":00", origin.getStringData('GEOID'), r.getIndividual().getStringData('GEOID'), r.getWalkDistance() , r.getTime()])
    
    # Save the result
    matrixCsv.save('traveltime_matrix_'+ str(h)+"-"+str(m) + '.csv')
    gc.collect()

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
