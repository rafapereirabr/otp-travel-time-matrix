from __future__ import print_function
import os
from org.opentripplanner.scripting.api import OtpsEntryPoint
from time import sleep
import threading
import shutil
import time
import gc
# INPUT ###################################################################################################
###################################################################################################

# max number of threads to use in parallel
max_threads = 2

# Trips
fromm = 10             # departure time start
until = 14             # departure time end
every = 30            # frequency (every 30 minutes)
# Max travel time in seconds | 1h = 3600 seconds , 2h = 7200 seconds, 3h = 10800 sec
time_threshold = 3600

# date of trips
year = 2015
month = 9
day = 15
mydate = "2015mix"

###################################################################################################
# import garbage collector (celan RAM memory)
gc.collect()


# Start timing the code
start_time = time.time()

# THREADED VERSION OF OTP SCRIPT


# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs(['--graphs', '.', '--router', 'portland'])


# Get the default router [outside]
router = otp.getRouter('portland')

# # set max snapping distance
# graph.getSampleFactory().setSearchRadiusM(100)


gc.collect()
###################################################################################################
###################################################################################################
filename = 'points.csv'
batch_size = 128
files = []
try:
    os.mkdir('temp_data')
except:
    print('folder already exists, continuing')

with open(filename, 'r') as fin:
    header = fin.next()
    count = 0
    for line in fin:
        if count % 128 == 0:
            fname = 'temp_data/' + str(count) + '_temp_points.csv'
            files.append(fname)
            try:
                fout.close()
            except:
                pass
            fout = open(fname, 'w')
            fout.write(header)
        fout.write(line)
        count += 1
    fout.close()

###################################################################################################
# 500 ############################################################################################


# make a list of jobs to do
jobs = []
for points in files:
    jobs.append(points)
# for h in range(fromm, until):
#     for m in range(0,60,every):
#         jobs.append((h,m))

# define a function describing a complete job
# I just copy-pasted what you had in the loop into here


def do_the_stuff(p):

  # Read Points of Destination - The file points.csv contains the columns GEOID, X and Y [inside]
  points = otp.loadCSVPopulation(p, 'Y', 'X')
  dests = otp.loadCSVPopulation(filename, 'Y', 'X')

# Create a default request for a given time
  req = otp.createRequest()
  req.setDateTime(year, month, day, 10, 00, 00)
  req.setMaxTimeSec(time_threshold)  # 1h = 3600 seconds , 2h = 7200 seconds
  # 'WALK,TRANSIT,BUS,RAIL,SUBWAY'
  req.setModes('WALK,TRANSIT,BUS,RAIL,SUBWAY,TRAM')
  req.setClampInitialWait(0)                # clamp the initial wait time to zero

# Create a CSV output
  matrixCsv = otp.createCSVOutput()
  matrixCsv.setHeader(['year', 'depart_time', 'origin',
                       'destination', 'walk_distance', 'travel_time'])

  # Start Loop
  for origin in points:
    print("Processing idhex500 origin: ", "10-00", " ",
          origin.getStringData('GEOID'), 'on ', threading.current_thread())
    req.setOrigin(origin)
    spt = router.plan(req)
    if spt is None:
        continue

    # Evaluate the SPT for all points
    result = spt.eval(dests)

# Add a new row of result in the CSV output
    for r in result:
      matrixCsv.addRow([mydate, "10:00:00", origin.getStringData(
          'GEOID'), r.getIndividual().getStringData('GEOID'), r.getWalkDistance(), r.getTime()])

# Save the result
  matrixCsv.save('traveltime_matrix_500_' + p.split('/')[1])
  gc.collect()


#
# ^ that ^ function has to be defined before it's called
# the threading bit is down here vvv
#

# how many threads do you want?
#max_threads = int(raw_input('max threads (int) ? --> '))
# start looping over jobs
threads = []
while len(jobs) > 0:
    if threading.active_count() < max_threads + 1:
        p = jobs.pop()
        print(p)
        thread = threading.Thread(target=do_the_stuff, args=(p,))
        #thread.daemon = True
        thread.start()
        threads.append(thread)
    else:
        sleep(0.1)
# now wait for all daemon threads to end before letting
# the main thread die. Otherwise stuff will get cut off
# before it's finished
while threading.active_count() > 1:
	sleep(0.1)
print('ALL JOBS COMPLETED!')
for t in threads:
    t.join()

print("Elapsed time was %g seconds" % (time.time() - start_time))


shutil.rmtree('temp_data')


###################################################################################################
###################################################################################################
###################################################################################################

print('ALL JOBS COMPLETED!')

print("Elapsed time was %g seconds" %
      (time.time() - start_time), "using %g threads" % (max_threads))
